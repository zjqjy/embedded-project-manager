# embed-ai-tool 整合 - 开发任务

## 讨论ID
`20260420-embed-ai-tool-integration`

## 最终方案
**协作分工**
- EM = 流程控制（verify 命令）
- embed-ai-tool = 具体执行（编译/烧录/监控/调试）

## 开发任务

### 任务1: 更新 verify.md 添加 embed-ai-tool 调用说明

**文件**: `C:\Users\23393\.claude\skills\EM-SKILL\commands\verify.md`

**修改内容**:
1. 添加 embed-ai-tool 技能调用说明
2. 添加技能对照表（验证场景 → 调用技能）
3. 添加调用流程说明

**embed-ai-tool 技能对照表**:

| 验证场景 | 调用技能 |
|----------|----------|
| 编译验证 | build-keil / build-cmake / build-platformio |
| 烧录验证 | flash-openocd / flash-keil / flash-platformio |
| 串口监控 | serial-monitor |
| CAN调试 | can-debug |
| Modbus调试 | modbus-debug |
| 完整流程 | workflow |

### 任务2: 更新 hvr-workflow.md

**文件**: `C:\Users\23393\.claude\skills\EM-SKILL\workflows\hvr-workflow.md`

**修改内容**:
1. 在 HVR 模板中添加 embed-ai-tool 技能声明
2. 说明 AI 在验证时应调用合适的技能

### 任务3: 验证整合效果

**验证步骤**:
1. `/em verify s4` - 测试芯片学习流程
2. AI 应自动调用 flash-openocd + serial-monitor
3. 检查 HVR 文件是否正确记录

## 状态
- [ ] 任务1: 更新 verify.md
- [ ] 任务2: 更新 hvr-workflow.md
- [ ] 任务3: 验证整合效果

## 讨论日期
2026-04-20
