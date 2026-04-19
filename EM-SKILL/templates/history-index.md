# 归档索引

## 说明
- 归档触发: 文件 > 行数阈值 或 S步骤完成 或 会话结束
- 活跃文件: 保留最近3个月内容
- 引用格式: `[.emv2/history/<年>/<月>/<日>/文件名.md#锚点]`

---

## 按日期

<!-- 归档记录自动添加 -->

### {{DATE}}
- memory-log.md - {{SUMMARY}}
- project-spec.md - {{SUMMARY}}
- problem-log.md - {{SUMMARY}}
- decision-log.md - {{SUMMARY}}

---

## 按类型

### memory-log.md (记忆日志)
| 日期 | 归档会话 | 归档位置 |
|------|----------|----------|
| {{DATE}} | {{SESSION_ID}} | [.emv2/history/{{YEAR}}/{{MONTH}}/{{DAY}}/memory-log.md#{{SESSION_ID}}] |

### project-spec.md (项目规格单)
| 日期 | 版本 | 归档位置 |
|------|------|----------|
| {{DATE}} | {{VERSION}} | [.emv2/history/{{YEAR}}/{{MONTH}}/{{DAY}}/project-spec.md#{{VERSION}}] |

### problem-log.md (问题追踪)
| 日期 | 摘要 | 归档位置 |
|------|------|----------|
| {{DATE}} | {{SUMMARY}} | [.emv2/history/{{YEAR}}/{{MONTH}}/{{DAY}}/problem-log.md#{{TITLE}}] |

### decision-log.md (决策记录)
| 日期 | 主题 | 归档位置 |
|------|------|----------|
| {{DATE}} | {{TOPIC}} | [.emv2/history/{{YEAR}}/{{MONTH}}/{{DAY}}/decision-log.md#{{DATE}}] |