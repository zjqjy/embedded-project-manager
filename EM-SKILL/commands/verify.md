# 命令: /em verify (步骤验证)

> **通用核版本**：流程控制、HVR 文件生成、commit 提议。
> 嵌入式项目自动加载 `plugins/embedded/workflows/verify-embedded.md` 注入编译/烧录/串口子流程。

## 功能
生成人工验证请求 (HVR)，提议 commit。

## 触发
```
/em verify s<编号>    # 如 /em verify s7 或 /em verify s7-a
```

步骤参数使用 `/em new` 分配的 S 编号。

## 执行流程（通用）

1. **【状态目录】** `get_state_dir()` → `<STATE_DIR>`
2. **【项目类型】** 读 `<STATE_DIR>/project.json` 的 `type` 字段
3. **【更新状态】**
   - `state.md`: 当前步骤 → `S<N>` 🔄 验证中
   - `project-spec.md` 步骤表对应行状态同步
4. **【生成 HVR】** 见下方「HVR 模板」
5. **【嵌入式注入】** 如 `type == "embedded"` → 加载 `plugins/embedded/workflows/verify-embedded.md` 执行编译/烧录/串口三连，结果记入 HVR 的「嵌入式执行记录」区段
6. **【输出验证清单】** 列出待用户确认的检查点
7. **【提议 commit】** 见下方「commit 提议」

## HVR 文件

- 路径：`<STATE_DIR>/checkpoints/HVR-<步骤>-<序号>.md`
- **模板选择**（按 `project.json.type` 自动）：
  - `general` → `templates/hvr-template.md`（通用模板，无嵌入式三连）
  - `embedded` → `plugins/embedded/templates/hvr-template-embedded.md`（含「嵌入式执行记录」表 + 工具执行记录 + 共同决策段）
- 流程细则与字段说明：`workflows/hvr-workflow.md`

## commit 提议（S10-D 集成）

HVR 文件 + 工具执行结果记录完成后，AI **不直接 commit**，而是输出"提议"：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 提议 commit  (S10-D Git 集成)
━━━━━━━━━━━━━━━━━━━━━━━━━━
建议 commit message:
  [S<step>] feat: verify <步骤描述> with HVR-<序号>

待提交文件:
  M  <STATE_DIR>/checkpoints/HVR-<步骤>-<序号>.md
  M  <STATE_DIR>/state.md
  M  <STATE_DIR>/project-spec.md

确认提交？[y/n/edit]
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 用户响应

| 输入 | 行为 |
|------|------|
| `y` / `确认` | `git add` + `git commit -m "..."` |
| `n` / `取消` | 跳过 |
| `edit` / `修改为: ...` | 用新 message 重提议 |
| `amend` | 加入上一次 commit（需用户已 commit 过） |

### 执行约束

- ✅ 允许 `git status` / `git add` / `git commit -m "..."`
- ❌ 禁止 `git push`（必须拒绝并提示手动 push）
- ❌ 禁止 `--no-verify` / `--force` 等破坏性选项
- ❌ 禁止 `git commit --amend` 改写历史

### 提议规则

- `commit message` 必须以 `[S<n>]` 开头
- type 推断：HVR 通过 → `feat`；修复 → `fix`；仅文档 → `docs`
- subject ≤ 50 字符；body 可选（解释 HVR 关键结论）

### 跳过条件

- 工作区无变更
- 仅日志/构建产物（应在 `.gitignore` 中）
- 用户明确说"暂不提交"

## 相关文件
- `workflows/hvr-workflow.md` — HVR 模板与流程图
- `plugins/embedded/workflows/verify-embedded.md` — 嵌入式 verify 子流程（仅 type=embedded 加载）
- `commands/result.md` — 验证结果记录
