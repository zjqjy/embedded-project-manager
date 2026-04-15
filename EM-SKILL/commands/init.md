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
7. **更新全局索引** ~/.claude/embedded-projects-index.md
8. **输出初始化完成报告**

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
