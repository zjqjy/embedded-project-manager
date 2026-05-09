# embed-ai-tool 整合 - 硬件对齐

## 讨论ID
`20260420-embed-ai-tool-integration`

## 硬件相关性
本整合为纯软件任务，不涉及直接硬件操作。

各技能脚本调用的硬件：
- **build**: 无硬件依赖（纯编译）
- **flash**: J-Link / ST-Link / CMSIS-DAP 调试器
- **debug**: 同上 + GDB
- **serial**: USB 串口（CH340/CP210x/虚拟串口）
- **can**: USB-CAN 适配器（PCAN/KVASER/SLCAN）
- **modbus**: RS485/TCP 转换器
- **workflow**: 组合上述工具

## 工具依赖清单
- Keil MDK (UV4.exe) - Windows
- IAR Embedded Workbench - Windows
- CMake / Ninja
- PlatformIO CLI
- OpenOCD
- pyserial
- python-can
- pymodbus
- pyvisa

## 配置文件
使用 embed-ai-tool 的 `scripts/em_config.py` 管理工具路径。
