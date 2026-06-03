# 命令: /em sessions (会话历史浏览)

## 功能
按需浏览历史会话（每会话一个 `.md`）。**与 rec 解耦**：rec 不再加载会话历史，需要时用这个。

## 触发
```
/em sessions             # 列最近 10 个会话标题（不展开内容）
/em sessions <id>        # 展开指定会话（如 sess-20260602-001）
/em sessions latest      # 展开最近一个会话
/em sessions search <kw> # 搜索会话内容（关键字）
```

## 文件布局

```
<STATE_DIR>/sessions/
├── sess-20260225-001.md
├── sess-20260327-001.md
├── ...
└── sess-20260602-001.md   ← 当前
```

老会话归档时按月份滚到 `<STATE_DIR>/history/<YYYY>/<MM>/sessions/`，sessions 目录只留最近 ~30 天。

## 兼容旧版

旧版项目（无 sessions/ 目录）：从 `memory-log.md` 的「会话历史」区段解析，按 `### sess-...` 切分为虚拟会话条目展示。

不破坏旧文件，只读不写。

## 执行流程

### 无参数（列表）
1. 扫描 `<STATE_DIR>/sessions/*.md`（或解析 memory-log 兼容）
2. 输出：

```
📜 会话历史（最近 10 个，共 N 个）

ID                    日期         主题摘要
─────────────────────────────────────────
sess-20260602-001     2026-06-02   S10 标准化+通用化+Git集成 ← 当前
sess-20260430-001     2026-04-30   S9-F 全流程验证
sess-20260429-001     2026-04-29   S9 embed-ai-tool 整合
...

查看详情: /em sessions <id>
```

### 带 ID
读取 `sessions/<id>.md` 全文并展示。

### latest
按文件 mtime 排序取最新 → 同上。

### search
对所有会话文件做 grep，输出命中行 + 上下文。

## 设计原则
- ❌ rec 不再被会话历史拖慢
- ✅ 会话独立成文件，归档/检索都干净
- ✅ 旧 memory-log 项目零破坏

## 相关文件
- `commands/rec.md` — 已不再加载会话历史
- `templates/session.md` — 单会话模板
- `commands/arch.md` — 会话归档时移动到 history/
