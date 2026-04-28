# 问题追踪

## 当前问题

### [2026-04-28] S7-C Claude Code桥接验证失败：Windows环境兼容性
- **状态**: open
- **步骤**: S7-C — Claude Code 桥接（Rust后端）
- **发现时间**: 2026-04-28
- **描述**: GUI 中调用 Claude CLI 在 Windows 上存在多兼容性问题

### 问题详情

1. **AI未按技能流程执行**:
   - 用户要求"启动一下"，AI 未先启动 GUI，直接进入代码修改
   - 偏离了用户请求本意，浪费了用户时间

2. **Claude CLI 路径解析失败**:
   - Rust 的 `Command::new("claude")` 找不到 npm 安装的 `claude.cmd`
   - 第一次已修复：改为使用 `claude.cmd`

3. **claude.cmd 弹出控制台窗口**:
   - 批处理文件触发 cmd.exe 窗口
   - 第二次修复：改用 `node` + 直接调用 `cli.js` + `CREATE_NO_WINDOW`

4. **缺少 git-bash 环境**:
   - Claude Code on Windows 需要 git-bash
   - 第三次修复：添加 `find_git_bash_path()` 自动检测
   - 已检测到用户 git-bash 在 `D:\ZouJinQiang\App\Git\bin`

### 当前状态
- 已针对上述3个技术问题做了修复（claude.rs），但尚未验证修复是否生效
- 流程层面的 AI 不按指令执行问题需在讨论中解决

### 相关文件
- HVR文件: [.emv2/checkpoints/HVR-S7-001.md]
- Claude桥接代码: [EM-SKILL/tools/em-gui/src-tauri/src/claude.rs]

---

## 历史归档
<!-- 已闭环问题归档索引 -->

