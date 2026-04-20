# embed-ai-tool 整合 - 子流程拆分

## 讨论ID
`20260420-embed-ai-tool-integration`

## 子流程拆分

### S7-A: 技能分类菜单开发
- **开发内容**: 实现交互式技能选择菜单
- **前置条件**: 无
- **验证方式**: `/em` 显示技能类别菜单
- **优先级**: 1

### S7-B: build 类技能整合
- **开发内容**: 整合 build-keil, build-cmake, build-iar, build-platformio
- **前置条件**: S7-A 完成
- **验证方式**: 成功编译示例工程
- **优先级**: 2

### S7-C: flash 类技能整合
- **开发内容**: 整合 flash-keil, flash-openocd, flash-platformio
- **前置条件**: S7-B 完成
- **验证方式**: 成功烧录示例固件
- **优先级**: 3

### S7-D: debug 类技能整合
- **开发内容**: 整合 debug-gdb-openocd, debug-platformio
- **前置条件**: S7-C 完成
- **验证方式**: 成功进入调试状态
- **优先级**: 4

### S7-E: 协议调试类技能整合
- **开发内容**: 整合 serial-monitor, can-debug, modbus-debug, visa-debug
- **前置条件**: S7-D 完成
- **验证方式**: 成功监控串口/CAN/Modbus
- **优先级**: 5

### S7-F: workflow 流水线整合
- **开发内容**: 整合 workflow 流水线编排
- **前置条件**: S7-E 完成
- **验证方式**: 成功执行 build-flash-monitor 流水线
- **优先级**: 6

## 进度
- [ ] S7-A
- [ ] S7-B
- [ ] S7-C
- [ ] S7-D
- [ ] S7-E
- [ ] S7-F
