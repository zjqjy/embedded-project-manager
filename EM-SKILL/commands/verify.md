# 命令: /em verify (准备验证)

## 功能
生成人工验证请求 (HVR)，并启动S5串口工具

## 触发
```
/em verify s<编号>    # 如 /em verify s7
```

**步骤参数使用 new 命令分配的 S 编号**（如 S7），详见 new.md。

## 执行流程

1. **【状态目录检测】** 调用 `get_state_dir()` 确定 `<STATE_DIR>`（S10-B 通用化）
2. 读取项目当前步骤
3. 🔄 **更新状态**：当前子步骤 🚧 开发中 → 🔄 验证中
4. 🔄 **更新 Meta**：当前步骤: S7-A(验证中)
5. 生成 HVR 文件（增强版）
6. 保存到 `<STATE_DIR>/checkpoints/HVR-<步骤>-<序号>.md`
7. 自动编译
9. 下载,默认stlink，探测作为参考，如果探测成功的下载失败，可以三个都试一遍下载
8. 启动串口工具，两个工具都要注意参数,要注意要采集完整信息，执行复位mcu时需要和下载成功的调试工具对应
10. 输出验证清单
11. 💡 **【提议 commit】**（S10-D 集成）见下方

## 提议 commit 流程（S10-D）

> **触发点**：HVR 验证流程完成（即第 10 步"输出验证清单"之后），
> 适用于"通过"和"失败"两种情况——失败时仍可提议 commit 暂存当前进度。

### AI 行为

HVR 文件生成、工具执行结果记录完成后，AI **不直接 commit**，而是输出"提议"：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 提议 commit  (S10-D Git 集成)
━━━━━━━━━━━━━━━━━━━━━━━━━━
建议 commit message:
  [S<step>] feat: verify <步骤描述> with HVR-<序号>

待提交文件:
  M  <STATE_DIR>/checkpoints/HVR-<步骤>-<序号>.md
  M  <STATE_DIR>/project-spec.md
  ?? <STATE_DIR>/logs/build_<步骤>_<时间>.log

确认提交？[y/n/edit]
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 用户响应

| 用户输入 | AI 行为 |
|----------|---------|
| `y` / `确认` | 执行 `git add` + `git commit -m "..."` |
| `n` / `取消` | 跳过本次 commit，保留到下次 |
| `edit` / `修改为: ...` | 用新 message 重新提议一次 |
| `amend` | 加入上一次 commit（需用户已 commit 过） |

### 执行约束

- ✅ 允许 `git status` / `git add` / `git commit -m "..."`（见 initem.md 白名单）
- ❌ **禁止** `git push`（无论用户如何要求，必须拒绝并提示手动 push）
- ❌ **禁止** `--no-verify` / `--force` 等破坏性选项
- ❌ **禁止** `git commit --amend` 改写历史（如需修改走"新 commit"）

### 提议规则

- **commit message 必须**以 `[S<n>]` 开头（EM 自定义规范，未配置默认 B 方案）
- **type** 推断依据：
  - 新增功能 / HVR 通过 → `feat`
  - 修复问题 → `fix`
  - 仅文档/HVR → `docs`
  - 仅日志文件 → 通常不打入 commit（`.gitignore` 过滤）
- **scope** 可选：`(scope)` 紧跟 type 后
- **subject** ≤ 50 字符，**body** 可选（解释 HVR 关键结论）

### 跳过条件

下列情况 AI 应**不**提议 commit（仅在用户主动要求时才提交）：

- 工作区无变更（`git status` 干净）
- 仅有日志/构建产物（应加入 `.gitignore`）
- 用户在 HVR 流程中明确说"暂不提交"

## HVR 文件

## HVR 文件

- 生成到 `<STATE_DIR>/checkpoints/HVR-<步骤>-<序号>.md`（实际路径由 `get_state_dir()` 解析）
- HVR 模板和工作流细则详见 `workflows/hvr-workflow.md`

## S5工具启动（串口调试）

```bash
# 使用 Python 直接启动，确保日志保存到 <STATE_DIR>/logs/
python EM-SKILL/tools/serial-mcp/serial_monitor.py --project "%CD%" --step "S9"
```

GUI程序启动后独立运行，AI继续其他工作。

**参数说明**：
- `%CD%` - 当前项目路径（自动获取）
- `S9` - 当前验证步骤（根据 /em verify s9 的参数）

## 编译验证（build-keil）

当验证步骤涉及固件编译时，AI 应调用 EM-SKILL 内置的 build-keil 工具。

### 调用方式

