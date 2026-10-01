# 工作流: verify-embedded（嵌入式 verify 子流程）

> 由通用 `commands/verify.md` 在检测到 `project.json.type == "embedded"` 时加载。
> 通用项目不读此文件。
>
> **S17-B 起数据驱动**：三连不再硬编码具体工具，而是读
> `project.json.embedded`（initem 锁定的组合）查 `tools/registry.json` 路由到 adapter。
> 新增芯片/工具只改 registry，本文件不随工具增长而修改。

## 子流程总览

```
通用 verify 流程
   │
   ├─ 嵌入式注入：编译 → 烧录 → 串口（三连）
   │   │
   │   ├─ build adapter    （按 project.json.embedded.build 路由，如 keil / ccs）
   │   ├─ flash adapter    （按 project.json.embedded.flash 路由，如 openocd / dslite）
   │   └─ observe adapter  （serial，芯片无关；GUI 走 serial-mcp）
   │
   └─ 用户口述物理现象观察 → HVR 文件
```

**关键**：AI 连续自动执行三步，用户只需观察物理现象并口述结果。

## 第 0 步: 解析工具组合

1. 读 `project.json.embedded`：
   ```json
   { "vendor": "st", "family": "f4", "chip": "STM32F407VGT6",
     "build": "keil", "flash": "openocd",
     "flash_args": { "target_cfg": "target/stm32f4x.cfg", "interface": "stlink" } }
   ```
2. 无此配置（旧项目）→ 提示先 `/em initem` 锁定组合；或按 registry `chips.<vendor>.<family>` 现查默认值并请用户确认后**补写回** project.json
3. adapter 脚本路径 = `tools/` + `registry.json → adapters.<verb>.<name>.file`

> 以下三节以 Keil + OpenOCD 为示例展开；其他 adapter（ccs / dslite）参数以各脚本 `--help` 与 registry `args` 为准。

## 子流程 1: 编译（build adapter）

### 调用方式（keil 示例）

```bash
python <SKILL>/plugins/embedded/tools/adapters/build/keil.py \
  --project <工程文件路径> \
  --target <目标名>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--project` | 扫描工作区 `*.uvprojx`/`*.uvproj`（CCS 工程则扫 `.project`/`.ccsproject`） |
| `--target` | 工程中第一个 Target 或用户指定 |
| 工具路径 | 自动从 `tool_config`（initem 注册）读取 |

### 结果提取（写 HVR）

| 字段 | 含义 |
|------|------|
| 编译状态 | ✅ 成功 / ❌ 失败 |
| 错误数/警告数 | `错误: N  警告: N` |
| 固件大小 | `Flash ≈ N KB  RAM ≈ N KB` |
| 产物路径 | `产物: file.axf (N KB)` |

### 决策

- 成功 → **自动进入烧录**
- 失败 → 读编译日志 → 分析 → 请求用户修复

## 子流程 2: 烧录（flash adapter）

### 先探测环境

```bash
python <SKILL>/plugins/embedded/tools/adapters/flash/openocd.py --detect
```

### 调用方式（openocd 示例）

```bash
python <SKILL>/plugins/embedded/tools/adapters/flash/openocd.py \
  --artifact <产物路径> \
  --interface stlink \
  --target <project.json.embedded.flash_args.target_cfg>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--artifact` | 上一步 build 的产物路径 |
| `--interface` | `--detect` 探测结果（stlink/jlink/cmsis-dap） |
| `--target` | **registry / project.json.embedded.flash_args**（不再人工记 GD32F407→哪个 cfg） |

### 烧录策略

- 默认 stlink；探测作为参考
- 如探测成功的 interface 烧录失败 → 三种 interface 都试一遍
- 复位 MCU 时与烧录成功的 interface 对应
- **dslite（TI）**：参数走 `flash_args.ccxml`，产物类型按 CCS 输出（.out/.hex）

### 结果检查

| 字段 | 检查 |
|------|------|
| 烧录状态 | success / failure |
| 校验状态 | verified / skipped |
| 失败分类 | connection-failure / target-response-abnormal / project-config-error |

### 决策

- 成功 → **自动进入串口**
- 失败 → 按分类引导排查

## 子流程 3: 串口（observe/serial + serial-mcp）

### 工具选择

| 工具 | 用途 |
|------|------|
| `serial-mcp` (GUI) | 用户人工观察启动日志（图形化窗口） |
| `adapters/observe/serial` (CLI) | AI 自动抓取启动日志（写入 logs/） |

### 完整参数（避免错过启动消息）

```bash
python <SKILL>/plugins/embedded/tools/adapters/observe/serial.py \
  --port COM5 \
  --baud 115200 \
  --duration 15 \
  --wait-reset \
  --auto-reset \
  --interface stlink \
  --openocd-config interface/stlink.cfg \
  --openocd-target <flash_args.target_cfg> \
  --save <STATE_DIR>/logs/serial_S<N>.log
```

| 参数 | 说明 |
|------|------|
| `--interface` | 必须与烧录时使用的 interface 一致 |
| `--openocd-config` | 接口配置文件 |
| `--openocd-target` | 目标芯片配置文件（与烧录同一来源） |
| `--auto-reset` | 打开串口后用 OpenOCD 复位 MCU，避免错过启动 |
| `--baud` | registry `chips.<vendor>.<family>.observe.args.baud`（TI 串口常非 115200，按 registry） |

> **TI 注意**：C2000 的 SCI 串口烧录后复位行为与 STM32 不同，`--auto-reset` 不可用（无 OpenOCD）；
> 引导用户手动按复位 / 重新上电，或经 dslite `--reset` 后抓取。

### 工作流程

1. 打开串口监听
2. 复位 MCU（OpenOCD 项目自动；dslite 项目用户手动）
3. MCU 重启输出完整启动日志
4. 抓取并保存到 `logs/serial_S<N>_<timestamp>.log`

### 常见错误

- ❌ 不传 `--interface` → `Unsupported transport`
- ❌ 不传 `--openocd-config` → `invalid command name`

### GUI 启动（用户人工观察）

```bash
python <SKILL>/plugins/embedded/tools/serial-mcp/serial_monitor.py \
  --project "%CD%" --step "S<N>"
```

GUI 独立进程，AI 继续其他工作。

## HVR 字段（嵌入式扩展）

通用 verify 的 HVR 文件追加以下字段：

```markdown
## 嵌入式执行记录

| 步骤 | adapter | 结果 |
|------|---------|------|
| 编译 | <build，如 keil/ccs> | <成功/失败> + 产物路径 |
| 烧录 | <flash，如 openocd/dslite> | <成功/失败> + interface/探针 |
| 串口 | serial | <抓到启动日志/未抓到> |

### 物理现象（用户口述）
- <用户观察>
```

## 相关文件
- `tools/registry.json` — 能力矩阵（S17-B，单一事实来源）
- `plugins/embedded/PLUGIN.md` — 插件清单
- `commands/verify.md` — 通用 verify 入口
- `workflows/hvr-workflow.md` — HVR 模板与流程图
