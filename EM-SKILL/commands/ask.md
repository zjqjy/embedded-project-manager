# 命令: /em ask (知识提取)

## 功能
从 vault 检索知识回答问题——返回带路径+双链的片段，命中快捕卡自动累积 surfaced 信号（转正判定的输入，宪法 §9.3）。

## 触发
```
/em ask <问题>
```

## 前置
未配置库时**不要只甩报错**：按 `commands/vault.md` §init 引导用户二选一（选目录建库 / 装 Obsidian 指引），建好再继续本次提问；用户明确说「以后」才中止。

## 执行流程

1. **【检索】**
   ```bash
   python "<SKILL_DIR>/tools/vault/search.py" query "<问题关键词>" --limit 5 --surface-top 3
   ```
   纯本地关键词/二元组计分（标题×3、tags×2、正文×1），无索引服务；`surfaced_count`/`last_surfaced` 自动回写前 3 条并 commit。
2. **【阅读】** 对 top 1-3 条结果，按需 Read 原文件取细节（检索 snippet 不够时才读）。
3. **【回答】** 回答必须带出处：`[[笔记名]]`（相对路径），快捕卡注明「尚未转正」。
4. **【缺口】** 检索无命中 → 明说"库里没有"，并提示 `入一下库` 可把本次对话结论存进去。

## briefing 模式

`/em vault briefing` 或 `/em rec` 附带：近 7 天入库摘要 + 待确认数（`search.py briefing`）。

## 输出格式
```
🔍 /em ask — <问题>
- <结论要点> — [[来源笔记]]（<路径>）
...
✍️ surfaced 已回写 3 张
```

## 相关文件
- `tools/vault/search.py` — 检索/回写/摘要实现
- vault 宪法 §9.2 — surfaced 是转正信号
