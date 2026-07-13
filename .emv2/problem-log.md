# 问题追踪

## 当前问题

### [2026-06-03] EM new 中档流程的过度设计倾向

- **状态**: open
- **触发场景**: 在 `presser_foot` 项目跑 S10 切针位重算功能，AI 跳出"用户只想要缓存几个数 + 切针位再调一次"这种**小需求**，把简单需求包装成 3 档方案 + brainstorm + milestones + decisions + state.md 全套
- **根因分析**:
  1. new 中档 workflow 的"3 候选方案"是**重档讨论的残留**——对 2-3 行代码的修改不该套这个流程
  2. AI 把"proposal 给你审"误读为"提案完直接落盘"——流程要求 `✅继续` 才写文件，但 AI 跳过确认直接 Write brainstorm.md
  3. milestones 阶段额外引入"`_raw` 字段 + 抽内部函数"等自创概念，**用户原话："脱裤子放屁"**
- **修复方向（待讨论）**:
  1. **轻档判定要更激进**：判定标准加 "改动 ≤ 10 行 + 单文件 + 无新概念 → 强制 light"
  2. **中档 brainwrite 必须等人确认**：`Write brainstorm.md` 前 AI 应该 `AskUserQuestion` 列方案，**不**直接落盘
  3. **轻档流程简化**：brainstorm.md 可省，milestones.md 可省，**只**写 quick-plan.md 一页纸（甚至直接动手改代码）
  4. **AI 自检问句**：落盘 brainstorm 之前 AI 自问"如果用户只看一句话，能不能直接动手？" 是 → 走轻档
- **相关**: 用户的原话记录——"你搞那么多乱七八糟的名词干什么" / "不就一个缓存 + 重调"
- **下一步**: 用户决定是否要把这个作为新步骤（建议 S12-S13）正式修复 EM 流程；或仅作为 reference 留待后续

---

### [2026-04-30] S9-F 全流程验证 - ✅ 通过
- **状态**: closed
- **步骤**: S9-F — embed-ai-tool 整合全流程验证
- **验证时间**: 2026-04-30
- **验证方式**: OTA 项目实际烧录验证
- **结论**: 编译→烧录→串口全流程验证通过

### [2026-04-30] S11 串口监控 + initem 优化（原 S10 顺延）
- **状态**: open
- **描述**: 串口监控错过消息、GIT启动、initem 需包含 OpenOCD 下载
- **编号变更说明**: 原计划分配 S10，2026-06-02 启动 S10 标准化+通用化+Git集成项目后顺延为 S11

#### 问题清单

**P1-9: 串口监控错过启动消息**
- **现象**: 验证流程：编译→烧录→打开串口监控，但打开串口时已错过很多启动消息
- **需求**: 打开串口后能自动重启开发板
- **修复方向**: serial-monitor 有 `--auto-reset` 参数，烧录后自动复位开发板

**P1-10: serial-mcp GUI 启动方式错误**
- **现象**: 有 GUI 的 serial-mcp 用 Windows `start` 命令打开
- **需求**: 应该直接用 Python 运行 `.py` 程序
- **修复方向**: verify.md 中改为 `python serial_monitor.py` 而不是 `start "" bat`

**P1-11: initem 需包含 OpenOCD 下载**
- **现象**: initem 没有强制要求下载 OpenOCD
- **需求**: OpenOCD 是必须下载的工具
- **修复方向**: initem.md 增加 OpenOCD 下载指引

### 问题清单

**✅ P0-1: openocd_flasher --detect 探针检测不准确** (已修复 2026-04-30)
- **现象**: `--detect` 不加 `--interface` 时找不到已连接的 ST-Link
- **根因**: `detect_probes()` 用 `shutil.which("openocd")` 而不是配置路径
- **修复**: 新增 `_get_openocd_executable()` 函数，优先使用配置路径，timeout 4s→8s
- **文件**: `EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py`

**✅ P0-2: serial-monitor --auto-reset 找不到 openocd** (已修复 2026-04-30)
- **现象**: `--auto-reset` 时报 `❌ 未找到 OpenOCD`
- **根因**: `serial_monitor.py` 用 `shutil.which("openocd")` 找 openocd，但用户只通过 `tool_config` 注册了路径
- **修复**: 引入 tool_config，添加 `_get_openocd_executable()` 函数
- **文件**: `EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py`

**✅ P1-2: verify 流程编译后就结束，未自动进入烧录** (已修复 2026-04-30)
- **现象**: 编译通过后流程就结束，没有自动进入烧录环节
- **修复**: 更新 `verify.md`，明确 AI 自动连续执行 编译→烧录→串口 三步
- **文件**: `EM-SKILL/commands/verify.md`

**✅ P1: serial-monitor 日志未关联 EM 体系** (已修复 2026-04-30)
- **现象**: `--save` 保存的日志路径和 EM 的 `.emv2/logs/` 没有关联
- **修复**: serial_monitor.py 新增 `--step` 参数和自动检测 `.emv2/logs/` 功能
- **文件**: `EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py`

**✅ P2: 权限弹窗过多** (已修复 2026-04-30)
- **现象**: 验证过程中 Claude Code 频繁弹出权限确认
- **修复**: 更新 initem.md，添加精确路径白名单配置
- **文件**: `EM-SKILL/commands/initem.md`

**✅ P1-3: openocd_flasher J-Link 烧录后程序不运行** (已修复 2026-04-30)
- **现象**: 使用 J-Link 烧录后，程序不自动运行，需要手动复位
- **修复**: J-Link 使用特殊命令 `init; halt; program ...; reset run; exit`
- **文件**: `EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py`

**✅ P1-4: openocd_flasher 需要支持部分擦除（保留 bootloader）** (已修复 2026-04-30)
- **现象**: 有 bootloader 的项目不希望全部擦除
- **修复**: 移除错误的 `erase` 参数（OpenOCD 不支持），直接使用 `program` 命令会自动处理擦除
- **文件**: `EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py`

**✅ P1-8: openocd_flasher OpenOCD 命令格式错误** (已修复 2026-04-30)
- **现象**: 烧录时报 `Error: Invalid command argument`
- **根因**: 我错误理解了 OpenOCD program 命令格式
- **修复**: 修正命令格式为 `program <file> [verify] [reset]`，参数用空格分隔
- **文件**: `EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py`

**✅ P1-5: S5 GUI 启动缺少步骤和路径参数** (已修复 2026-04-30)
- **现象**: 启动 `start.bat` 时没有传入项目路径和步骤参数
- **修复**: 更新 `verify.md`，启动时传入 `%CD%` 和 `S9` 参数
- **文件**: `EM-SKILL/commands/verify.md`

**✅ P1-6: logs 目录需要包含当前调试的简短信息** (已修复 2026-04-30)
- **现象**: 日志文件只有步骤信息，缺少当前在调功能的描述
- **修复**: serial_monitor.py 日志命名改为 `serial_<步骤>_<时间戳>.log`
- **文件**: `EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py`

**✅ P1-7: 两个串口工具的日志需要统一** (已修复 2026-04-30)
- **现象**: S5 GUI 和 CLI serial-monitor 两个工具的日志保存方式不一致
- **修复**: CLI serial-monitor 自动检测 `.emv2/logs/` 并使用相同目录
- **文件**: `EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py`

### 相关文件
- HVR文件: [.emv2/checkpoints/HVR-S9-F-001.md]

---

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

