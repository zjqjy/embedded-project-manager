/**
 * Claude CLI 进程管理模块
 *
 * 负责 spawn claude -p 子进程、读取 stream-json 输出、
 * 通过 Tauri 事件系统向前端转发流事件。
 */

use std::io::{BufRead, BufReader};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use serde::Serialize;
use tauri::{AppHandle, Emitter, Manager, State};

/// 向前端发送的原始行事件
#[derive(Clone, Serialize)]
pub struct ClaudeLineEvent {
    pub line: String,
    pub is_error: bool,
}

/// 子进程完成事件
#[derive(Clone, Serialize)]
pub struct ClaudeDoneEvent {
    pub success: bool,
    pub error: Option<String>,
}

/// 管理状态：当前运行的 claude 子进程
pub struct ClaudeState {
    pub child: Mutex<Option<Child>>,
}

impl ClaudeState {
    pub fn new() -> Self {
        Self {
            child: Mutex::new(None),
        }
    }
}

/// 自动检测 git-bash 路径（Claude Code on Windows 必需）
/// 按优先级搜索常见 Git for Windows 安装位置
fn find_git_bash_path() -> Option<String> {
    // 优先级 0: 用户已配置的环境变量
    if let Ok(path) = std::env::var("CLAUDE_CODE_GIT_BASH_PATH") {
        if std::path::Path::new(&path).exists() {
            return Some(path);
        }
    }

    // 优先级 1: PATH 中的 bash（排除 Cygwin 的 /usr/bin/bash）
    if let Ok(path) = std::env::var("PATH") {
        for dir in std::env::split_paths(&path) {
            let candidate = dir.join("bash.exe");
            if candidate.exists() {
                let p = candidate.to_string_lossy().to_string();
                // 跳过 Cygwin 的 bash
                if !p.contains("cygwin") && !p.contains("/usr/bin") {
                    return Some(p);
                }
            }
        }
    }

    // 优先级 2: 常见 Git for Windows 路径
    let common_paths = [
        // Program Files
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        // Local AppData (winget / portable 安装)
        r"C:\Users\23393\AppData\Local\Programs\Git\bin\bash.exe",
        r"C:\Users\23393\AppData\Local\Git\bin\bash.exe",
        // 用户自定义磁盘路径
        r"D:\ZouJinQiang\App\Git\bin\bash.exe",
    ];

    for p in &common_paths {
        if std::path::Path::new(p).exists() {
            return Some(p.to_string());
        }
    }

    None
}

/// 构建 claude CLI 命令配置
/// Windows 上跳过 claude.cmd 包装层（会弹控制台窗口），
/// 直接调用 node + 入口 JS 文件。
fn build_claude_command() -> (String, Vec<String>) {
    #[cfg(target_os = "windows")]
    {
        // 查找 npm 全局安装目录下的 cli.js
        if let Some(appdata) = std::env::var_os("APPDATA") {
            let cli_js = std::path::Path::new(&appdata)
                .join("npm")
                .join("node_modules")
                .join("@anthropic-ai")
                .join("claude-code")
                .join("cli.js");
            if cli_js.exists() {
                return (
                    "node".to_string(),
                    vec![cli_js.to_string_lossy().to_string()],
                );
            }
        }
        // 后备：让 OS 通过 PATH 解析 claude.cmd
        ("claude.cmd".to_string(), vec![])
    }
    #[cfg(not(target_os = "windows"))]
    {
        ("claude".to_string(), vec![])
    }
}

/**
 * 调用 Claude CLI
 *
 * 启动 claude -p 子进程，在后台线程中读取 stdout/stderr，
 * 通过 Tauri event 系统逐行转发到前端。
 */
