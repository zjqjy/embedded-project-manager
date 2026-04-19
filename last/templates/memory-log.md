# 项目记忆日志 - {{PROJECT_NAME}}

## 会话指纹
- **项目ID**: {{PROJECT_ID}}
- **当前会话**: {{SESSION_ID}}
- **会话链**: {{SESSION_CHAIN}}

## 快速恢复信息
```
恢复命令: 恢复项目 {{PROJECT_NAME}}，步骤{{CURRENT_STEP}}，问题：{{CURRENT_ISSUE}}，下一步：{{NEXT_ACTION}}
```

## 当前状态
- **步骤**: {{CURRENT_STEP}}
- **状态**: {{STEP_STATUS}}（第{{RETRY_COUNT}}次重试，预算3次）
- **最后活跃**: {{LAST_ACTIVE}}
- **最后会话ID**: {{LAST_SESSION_ID}}

## 待办事项（下次会话自动提示）
1. [高] {{TODO_1}}
2. [高] {{TODO_2}}
3. [中] {{TODO_3}}

## 关键决策（自动继承）
- [{{DECISION_1_DATE}}] {{DECISION_1}}
- [{{DECISION_2_DATE}}] {{DECISION_2}}

## 人工验证历史
- [{{HVR_1_DATE}}] {{HVR_1_ID}}: {{HVR_1_DESC}} - 结果：{{HVR_1_RESULT}}
  - 人工操作: {{HVR_1_ACTION}}
  - 结果: {{HVR_1_DETAIL}}
  - 证据: `{{HVR_1_EVIDENCE}}`

## 新功能开发记录
- [{{FEATURE_DATE}}] 规划新功能: {{FEATURE_NAME}}
  - 描述: {{FEATURE_DESC}}
  - 步骤: {{FEATURE_STEP}}
  - 影响文件: {{FEATURE_FILES}}

## 会话历史

### {{SESSION_1_ID}} ({{SESSION_1_DATE}})
- **持续时间**: {{SESSION_1_DURATION}}
- **主要内容**: {{SESSION_1_CONTENT}}
- **产出**: {{SESSION_1_OUTPUT}}
- **遗留问题**: {{SESSION_1_ISSUE}}

## 代码变更记录

| 日期 | 文件 | 变更类型 | 说明 |
|------|------|----------|------|
| {{CHANGE_1_DATE}} | {{CHANGE_1_FILE}} | {{CHANGE_1_TYPE}} | {{CHANGE_1_DESC}} |

## 调试记录

### {{DEBUG_1_DATE}}
**问题**: {{DEBUG_1_ISSUE}}
**尝试方案**:
1. {{DEBUG_1_TRY_1}} - 结果: {{DEBUG_1_RESULT_1}}
2. {{DEBUG_1_TRY_2}} - 结果: {{DEBUG_1_RESULT_2}}
**结论**: {{DEBUG_1_CONCLUSION}}
