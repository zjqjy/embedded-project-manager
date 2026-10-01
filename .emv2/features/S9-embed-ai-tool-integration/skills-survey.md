# embed-ai-tool 技能调查记录

## 目的
逐个试用 embed-ai-tool 各技能，记录每个技能的输入要求、环境依赖、权限需求和输出结果，为 S9 整合提供依据。

## 调查记录

---

### 技能1: build-keil — Keil MDK 命令行编译

#### 测试时间
2026-04-29

#### 测试项目
`D:\DeskTop\GD32\OTA\GD32F407OTA\USER\OTA.uvprojx` (GD32F407VE)

#### 输入要求

| 参数 | 说明 | 示例 |
|------|------|------|
| `--project` | .uvprojx/.uvproj 工程文件路径 | `D:\...\OTA.uvprojx` |
| `--target` | 构建目标名称（可选，默认第一个） | `OtaProject` |
| `--uv4` | UV4.exe 路径（可选，自动探测失败时） | `D:\ZouJinQiang\App\MDK\UV4\UV4.exe` |
| `--rebuild` | 重新编译（clean+build） | 可选 |
| `--log` | 编译日志输出路径 | 可选 |
| `--verbose` | 输出详细日志 | 可选 |
| 工作区路径 | 或用 `--scan` 自动扫描 | 可选 |

#### 自动探测能力
- ✅ 扫描常见 Keil MDK 安装路径
- ✅ 检查环境变量 `KEIL_ROOT`、`MDK_ROOT`
- ✅ 查找 UV4.exe、ARMCC、ARMCLANG

#### 环境依赖（本机探测结果）

| 工具 | 路径 | 来源 |
|------|------|------|
| UV4.exe | `D:\ZouJinQiang\App\MDK\UV4\UV4.exe` | 自动探测失败，需手动指定 |
| ARMCC | `D:\ZouJinQiang\App\MDK\ARM\ARMCC\bin\armcc.exe` | 自动探测失败，需手动指定 |
| ARMCLANG | `D:\ZouJinQiang\App\MDK\ARM\ARMCLANG\bin\armclang.exe` | 自动探测失败，需手动指定 |

> **注**: 本机 Keil 安装在 `D:\ZouJinQiang\App\MDK`（非标准路径），自动探测无法发现，需通过 `--uv4` 显式传入。

#### 权限需求

| 操作 | 需要权限 |
|------|----------|
| 扫描工程文件 | `Glob`, `Read` |
| 执行 UV4.exe | `Bash(D:\ZouJinQiang\App\MDK\UV4\UV4.exe *)` |
| 读取编译日志 | `Read` |
| 访问输出目录 | `Read`, `Glob` |

#### 脚本调用方式
```bash
python skills/build-keil/scripts/keil_builder.py \
  --project <工程文件> \
  --target <目标名> \
  --uv4 <UV4路径>
```

#### 输出结果

| 字段 | 说明 |
|------|------|
| 状态 | success / failure |
| 错误数 / 警告数 | 整数 |
| 芯片型号 | 如 GD32F407VE |
| 工具链 | ARMCC / ARMCLANG |
| 固件大小 | Code / RO / RW / ZI + Flash/RAM 汇总 |
| 产物列表 | AXF(ELF) > HEX > BIN，含大小 |
| 编译耗时 | HH:MM:SS |
| 失败分类 | environment-missing / project-config-error / artifact-missing / ambiguous-context |

输出示例（success）：
```
✅ 编译成功
  工程: OTA.uvprojx → 目标: OtaProject
  芯片: GD32F407VE | 工具链: ARMCC
  固件大小: Flash ≈ 8.8 KB  RAM ≈ 5.4 KB
  产物: OTA.axf (126.2 KB), OTA.hex (24.8 KB)
  编译耗时: 00:00:01
```

输出示例（failure）：
```
❌ 编译失败
  错误: 1  警告: 1
  ..\HW\Source\iic.c(11): error: #20: identifier "GPIO_PUPD_PULL_UP" is undefined
  失败分类: project-config-error
```

