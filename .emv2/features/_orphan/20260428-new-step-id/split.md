# 需求拆分 - new 命令步骤编号

## 问题
`/em new` 创建的开发步骤缺少统一编号，导致 verify 阶段无法引用、stat 无法追踪。

## 涉及模块

| 编号 | 模块 | 说明 |
|------|------|------|
| 1 | `commands/new.md` | new 命令增加步骤编号生成逻辑 |
| 2 | `commands/verify.md` | verify 支持新编号格式 |
| 3 | `commands/stat.md` | 状态显示识别新编号 |
| 4 | `project-spec.md` | 步骤跟踪表调整 |
| 5 | `workflows/hvr-workflow.md` | 验证工作流引用编号方式 |

## 已确认方案

- **编号方式**: 项目内自增（当前最大 S 编号 +1）
- **起点**: 存量项目从当前最大编号 +1，新项目从 S1 开始
