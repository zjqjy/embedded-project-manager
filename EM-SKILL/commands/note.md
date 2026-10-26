# 命令: /em note (知识快捕)

## 功能
把当前对话里的知识（结论/踩坑/可复用方案/关键决策）用最低摩擦落进 vault 快捕区 `08_快捕/`。**你说一声，脏活 AI 干**——frontmatter/查重/git 全部脚本代办（宪法 §9.1）。

## 触发
```
/em note [标题]          # 显式命令
入一下库 / 入库          # 自然语言同义触发（AI 识别后走本流程）
```

## 前置
vault 未连接时首次运行 → 提示 `/em vault connect <路径>`，连接一次永久生效。

## 执行流程

1. **【提炼】** 从对话上下文提炼 1 张卡的标题+正文：
   - 标题即结论（如《ESP32 GPIO 矩阵死锁的根因》），不用《记录一下》
   - 正文 3-8 行：踩坑现象/根因/解法/适用条件；技术词保留英文，中英不留空格
2. **【查重】** 运行脚本粗筛：
   ```bash
   python "<SKILL_DIR>/tools/vault/capture.py" check --title "<标题>"
   ```
   - 无相似 → 直接落卡
   - 有相似（top3 JSON）→ 展示给用户选：**A 新建** / B 更新旧卡（改写那张卡）/ C 追加进旧卡（在旧卡正文补一段）；B/C 时直接 Edit 旧卡文件并 commit，不落新卡
3. **【落卡】**
   ```bash
   python "<SKILL_DIR>/tools/vault/capture.py" write \
     --title "<标题>" --body "<正文（多行用一个临时文件 --body-file）>" \
     --tags "<可选,逗号分隔>" --status 快捕 --source 对话快捕
   ```
   脚本自动：生成 frontmatter（surfaced_count=0 等）→ 写 `08_快捕/YYYY-MM-DD_<标题>.md` → `git commit -m "AI: 快捕 <标题>"`
4. **【报告】** 一行：卡路径 + commit 短码。**目标 ≤10 秒完成，不做多余展开。**

## AI 主动提议（软约定，锦上添花）

hook 分拣（§S1-F）是自动建议的主机制；对话中 AI 额外遵守一条：当出现明显值得入库的产出且用户没提，可**一句话**提议（「这个坑要不要入库？建议卡：《X》」）；同话题只提一次；用户不理会就不再提。

## 输出格式
```
✅ 快捕完成
   卡: 08_快捕/2026-10-26_<标题>.md
   commit: <hash>
```

## 相关文件
- `tools/vault/capture.py` — 落卡/查重实现
- `tools/vault/em_config.py` — vault 路径解析
- vault 宪法 §九 — 规则真值