#### 产出物
- `.axf` (ELF) 文件 — 首选调试/烧录格式
- `.hex` 文件 — 备用烧录格式
- 编译日志

#### 整合建议
- 需要提前通过配置或环境变量注册 UV4.exe 路径（否则在非标准路径下会失败）
- 推荐单次调用 `--detect --project --target` 减少进程启动开销
- 输出结果可直接喂给下游 flash 技能

---

### 技能2: flash-openocd — OpenOCD 烧录

#### 测试时间
2026-04-29

#### 测试项目
`D:\DeskTop\GD32\OTA\GD32F407OTA\OBJ\OTA.axf` (GD32F407VE, ELF, 126.2 KB)

#### 输入要求

| 参数 | 说明 | 示例 |
|------|------|------|
| `--artifact` | 固件产物路径（ELF/HEX/BIN） | `D:\...\OTA.axf` |
| `--interface` | 调试接口类型 | `stlink` / `cmsis-dap` / `jlink` |
| `--target` | OpenOCD 目标配置文件 | `target/stm32f4x.cfg` |
| `--config` | 额外 OpenOCD 配置（可重复） | 可选 |
| `--base-address` | BIN 文件烧录基地址 | `0x08000000` |
| `--no-verify` | 跳过校验 | 可选 |
| `--no-reset` | 不复位 | 可选 |
| `--scan-configs` | 扫描工作区配置线索 | 可选 |

#### 自动探测能力
- ✅ OpenOCD 版本检测（配置 + PATH + 常见安装路径）
- ✅ 自动扫描已连接探针（ST-Link/CMSIS-DAP/J-Link）
- ✅ 工作区 OpenOCD 配置扫描
- ❌ `build_flash_command()` 硬编码 `"openocd"`，未使用 `tool_config.py` 配置路径（bug）

#### 环境依赖（本机探测结果）

| 工具 | 路径 | 状态 |
|------|------|------|
| OpenOCD | `D:\OpenOCD\xpack-openocd-0.12.0-7\bin\openocd.exe` | ✅ 已安装（需加 PATH） |
| ST-Link V2 | USB 连接 | ✅ 已连接，2.86V，Cortex-M4 |
| J-Link V640 | `C:\Program Files (x86)\SEGGER\JLink_V640\JLink.exe` | ✅ 已安装（未连接） |

#### 权限需求

| 操作 | 需要权限 |
|------|----------|
| 执行 openocd | `Bash(D:\OpenOCD\...\bin\openocd.exe *)` |
| USB 访问调试器 | 系统驱动（ST-Link 驱动） |
| 访问固件产物 | `Read` |
| 扫描 OpenOCD 配置 | `Glob`, `Read` |

#### 脚本调用方式
```bash
python skills/flash-openocd/scripts/openocd_flasher.py \
  --artifact <产物路径> \
  --interface stlink \
  --target target/stm32f4x.cfg
```

#### 输出结果

| 字段 | 说明 |
|------|------|
| 状态 | success / failure |
| 调试接口 | stlink / jlink / cmsis-dap |
| 目标配置 | target/stm32f4x.cfg |
| 校验状态 | verified / skipped |
| 复位状态 | reset / no-reset |
| 失败分类 | environment-missing / connection-failure / project-config-error / target-response-abnormal / ambiguous-context |

输出示例（success）：
```
✅ 烧录成功，校验通过
  STLINK V2J37S7 → GD32F407VE (Cortex-M4)
  固件: OTA.axf (126.2 KB)
  校验: ✅  复位: ✅
```

输出示例（failure）：
```
❌ 烧录失败
  失败分类: connection-failure
  未找到 openocd 命令（PATH 中无 openocd，且脚本未使用配置路径）
```

