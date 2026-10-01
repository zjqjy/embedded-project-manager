# embed-ai-tool 整合 - 需求确认

## 讨论ID
`20260420-embed-ai-tool-integration`

## 整合目标
在 EM 的 verify 流程中调用 embed-ai-tool 技能执行实际操作

## 整合方案

### 最终方案
**协作分工**
- EM = 流程控制（verify 命令）
- embed-ai-tool = 具体执行（编译/烧录/监控）

### 整合点

| EM 阶段 | 调用 embed-ai-tool 技能 |
|---------|------------------------|
| S4 芯片学习 | flash-openocd + serial-monitor |
| S5 串口调试 | serial-monitor |

### 实现方式

在 verify 流程中：
1. EM 生成 HVR 文件
2. EM 调用 embed-ai-tool 脚本执行实际操作
3. AI 分析结果
4. EM 记录验证结果

### 命令示例

```
/em verify s4
    ↓
EM: 生成 HVR → 调用 flash-openocd 烧录 → 调用 serial-monitor 监控
    ↓
AI: 分析日志 → 记录结果
    ↓
EM: 更新项目状态
```

## 待确认
（无）

## 涉及文件
- `.emv2/discussion/20260420-embed-ai-tool-integration/`
