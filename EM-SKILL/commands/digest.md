# 命令: /em digest (手动蒸馏 + 快捕区自维护)

## 功能
S21 手动入口：跳过时间门控，立即清积压 + 跑一轮自维护。与自动管线共用同一套 distill.py。

## 触发
```
/em digest          # 手动触发
整理一下积压 / 蒸馏一下 / 跑一轮自维护   # 自然语言同义触发
```

## 执行流程

1. **【跑管线】**
   ```bash
   python "<SKILL_DIR>/tools/vault/distill.py" --run
   ```
   一次做完：sweep 多源入队 → 取队列 → 书签±k 回读 → headless AI 蒸馏
   → NEW（新知识卡）/ UPDATE（过程卡快照覆盖）/ NONE（零产出）→ 落卡 → commit → 清队列 → 自维护
2. **【报告】** 向用户转述脚本 JSON：新卡几张、过程卡更新几张、查重跳过几张、归档几张（冷卡/待确认积压）、转正建议（如有，读 `~/.em/promotion_suggestions.md`）
3. **【新卡质量】** 逐张列出新卡标题；用户不满意可直接说，删卡/改卡当场做
4. **【错误汇报】** 结果是 error 时读 `~/.em/distill.log` 尾部 5 行给用户看

## 输出格式
```
✅ 蒸馏完成：新卡 N / 过程卡更新 M / 跳过重复 K / 归档 C（冷 x + 待确认 y）
   新卡:
   - 08_快捕/2026-10-30_<标题>.md
   转正建议: <有则列标题；AI 只建议，转不转用户定>
```
零产出时：`✅ 本轮零产出（材料无可复用知识）——这是正常结果，宁少勿多`

## 自动管线（同一机制，供参照）

| 环节 | 触发 | 行为 |
|------|------|------|
| 入队（push） | ZCode Stop / Claude Code SessionEnd hook | triage.py 提取书签行 → `~/.em/pending_lines.jsonl`，零 token |
| 入队（pull） | 每次蒸馏前 sweep | 扫 `~/.em/config.json` 的 `transcript_sources`，增量提取 |
| 蒸馏 | SessionStart hook（后台） | 门控：距上次 ≥ `distill_min_hours`（默认6h）且有积压 → distill.py --maybe |
| 自维护 | 同上，每天最多一次 | 待确认积压/冷卡归档（surfaced=0 超 `archive_min_days`）+ 转正建议报告 |

### hook 注册片段（S21-C 交付，各机一次）

**ZCode**（`~/.zcode/cli/config.json` → `hooks.events`）：SessionStart 数组追加一项——
```json
[{ "hooks": [{ "type": "process", "command": "python", "args": ["-X", "utf8", "<INSTALL_ROOT>/EM-SKILL/tools/vault/hook_session_start.py"], "timeoutMs": 10000 }] }]
```

**Claude Code**（`~/.claude/settings.json`）：
```json
{ "hooks": { "SessionEnd": [
  { "matcher": "", "hooks": [{ "type": "command", "command": "python -X utf8 <INSTALL_ROOT>/EM-SKILL/tools/vault/hook_session_end.py" }] }
] } }
```
> `<INSTALL_ROOT>` 按平台替换（Windows `%USERPROFILE%\.zcode\skills` / `~/.zcode\skills`；路径占位符约定见 EIM CLAUDE.md）。

### 可配项（`~/.em/config.json`，均有默认值）
| 键 | 默认 | 说明 |
|----|------|------|
| `ai_cmd` | `claude -p --model haiku` | headless 蒸馏命令（prompt 走 stdin） |
| `distill_min_hours` | 6 | 自动蒸馏最小间隔 |
| `archive_min_days` | 30 | surfaced=0 冷卡归档天数 |
| `backlog_days` | 30 | 待确认超期归档天数 |
| `queue_cap` | 80 | 单次蒸馏书签上限（熔断） |
| `transcript_sources` | `[]` | sweep 源：`[{"name":"codex","path":"~","glob":".codex/sessions/**/*.jsonl","format":"jsonl"}]` |

## 相关文件
- `tools/vault/distill.py` — 蒸馏器/sweep/自维护实现
- `tools/vault/triage.py` — 入队器（书签 + 指针 + 角色标记，S21-A 重写）
- `tools/vault/hook_session_start.py` — SessionStart 后台触发入口
- `tools/vault/capture.py` — 落卡（extra frontmatter：card_type/files）+ 过程卡覆盖 + 归档