#### 注意事项
- `build_flash_command()` 函数硬编码 `"openocd"` 为命令名，需将 OpenOCD 加入 `PATH` 或在整合时修复此问题
- GD32F407 与 STM32F4 引脚兼容，用 `target/stm32f4x.cfg` 即可
- 探测时正常读 `tool_config.py`，但烧录时不读——这是一个不一致点

#### 整合建议
- 整合时需要确保 OpenOCD 在 PATH 中，或修复脚本硬编码问题
- ST-Link 和 J-Link 共用同一套 OpenOCD 流程，只需切换 `--interface` 参数
- 烧录成功后可直接接 `serial-monitor` 查看串口输出

---

### 技能3: serial-monitor — 串口监控与日志分析

#### 测试时间
2026-04-29

#### 测试项目
GD32F407VE OTA 开发板，USART1 (PA9/PA10)，115200 baud

#### 输入要求

| 参数 | 说明 | 示例 |
|------|------|------|
| `--port` | 串口号 | `COM14` |
| `--baud` | 波特率（默认 115200） | `115200` |
| `--duration` | 读取时长（秒） | `10` |
| `--clear` | 读取前清空缓冲区 | 可选 |
| `--wait` | 等待指定字符串 | `"System Start"` |
| `--monitor` | 持续监视（Ctrl+C 退出） | 可选 |
| `--save` | 保存日志到文件 | 可选 |
| `--timestamp` | 每行加时间戳 | 可选 |
| `--wait-reset` | 先监听，等待复位后抓取 | 可选 |
| `--auto-reset` | 通过 OpenOCD 自动复位 | 需 `--interface` + `--openocd-target` |

#### 自动探测能力
- ✅ 自动列出可用串口
- ✅ 自动选择常见串口设备（CH340/CP210x/ST-Link VCP）
- ✅ 日志基础分析（行数统计、关键词检测）
- ❌ `--list` 和 `--auto` 在无串口时返回"未找到"，信息不够明确

#### 环境依赖（本机探测结果）

| 工具 | 路径 | 状态 |
|------|------|------|
| pyserial | 系统 Python 包 | ✅ 已安装 |
| 串口适配器 | COM14 | ✅ 已连接 |
| ST-Link | USB 连接 | ✅ 用于 `--auto-reset` |

#### 权限需求

| 操作 | 需要权限 |
|------|----------|
| 打开串口 | 系统权限（Windows 一般无需额外配置） |
| 读取串口数据 | 系统权限 |
| 保存日志 | `Write` |
| 自动复位 | 同 flash-openocd 权限 |

#### 脚本调用方式

基本监控：
```bash
python skills/serial-monitor/scripts/serial_monitor.py \
  --port COM14 --baud 115200 --duration 10 --clear --verbose
```

捕获启动日志（自动复位）：
```bash
python skills/serial-monitor/scripts/serial_monitor.py \
  --port COM14 --baud 115200 \
  --wait-reset --auto-reset \
  --interface stlink --openocd-target target/stm32f4x.cfg \
  --duration 15 --save startup.log
```

#### 输出结果

| 字段 | 说明 |
|------|------|
| 串口/波特率 | 如 COM14 @ 115200 |
| 总行数 | 接收到的行数 |
| 关键词统计 | 如 Heartbeat: 12 |
| 健康状态 | ✅ 正常 / ⚠️ 未识别 / ❌ 检测到错误 |
| 日志文件 | 可选保存路径 |

#### 输出示例
```
✅ 串口日志看起来正常（共 531 行）
  总行数: 531  心跳: 12
  首行: OTA System Start!
```

#### 注意事项
- `--auto-reset` 需要 OpenOCD 在 PATH 中（同 flash-openocd 的硬编码问题）
- `--auto` 自动串口选择在多个串口时可能选错，建议固定 `--port`
- 波特率默认 115200，不匹配时会收乱码或空数据

#### 整合建议
- 通常与 flash-openocd 串联使用：烧录 → `--wait-reset --auto-reset` 看启动日志
- 日志可保存到 `.emv2/logs/` 目录下
- 波特率配置应该在整合层指定，避免每次手动输入

