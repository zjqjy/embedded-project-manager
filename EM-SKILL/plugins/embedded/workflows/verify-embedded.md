# 工作流: verify-embedded（嵌入式 verify 子流程）

> 由通用 `commands/verify.md` 在检测到 `project.json.type == "embedded"` 时加载。
> 通用项目不读此文件。

## 子流程总览

```
通用 verify 流程
   │
   ├─ 嵌入式注入：编译 → 烧录 → 串口（三连）
   │   │
   │   ├─ build-keil      （编译固件）
   │   ├─ flash-openocd   （烧录到芯片）
   │   └─ serial-monitor / serial-mcp （抓取启动日志）
   │
   └─ 用户口述物理现象观察 → HVR 文件
```

**关键**：AI 连续自动执行三步，用户只需观察物理现象并口述结果。

## 子流程 1: 编译（build-keil）

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/build-keil/scripts/keil_builder.py \
  --project <工程文件路径> \
  --target <目标名>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--project` | 扫描工作区 `*.uvprojx`/`*.uvproj` |
| `--target` | 工程中第一个 Target 或用户指定 |
| UV4 路径 | 自动从 `tool_config`（initem 注册）读取 |

### 检测工程

```bash
python -c "
from pathlib import Path
for p in Path('.').rglob('*.uvprojx'): print(p)
for p in Path('.').rglob('*.uvproj'):  print(p)
"
```

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

## 子流程 2: 烧录（flash-openocd）

### 先探测环境

```bash
python EM-SKILL/plugins/embedded/tools/flash-openocd/scripts/openocd_flasher.py --detect
```

确认 OpenOCD 可用 + 调试探针已连接。

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/flash-openocd/scripts/openocd_flasher.py \
  --artifact <产物路径> \
  --interface stlink \
  --target target/stm32f4x.cfg
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--artifact` | 上一步 build-keil 的产物路径 |
| `--interface` | `--detect` 探测结果（stlink/jlink/cmsis-dap） |
| `--target` | 根据芯片型号选择（GD32F407 → `target/stm32f4x.cfg`） |

### 烧录策略

- 默认 stlink；探测作为参考
- 如探测成功的 interface 烧录失败 → 三种 interface 都试一遍
- 复位 MCU 时与烧录成功的 interface 对应

### 结果检查

| 字段 | 检查 |
|------|------|
| 烧录状态 | success / failure |
| 校验状态 | verified / skipped |
| 失败分类 | connection-failure / target-response-abnormal / project-config-error |

### 决策

- 成功 → **自动进入串口**
- 失败 → 按分类引导排查

## 子流程 3: 串口（serial-monitor / serial-mcp）

### 工具选择

| 工具 | 用途 |
|------|------|
| `serial-mcp` (GUI) | 用户人工观察启动日志（图形化窗口） |
| `serial-monitor` (CLI) | AI 自动抓取启动日志（写入 logs/） |

### 完整参数（避免错过启动消息）

```bash
python EM-SKILL/plugins/embedded/tools/serial-monitor/scripts/serial_monitor.py \
  --port COM5 \
  --baud 115200 \
  --duration 15 \
  --wait-reset \
  --auto-reset \
  --interface stlink \
  --openocd-config interface/stlink.cfg \
  --openocd-target target/stm32f4x.cfg \
  --save <STATE_DIR>/logs/serial_S<N>.log
```

| 参数 | 说明 |
|------|------|
| `--interface` | 必须与烧录时使用的 interface 一致 |
| `--openocd-config` | 接口配置文件 |
| `--openocd-target` | 目标芯片配置文件 |
| `--auto-reset` | 打开串口后用 OpenOCD 复位 MCU，避免错过启动 |

### 工作流程

1. 打开串口监听
2. OpenOCD `reset halt` 复位
3. MCU 重启输出完整启动日志
4. 抓取并保存到 `logs/serial_S<N>_<timestamp>.log`

### 常见错误

- ❌ 不传 `--interface` → `Unsupported transport`
- ❌ 不传 `--openocd-config` → `invalid command name`

### GUI 启动（用户人工观察）

```bash
python EM-SKILL/plugins/embedded/tools/serial-mcp/serial_monitor.py \
  --project "%CD%" --step "S<N>"
```

GUI 独立进程，AI 继续其他工作。

## HVR 字段（嵌入式扩展）

通用 verify 的 HVR 文件追加以下字段：

```markdown
## 嵌入式执行记录

| 步骤 | 工具 | 结果 |
|------|------|------|
| 编译 | build-keil | <成功/失败> + 产物路径 |
| 烧录 | flash-openocd | <成功/失败> + interface |
| 串口 | serial-monitor | <抓到启动日志/未抓到> |

### 物理现象（用户口述）
- <用户观察>
```

## 相关文件
- `plugins/embedded/PLUGIN.md` — 插件清单
- `commands/verify.md` — 通用 verify 入口
- `workflows/hvr-workflow.md` — HVR 模板与流程图