```bash
python EM-SKILL/tools/build-keil/scripts/keil_builder.py \
  --project <工程文件路径> \
  --target <目标名>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--project` | 扫描工作区中的 `.uvprojx`/`.uvproj` 文件 |
| `--target` | 使用工程中第一个 Target，或由用户指定 |
| UV4 路径 | 自动从 tool_config 读取（由 initem 注册） |

### 检测工程

AI 自动在工作区中查找 Keil 工程文件：

```bash
python -c "
from pathlib import Path
for p in Path('.').rglob('*.uvprojx'):
    print(p)
for p in Path('.').rglob('*.uvproj'):
    print(p)
"
```

### 结果处理

AI 从脚本 stdout 中提取以下字段记录到 HVR：

| 字段 | 作用 |
|------|------|
| 编译状态 | ✅ 成功 / ❌ 失败 |
| 错误数/警告数 | `错误: N  警告: N` |
| 固件大小 | `Flash ≈ N KB  RAM ≈ N KB` |
| 产物路径 | `产物: file.axf (N KB)` |

### 自动决策

**编译成功 → 自动进入烧录流程**（AI 连续执行，用户只需观察物理现象）

AI 按以下顺序连续执行：

1. **编译** → 成功则自动进入步骤 2
2. **烧录** → 成功则自动进入步骤 3
3. **串口** → 抓取启动日志，用户观察物理现象并口述结果

```
编译(AI执行) → 烧录(AI执行) → 串口监控(AI抓日志) → 用户口述观察结果
```

**编译失败** → 读取编译日志 → 分析错误 → 请求用户修复

**烧录失败** → 根据失败分类引导排查（connection-failure / target-response-abnormal / project-config-error）

## 烧录验证（flash-openocd）

当验证步骤涉及固件烧录时，AI 应调用 EM-SKILL 内置的 flash-openocd 工具。

### 先探测环境

```bash
python EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py --detect
```

确认 OpenOCD 可用且调试探针已连接。

### 调用方式

```bash
python EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py \
  --artifact <产物路径> \
  --interface stlink \
  --target target/stm32f4x.cfg
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--artifact` | 从 build-keil 的产物路径获取（AXF/ELF） |
| `--interface` | 从 `--detect` 探测结果获得（stlink/jlink/cmsis-dap） |
| `--target` | 根据芯片型号选择（GD32F407 → `target/stm32f4x.cfg`） |

### 结果处理

| 字段 | 检查要点 |
|------|----------|
| 烧录状态 | success / failure |
| 校验状态 | verified / skipped |
| 失败分类 | connection-failure / target-response-abnormal / project-config-error |

### 自动决策

- 烧录成功 → 提示下一步（串口观察启动日志）
- 烧录失败 → 根据失败分类引导排查

## 串口工具

EM-SKILL 内置两个串口工具：

| 工具 | 路径 | 用途 |
|------|------|------|
| S5 serial-mcp (GUI) | `EM-SKILL/tools/serial-mcp/` | 可视化串口监控（tkinter + MCP） |
| serial-monitor (CLI) | `EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py` | 脚本式串口抓取（定长/关键字/持续） |

S5 工具用于人工观察，serial-monitor 用于 AI 自动抓取日志。

### 避免错过启动消息

**关键：必须指定 OpenOCD 参数，否则复位会失败！**

如果需要在烧录后观察完整的启动日志，使用以下完整参数：

```bash
python EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py \
  --port COM5 \
  --baud 115200 \
  --duration 15 \
  --wait-reset \
  --auto-reset \
  --interface stlink \
  --openocd-config interface/stlink.cfg \
  --openocd-target target/stm32f4x.cfg \
  --save <STATE_DIR>/logs/serial_S9.log
```

**参数说明**：
| 参数 | 说明 |
|------|------|
| `--interface` | 必须与烧录时使用的接口一致 (stlink/jlink/cmsis-dap) |
| `--openocd-config` | OpenOCD 接口配置文件 |
| `--openocd-target` | OpenOCD 目标芯片配置文件 |

**工作流程**：
1. 打开串口，开始监听
2. OpenOCD 执行 `reset halt` 复位开发板
3. MCU 重启后输出完整启动日志
4. 捕获完整的启动日志并保存

**常见错误**：
- ❌ 不传 `--interface`：OpenOCD 自动选择错误接口，导致 `Unsupported transport`
- ❌ 不传 `--openocd-config`：配置文件路径不对，导致 `invalid command name`

## 相关文件
- workflows/hvr-workflow.md - HVR工作流细则（含模板和流程图）
