# 命令: /em stat (项目状态)

## 功能
查看项目状态：默认极简（state.md），`-v` 详细（含步骤全表、最近会话、决策、问题）。

## 触发
```
/em stat              # 默认：读 state.md，输出 ≤10 行
/em stat -v           # 详细：加载 project-spec/最近会话/decisions/problem-log
/em stat steps        # 只显示开发步骤状态表
/em stat next         # 只显示下一步动作
```

## 加载策略

| 模式 | 加载文件 | 用途 |
|------|---------|------|
| 默认 | `state.md` + `project.json` | 快速看现在做啥 |
| `-v` | + `project-spec.md` + 最新 `sessions/<id>.md` + `decisions.md` + `problem-log.md` | 全景 |
| `steps` | `project-spec.md` 的步骤表区段 | 看进度 |
| `next` | `state.md` 的「下一步动作」区段 | 极简 |

## 执行流程

1. **【状态目录】** 调用 `get_state_dir()` → `<STATE_DIR>`
2. **按模式加载**对应文件
3. **输出对应格式**

## 输出格式

### 默认模式
```
📍 <项目名> — S<N> <状态>
更新: YYYY-MM-DD   会话: sess-...

下一步:
1. <动作1>
2. <动作2>

详情: /em stat -v
```

### `-v` 模式
```
📍 <项目名> (<type>) — S<N> <状态>

━━ 步骤状态 ━━
| S1 | ✅ | ... |
| ... |

━━ 最近会话 sess-... ━━
<会话内容>

━━ 最近决策 ━━
<3-5 条>

━━ 待解决问题 ━━
<P0/P1 列表>

下一步:
- ...
```

### `steps` 模式
仅输出 `project-spec.md` 的步骤状态表。

### `next` 模式
仅输出 state.md 的「下一步动作」区段。

## 旧版兼容
- 无 state.md → 默认模式回退读 memory-log 前 30 行
- 无 sessions/ → `-v` 模式从 memory-log 提取会话

## 设计原则
- ❌ stat 默认不再灌入完整 memory-log/project-spec
- ✅ 渐进式查询：默认极简 → 用户主动 `-v` 才详细

## 相关文件
- `commands/rec.md` — 启动恢复，加载同样的 state.md
- `commands/sessions.md` — 单独浏览会话历史
- `templates/state.md` — state.md 模板
