# 命令: /em verify (准备验证)

## 功能
生成人工验证请求 (HVR)，并启动S5串口工具

## 触发
```
/em verify s<编号>    # 如 /em verify s7
```

**步骤参数使用 new 命令分配的 S 编号**（如 S7），详见 new.md。

## 执行流程

1. 读取项目当前步骤
2. 🔄 **更新状态**：当前子步骤 🚧 开发中 → 🔄 验证中
3. 🔄 **更新 Meta**：当前步骤: S7-A(验证中)
4. 生成 HVR 文件（增强版）
5. 保存到 `.emv2/checkpoints/HVR-<步骤>-<序号>.md`
6. 启动S5串口工具
7. 输出验证清单

## HVR 文件

- 生成到 `.emv2/checkpoints/HVR-<步骤>-<序号>.md`
- HVR 模板和工作流细则详见 `workflows/hvr-workflow.md`

## S5工具启动（串口调试）

```bash
# 传入项目路径和步骤参数，确保日志保存到 .emv2/logs/
start "" "EM-SKILL\tools\serial-mcp\start.bat" "%CD%" "S9"
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

## 相关文件
- workflows/hvr-workflow.md - HVR工作流细则（含模板和流程图）
