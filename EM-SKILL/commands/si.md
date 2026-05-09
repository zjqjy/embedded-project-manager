# 命令: /em si (存量接入)

## 功能
分析现有代码，重建项目状态

## 触发
```
/em si [路径]
```

## 参数
- **路径**（可选）：项目目录路径
  - 不带路径时：使用当前项目目录（`.`）
  - 带路径时：使用指定目录

## 执行流程

1. **进入指定目录**
2. **分析代码结构**
   - 识别芯片型号（查找 system_xxx.c, startup_xxx.s）
   - 识别已初始化外设（gpio, usart, i2c, spi, timer等）
   - 识别驱动层（已驱动的传感器/设备）
   - 识别应用层（主功能循环）
   - 识别调试接口（printf重定向，LED指示）
   - 检查git状态（最后一次提交信息）

3. **【芯片学习】**
   - 检查 ~/.claude/chips.json 是否存在
     - 不存在 → 自动创建
   - 检测芯片型号：正则提取 system_xxx.c / startup_xxx.s
   - 识别厂商：ST → ST, GD → GigaDevice, CH32/WCH → WCH
   - 检测外设：搜索 gpio_init, usart_init 等关键词
   - 添加到 chips.json
   - 如芯片已存在 → 更新 lastUsed 时间戳

4. **创建 .emv2/ 目录结构**
5. **生成/更新 project-spec.md 和 memory-log.md**
6. **创建/更新 CLAUDE.md**
   - 如果项目没有 `CLAUDE.md`，创建并写入：
     - 工具使用说明索引
     - 角色模式配置
     - Token 管理策略
7. **更新全局索引:embedded-projects-index.md,一般在.claude里**
8. **输出审计报告**

## CLAUDE.md 模板（存量接入时）

```markdown
---
role: embedded-debugger
context: fork
max_tokens: 4000
summarize_threshold: 0.8
checkpoint_file: memory-log.md
---

# 项目名称

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

## 输出格式

```
🔍 代码审计完成

识别结果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📟 芯片型号: [从代码识别]
✅ 已完成:
   - [步骤]: [描述]

⚠️ 部分完成:
   - [步骤]: [描述]

🔄 当前状态推测:
   - 步骤: [当前步骤]
   - 问题: [发现的问题]
   - 上次提交: [git log信息]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 相关文件
- workflows/chip-learning.md - 芯片学习机制
