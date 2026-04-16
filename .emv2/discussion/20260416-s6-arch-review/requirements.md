# S6 归档机制讨论 - 需求确认

**讨论ID**: 20260416-s6-arch-review
**日期**: 2026-04-16
**参与者**: 用户 + AI

---

## 原始问题

用户指出 S6 归档机制遗漏了最重要的两个文件：
1. memory-log.md - 记忆日志
2. project-spec.md - 项目规格单

这两个文件才是容易膨胀的重点，而不是 templates/ 下的模板文件。

---

## 讨论结论

### 归档文件类型（修正）

| 文件 | 触发条件 | 说明 |
|------|----------|------|
| memory-log.md | > 200行 | 记忆日志，按会话归档 |
| project-spec.md | S完成后 | 项目规格单，按里程碑归档 |
| problem-log.md | > 100行 | 问题追踪记录 |
| decision-log.md | > 100行 | 关键决策记录 |

### 归档后的使用场景

1. **查找历史决策**: 通过 `/em gi` 或 history/index.md 找到归档文件
2. **恢复项目上下文**: 读取 memory-log 活跃部分 + 归档的会话摘要
3. **问题闭环追溯**: problem-log 的"已解决问题"列表含归档引用

### 归档后引用格式

```
[.emv2/history/<年>/<月>/<日>/memory-log.md#会话ID]
```

### 活跃文件保留策略

- memory-log.md: 保留最近3个月内容
- 归档时清空原文件，保留模板头部
- 原文件开头添加引用注释

---

## 更新的文件

1. **templates/history-index.md** - 增强，支持 memory-log 和 project-spec
2. **commands/arch.md** - 更新归档文件类型和执行流程
3. **project-spec.md S6** - 补充 memory-log 和 project-spec 归档说明
