# 需求确认 - 优化项目记忆和工具文件模板

## 重复问题确认

### 1. project-spec.md vs memory-log.md
- **方案**: project-spec 瘦身，只保留步骤状态表和技术方案
- 去掉：关键决策、讨论方案要点、待执行任务
- memory-log 统一：保留会话历史和决策，去掉步骤状态表和最近更新

### 2. 讨论目录 vs project-spec.md
- **方案**: project-spec 只留一行「讨论目录」引用
- 方案要点、待执行任务只存在 discussion/ 中

### 3. memory-log.md「最近更新」vs 会话历史
- **方案**: 删除「最近更新」，统一用「会话历史」追溯

### 4. 全局文件膨胀（新增）
- SKILL.md 命令列表、commands/ 各文件、workflows/ 细则文件也可能有重复和膨胀
- 需要一并评估优化
