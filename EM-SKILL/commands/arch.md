# 命令: /em arch (归档)

## 功能
归档旧记录，避免文件膨胀

## 触发
```
/em arch [文件名]
```

## 无参数时
检查并归档所有需要归档的文件

## 有参数时
归档指定文件

## 归档文件类型

| 文件 | 触发条件 | 说明 |
|------|----------|------|
| memory-log.md | > 600行 | 记忆日志，按会话归档 |
| project-spec.md | S完成后 | 项目规格单，按里程碑归档 |
| problem-log.md | > 300行 | 问题追踪记录 |
| decision-log.md | > 300行 | 关键决策记录 |

## 执行流程

1. 检查需要归档的文件
2. 按日期归档: `.emv2/history/<年份>/<月份>/<日期>/`
3. 在原文件开头添加引用注释
4. 更新 `.emv2/history/index.md` 索引
5. 如文件过大（>阈值行），清空原文件内容并保留模板头部

## 归档目录结构

```
.emv2/history/
├── index.md              # 归档索引（总入口）
├── 2026/
│   ├── 04/
│   │   ├── 15/
│   │   │   ├── memory-log.md
│   │   │   ├── project-spec.md
│   │   │   ├── problem-log.md
│   │   │   └── decision-log.md
```

## 触发条件

- 提交结果成功时自动归档
- 会话结束自动归档
- 文件过大时自动归档
  - memory-log.md: > 600行
  - project-spec.md: S完成后
  - problem-log.md: > 300行
  - decision-log.md: > 300行
- 手动命令归档: `/em arch`

## 引用完整性

归档格式:
- `[.emv2/history/<年>/<月>/<日>/memory-log.md#会话ID]`
- `[.emv2/history/<年>/<月>/<日>/project-spec.md#版本]`
- `[.emv2/history/<年>/<月>/<日>/problem-log.md#标题]`
- `[.emv2/history/<年>/<月>/<日>/decision-log.md#日期]`

## 相关文件
- templates/history-index.md - 归档索引模板
- templates/memory-log.md - 记忆日志模板
- templates/project-spec.md - 项目规格单模板
- templates/problem-log.md - 问题追踪模板