#[tauri::command]
pub async fn call_claude(
    app: AppHandle,
    state: State<'_, ClaudeState>,
    prompt: String,
    permission_mode: String,
) -> Result<(), String> {
    // 检查是否已有运行中的进程
    {
        let guard = state.child.lock().map_err(|e| format!("状态锁冲突: {}", e))?;
        if guard.is_some() {
            return Err("已有正在运行的 Claude 进程".to_string());
        }
    }

    // 非交互式 -p 模式统一使用 acceptEdits 避免阻塞
    let perm_flag = match permission_mode.as_str() {
        "interactive" | "notify" | "silent" => "acceptEdits",
        _ => "acceptEdits",
    };

    let (program, extra_args) = build_claude_command();

    // 构建命令
    let mut cmd = &mut Command::new(&program);
    // 插入 extra_args（Windows 上为 cli.js 路径）
    for a in &extra_args {
        cmd = cmd.arg(a);
    }
    cmd = cmd
        .arg("-p")
        .arg(&prompt)
        .arg("--output-format")
        .arg("stream-json")
        .arg("--verbose")
        .arg("--permission-mode")
        .arg(perm_flag)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());

    // Windows 上隐藏控制台窗口并设置 git-bash 路径
    #[cfg(target_os = "windows")]
    {
        use std::os::windows::process::CommandExt;
        cmd = cmd.creation_flags(0x08000000); // CREATE_NO_WINDOW

        // Claude Code on Windows 需要 git-bash，自动检测并注入环境变量
        if let Some(bash_path) = find_git_bash_path() {
            cmd = cmd.env("CLAUDE_CODE_GIT_BASH_PATH", &bash_path);
        }
    }

    let mut child = cmd.spawn().map_err(|e| format!("启动 Claude 失败: {}", e))?;

    // 取出 stdout / stderr 管道，存入子进程句柄
    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "无法获取 stdout".to_string())?;
    let stderr = child
        .stderr
        .take()
        .ok_or_else(|| "无法获取 stderr".to_string())?;

    *state.child.lock().map_err(|e| format!("状态锁冲突: {}", e))? = Some(child);

    // 收集 stderr 错误信息
    let stderr_lines = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
    let stderr_collector = stderr_lines.clone();

    // --- 后台线程 1: 读取 stdout (stream-json 事件) ---
    let app_stdout = app.clone();
    std::thread::spawn(move || {
        let reader = BufReader::new(stdout);
        for line in reader.lines() {
            match line {
                Ok(text) => {
                    let trimmed = text.trim().to_string();
                    if trimmed.is_empty() {
                        continue;
                    }
                    let _ = app_stdout.emit(
                        "claude-line",
                        ClaudeLineEvent {
                            line: trimmed,
                            is_error: false,
                        },
                    );
                }
                Err(e) => {
                    let _ = app_stdout.emit(
                        "claude-line",
                        ClaudeLineEvent {
                            line: format!("读取 stdout 错误: {}", e),
                            is_error: true,
                        },
                    );
                    break;
                }
            }
        }
    });

    // --- 后台线程 2: 读取 stderr (日志/调试信息) ---
    let app_stderr = app.clone();
    std::thread::spawn(move || {
        let reader = BufReader::new(stderr);
        for line in reader.lines() {
            if let Ok(text) = line {
                let trimmed = text.trim().to_string();
                if trimmed.is_empty() {
                    continue;
                }
                stderr_collector.lock().unwrap().push(trimmed.clone());
                let _ = app_stderr.emit(
                    "claude-line",
                    ClaudeLineEvent {
                        line: trimmed,
                        is_error: true,
                    },
                );
            }
        }
    });

    // --- 后台线程 3: 等待进程退出，通知前端完成 ---
    std::thread::spawn(move || {
        // 等待一小段时间让第一个线程开始读取
        std::thread::sleep(std::time::Duration::from_millis(100));

        // 等待子进程退出
        let exit_status = {
            let state_guard = app.state::<ClaudeState>();
            let mut guard = state_guard.child.lock().unwrap();
            if let Some(ref mut child) = *guard {
                child.wait().ok()
            } else {
                None
            }
        };

        // 清除子进程引用
        {
            let state_guard = app.state::<ClaudeState>();
            let mut guard = state_guard.child.lock().unwrap();
            *guard = None;
        }

        // 收集 stderr 错误信息（如果进程失败了）
        let collected_stderr = stderr_lines.lock().unwrap().join("\n");
        let err_msg = if exit_status.map(|s| s.success()).unwrap_or(false) {
            None
        } else {
            let base = format!("Claude 进程退出代码: {:?}", exit_status.map(|s| s.code().unwrap_or(-1)));
            if collected_stderr.is_empty() {
                Some(base)
            } else {
                Some(format!("{}\n{}", base, collected_stderr))
            }
        };

        let _ = app.emit(
            "claude-done",
            ClaudeDoneEvent {
                success: exit_status.map(|s| s.success()).unwrap_or(false),
                error: err_msg,
            },
        );
    });

    Ok(())
}

/**
 * 取消当前运行的 Claude 进程
 */
#[tauri::command]
pub async fn cancel_claude(state: State<'_, ClaudeState>) -> Result<(), String> {
    let mut guard = state.child.lock().map_err(|e| format!("状态锁冲突: {}", e))?;
    if let Some(ref mut child) = *guard {
        let _ = child.kill();
        let _ = child.wait();
        *guard = None;
        Ok(())
    } else {
        Err("没有正在运行的 Claude 进程".to_string())
    }
}
