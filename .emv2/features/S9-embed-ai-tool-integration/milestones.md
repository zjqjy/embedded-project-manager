# embed-ai-tool 整合 - 子流程拆分（重编号版）

## 讨论ID
`20260420-embed-ai-tool-integration`

## 变更记录
原 S7 讨论时 S7 尚未被占用（当时 GUI 项目仍为 S7），现 S7 已分配给 GUI 桌面应用，
因此整合子步骤从 S9 开始编号。

## 子流程拆分

### S9-A: 工具初始化与权限配置
- **开发内容**: initem.md 新增 embed-ai-tool 工具路径自动探测/注册流程，扩展 permissions
- **前置条件**: 无
- **验证方式**: 运行 `python EM-SKILL/commands/scripts/detect_tools.py` 自动探测并注册工具路径

### S9-B: build-keil 集成
- **开发内容**: verify.md 新增编译验证指令，调用 keil_builder.py
- **前置条件**: S9-A 完成（确保 UV4 路径已注册）
- **验证方式**: `/em verify s9` 时 AI 调用 keil_builder.py 编译固件

### S9-C: flash-openocd 集成
- **开发内容**: verify.md 新增烧录验证指令，修复 openocd_flasher.py 硬编码 bug
- **前置条件**: S9-B 完成
- **验证方式**: 手动执行烧录验证，确认 openocd_flasher 能正确使用配置路径

### S9-D: serial-monitor 策略确认
- **开发内容**: 确认串口监控使用 EM 自带的 S5 工具，不整合 embed-ai-tool serial-monitor
- **前置条件**: 无
- **验证方式**: verify.md 注明串口策略

### S9-E: HVR 工作流更新
- **开发内容**: hvr-workflow.md 更新流程图和 HVR 模板，新增 AI 技能执行记录区段
- **前置条件**: S9-B/C 完成
- **验证方式**: 生成的 HVR 文件中包含技能调用记录

### S9-F: 全流程验证与元数据更新
- **开发内容**: 更新 project-spec.md / memory-log.md，验证编译+烧录+串口完整流程
- **前置条件**: S9-E 完成
- **验证方式**: 完整执行一次 build→flash→serial 验证流程

## 进度
- [ ] S9-A
- [ ] S9-B
- [ ] S9-C
- [ ] S9-D
- [ ] S9-E
- [ ] S9-F
