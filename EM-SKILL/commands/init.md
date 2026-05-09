# 命令: /em init (项目初始化)

## 功能
从零开始新项目

## 触发
```
/em init <项目名称>
```

## 执行流程

1. **【芯片选择】**（支持 chips.json 中的已学习芯片）
2. **询问开发环境**（Keil/IAR/GCC）
3. **芯片学习**：用户选择/输入的芯片自动添加到全局 chips.json
4. **创建 .emv2/ 目录结构**
5. **创建 .emv2/project-spec.md**
6. **创建 .emv2/memory-log.md**
7. **创建 CLAUDE.md**（如果不存在）
   - 写入工具使用说明索引
   - 写入项目元数据
   - 写入角色模式配置
   - 写入 Token 管理策略
8. **更新全局索引** ~/.claude/embedded-projects-index.md
9. **输出初始化完成报告**

## CLAUDE.md 模板（新项目初始化）

```markdown
---
role: embedded-debugger
context: fork
max_tokens: 4000
summarize_threshold: 0.8
checkpoint_file: memory-log.md
---

# 项目名称

## 项目元数据
- **芯片型号**: [芯片型号]
- **开发环境**: [Keil/IAR/GCC]
- **调试器**: [J-Link/ST-Link]
- **创建日期**: [日期]

## 工具使用说明

当提到以下关键词时，AI 自动查看对应命令文件：

| 关键词 | 查看文件 |
|--------|----------|
| 编译/build/编译固件 | `EM-SKILL/commands/build.md` |
| 烧录/下载/flash | `EM-SKILL/commands/flash.md` |
| 串口/监控/debug | `EM-SKILL/commands/serial.md` |

## Token 管理策略

### 自动触发条件
- 上下文使用 > 80% 时，自动建议 `/compact`
- 对话轮数 > 20 时，提示生成 Memory Log

### 智能摘要规则
- **保留**：关键决策、已验证的配置、待解决事项
- **压缩**：探索过程、重复的错误尝试、通用知识
- **丢弃**：已解决的临时问题、过时代码片段
```

## 芯片选择界面

```
📋 芯片选择

【已学习芯片】
1. GD32F407VET6 (GigaDevice) [最近: 2026-03-27]
2. STM32F407VET6 (ST) [最近: 2026-03-26]

【内置芯片 - ST】
3. STM32F103C8T6
4. STM32F405RGT6

【内置芯片 - GigaDevice】
5. GD32F405RGT6

【内置芯片 - WCH】
6. CH32V103C8T6
7. CH32V203C8T6

───────────────────────────────────
请选择 (1-7) 或输入芯片型号: _
```

## 相关文件
- workflows/chip-learning.md - 芯片学习机制
