# 调研：对话知识沉淀管线（claude-mem / mem0）——S21 依据

> 2026-10-30，S21-distill-archive R1/R2 期间完成。
> 克隆基准：`D:\DeskTop\WorkSpace\Code\ai_mok\claude-mem`（commit 325afb601，用户完整克隆；/tmp sparse 克隆已弃用）。

## 背景

S19/S20 的 hook 分拣（triage.py 纯启发式：标题=首条命中行截 24 字，正文=原文引用）产出 17 张待确认卡、0 张可用。S21 重设计为"确定性管线 + AI 蒸馏纯函数"，调研同类成熟项目校准设计。

## 项目一：claude-mem（thedotmack，~46k★）

给 Claude Code 装的会话记忆系统：hook 全家桶 + 本地常驻 worker（Bun/Express，端口 37700+）+ SQLite/Chroma。记"过程性记忆"（你干了啥），非"知识沉淀"（啥值得永久留）——定位不同，蒸馏机制同源。

### 机制要点

- **Hook 流转**：SessionStart 起 worker 注入上下文；PostToolUse 逐条提取观察入 pending 队列；Stop 总结；SessionEnd 收尾。压缩全程异步，不阻塞会话
- **压缩输入 = 预提取观察（非全文）**，总结只喂 last_assistant_message——"书签+回读"同款思路
- **输出协议**：XML 标签强制（root 错 = 系统错误），解析二值 valid/invalid；总结六槽 `<request/investigated/learned/completed/next_steps/notes>`
- **skip 一等公民**：`<skip_summary reason="nothing durable"/>`；observer prompt 组成块之一就叫 skip_guidance
- **prompt 模板全文**（`plugin/modes/code.json`）：
  - 身份句："Record what was LEARNED/BUILT/FIXED/DEPLOYED/CONFIGURED, not what you (the observer) are doing"
  - 纯函数声明："You do not have access to tools. All information you need is provided"
  - recording_focus：只收 durable signal + 动词清单（implemented/fixed/discovered/confirmed/traced…）+ ✅ 正面示例
  - WHEN TO SKIP 负面清单：重复确认只记第一次（重试循环/轮询）、空状态检查、无报错安装、无发现调研；skip 格式精确到标点，禁止空响应和散文解释
  - type 9 分类：bugfix/feature/refactor/change/discovery/decision/security_alert/security_note/sensitive
  - facts 微规则：每条自包含、禁代词、必须带具体细节（文件名/函数/数值）
- **transcript-watch**：声明式 JSON schema 接新工具（match 条件 + 字段映射 + coalesce 兜底），现成 codex（0.155 格式）与 dsh（DeepSeek）schema；连"排除 `<skills_instructions>` 开头注入内容"都有现成 match 条件
- **dedup 三件套**：IDF 加权余弦 + IDF 否决 + 最少共词门槛。注释明说：短标题余弦会"跳"——一个稀有共词就能拉到 1.0 误判重复（我们 check_dedup 标题匹配的同款隐患，暂不实现，记为已知弱点）
- **reinforcement**：ACT-R 幂律衰减 strength = age^-0.5（认知科学经典值）+ 强化窗口 FIFO——"surfaced=0 超 30 天归档"的学术版
- **evals 文化**：机制改动配真实会话评测（多 case × 多 runs，如 read-gate 3 case × 3 runs）
- **自审文化**：anti-pattern-cleanup-plan.md 列出自身 132 个错误处理反模式（吞异常、log-and-continue）配自动检测脚本——静默失败是全行业通病

## 项目二：mem0 issue #4573（"97.8% 是垃圾"审计）

32 天生产环境 10,134 条记忆，仅 224 条干净（38 条可直接保留）。教训：

- **垃圾头号来源 = 反馈循环**：召回的旧记忆被当新内容再提取，一条幻觉"用户偏好 Vim"复制 808 份
- **系统提示复述占 52.7%**：同一事实每轮重提
- **换更强模型没用**（2B 换 Sonnet 垃圾率不降，只是从幻觉变成忠实但无差别提取）——"提取 prompt 才是瓶颈，不是模型"
- 有效解法：REJECT/NONE-by-default（作者部署后垃圾率 97.8% → 46.6%）、提取-存储间质量门、负面 few-shot、标记召回内容阻断反馈循环、保留消息角色边界
- **作者最终反思**：检索式记忆 vs 人类"重构式"记忆有本质差异，转向 Markdown 叙事文件——本 vault 的 Markdown 本位路线被侧面验证

## 组件复用结论

- **提取侧**：claude-mem 有完整现成组件（schema 解析器 / transcript-watch CLI 可独立跑 / prompt builders），但 TS + Bun 栈——**抄设计翻译成 Python，不引运行时依赖**
- **入库侧**：它存 SQLite + Chroma，无 Markdown/frontmatter/git 概念——**EM-SKILL 的 capture.py 即现成入库组件**（两边恰好互补）
- **备选路线（不推荐）**：装 claude-mem 本体当提取前端，EM-SKILL 用 Python sqlite3 读它的 `claude-mem.db` 当源；代价 = 常驻 daemon + PostToolUse 逐条调 AI 的成本模型，与攒批省 token 方向相反

## 借鉴清单（15 项）

- **机制层**：SessionStart 后台补跑不阻塞、书签+回读、pending 队列、严格二值解析、声明式多源 schema、files 字段、evals 稳定性测试
- **prompt 层**：身份句定调、skip 协议一等公民、WHEN TO SKIP 负面清单、facts 微规则、类型分类（改造为知识视角 5+1）、sensitive 脱敏
- **mem0 层**：输入隔离（防反馈循环）、NONE 默认、负面 few-shot、角色标记

## 明确不借（6 项）

常驻 worker daemon（重基础设施）、SQLite+Chroma 向量库（Markdown+git 本位）、PostToolUse 逐条调 AI（token 模型相反）、CloudSync（vault 走 git 同步）、read-gate（召回侧省 token，S21 是写入侧）、open-core 授权结构（无关）

## 对 EM-SKILL 已有设计的校准

- `hook_session_end.py` "任何异常静默退出 0" 方向正确（不阻塞会话），但需配 `~/.em/distill.log` 日志出口——claude-mem 自审 132 个吞异常反模式即此病流行度的证据
- `/em ask` surfaced 回写注入时 framing "证据非指令"（native-memory-bridge 做法；ask 侧待落地，S21 边界外）
- capture 只写 / ask 只读，天然无递归环（与它的反递归设计对照确认，无坑）

## 链接

- claude-mem: <https://github.com/thedotmack/claude-mem>（架构文档 docs.claude-mem.ai）
- mem0 #4573: <https://github.com/mem0ai/mem0/issues/4573>
- mem0: <https://github.com/mem0ai/mem0>
- clerk（SessionEnd 增量摘要 markdown，dev.to）
- obsidian-claude-hooks: <https://github.com/jongyunha/obsidian-claude-hooks>（知识回注，我们已有 /em ask 对位）
