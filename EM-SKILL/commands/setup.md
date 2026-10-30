# 命令: /em setup (环境自检 + 修复)

## 功能
一条命令把 EM-SKILL 环境从零带到"可直接用"：检测 → 能自动修的自动修 → 不能修的给精确到命令的指引。
人和 AI agent 都能跑（JSON + 人话双输出）。S22。

## 触发
```
/em setup                # 全量体检（安全项自动修复）
/em setup --guide        # 向导：不自动修，逐项问用户后再修
/em setup --embedded     # 附带嵌入式检查组（= 原 /em initem，已别名化）
环境体检 / 检查环境 / setup 一下    # 自然语言同义触发
```

## 参数
| 参数 | 说明 |
|------|------|
| （无） | 全量检测 + 安全项自动修复（写配置前自动备份 `.bak-时间戳`） |
| `--guide` | 不动手，列出"可自动修"项由会话 AI 逐项问用户，确认后 `--fix-only <id>` 逐个执行 |
| `--fix-only <id>` | 只修指定检查项（如 `hook_zcode` / `engine`） |
| `--smoke` | 附带真实引擎冒烟（一次 headless 调用，花少量 token，默认跳过） |
| `--embedded` | 附带嵌入式检查组 |
| `--json` | 只输出 JSON（agent 消费） |

## 检查项（通用组）
| id | 检查 | 修复 |
|----|------|------|
| python | Python ≥3.10 | 指引安装 |
| git | git 可用 | 指引安装 |
| vault | `~/.em/config.json` vault_path 有效 | 无 → 引导 `/em vault init <目录>` |
| engine | 蒸馏引擎发现链 claude → codex exec → 手动降级，自动写 `ai_cmd` | 无 CLI → 指引安装；手动模式不影响其余功能 |
| hook_zcode | ZCode Stop(入队) + SessionStart(蒸馏) 注册状态 | 自动 JSON 合并式插入（不覆盖既有 hook），改前备份 |
| hook_claude | Claude Code SessionEnd 注册 | 同上（未用 Claude Code 则跳过） |
| codex_sweep | `~/.codex/sessions` 存在 → transcript_sources 自动加 sweep 源 | 幂等 |

插件可追加检查组：PLUGIN.md 声明 `provides.setup_checks: <模块路径>`，模块提供 `register_checks(apply)`。embedded 即范例。

## 执行流程（AI 承担部分）
1. 跑脚本，转述人话报告
2. **📋 需人工项**：逐项把 `guide` 字段转述给用户（含精确命令），处理完重跑复查
3. `--guide` 模式：对每个"可自动修"项问用户是否执行，确认后逐个 `--fix-only`
4. **error**：原样报给用户

## 输出格式
```
🩺 /em setup 环境体检
 ✅ [基础] Python ≥3.10 — Python 3.14.x
 ✅ [基础] git — git version 2.x
 ✅ [知识流] 知识库 vault — vault: D:\...
 🔧 [知识流] ZCode hook — 已补注册（备份 config.json.bak-...）
 📋 [知识流] 蒸馏引擎 — 缺失 → ↳ 安装指引...
就绪 5 / 自动修 1 / 需人工 1
```

## 相关文件
- `tools/setup.py` — 框架 + 通用检查组
- `plugins/embedded/setup_checks.py` — 嵌入式检查组（原 initem 职责，经 `provides.setup_checks` 注册）
- `plugins/embedded/commands/initem.md` — 别名指针（`/em initem` = `/em setup --embedded`）
