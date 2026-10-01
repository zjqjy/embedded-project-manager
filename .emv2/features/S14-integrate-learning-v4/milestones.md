# milestones: S14-整合 S10 学习模式 v4.1 到元仓库

## 选定方案

**方案 A**：`plugins/learning/` 物理解耦 + `/em learn` 子命令

关键决策（待用户最终确认）：
1. 状态目录归属 → **用户项目内 `.em/learning/state.md`**（插件只提供 schema）
2. topics/ 位置 → **用户项目内创建**（插件 `templates/topics/` 只作种子）
3. 通用核 README 加 `## Plugins` 章节
4. em-new-s10 重档产物归档到 `.emv2/history/2026/07/13/S10-learning-v4-design/`

## 子步骤

### S14-A: 学习模式插件骨架
- 内容：创建 `EM-SKILL/plugins/learning/` 目录，写入 PLUGIN.md（入口文档，Mermaid 拓扑图复用 em-skill-v4.1 的 LPR 图）+ commands/learn-new.md / learn-verify.md / learn-status.md + workflows/learn-lpr.md（L1-L5 阶段流转）
- 依赖：无（首子步骤）
- 验证：`/em help learn` 能列出 3 个子命令；PLUGIN.md Mermaid 渲染正常
- 预估：M

### S14-B: 模板层迁入
- 内容：从 `em-skill-v4.1/.em/learning/` 迁入 `plugins/learning/templates/`：README-card.md（5 段式）、lpr-stage.md（L1-L5 模板）、_index.json.example、topics/ota-firmware-upgrade/（种子，含 README + deep-dive + cheatsheet）
- 依赖：S14-A
- 验证：模板文件结构与 S10 brainstorm 决策一致；OTA 主题种子能作为新主题参考
- 预估：M

### S14-C: 脚本层迁入
- 内容：从 em-skill-v4.1 迁入 `plugins/learning/tools/`：build-html.py（Markdown → HTML，暗色主题 + Mermaid CDN）、generate-script.py（README → 视频口播稿）
- 依赖：S14-B（脚本依赖 README 卡片结构稳定）
- 验证：`python build-html.py <test.md>` 能生成 HTML；Mermaid 渲染通过 CDN
- 预估：M

### S14-D: 注册与文档
- 内容：1) 新建 `EM-SKILL/plugins/INDEX.md`（列出 embedded + learning） 2) 通用核根 README.md 新增 `## Plugins` 章节 3) 与 S13 协同：CLAUDE.md 触发器同步注册 `/em learn` 前缀
- 依赖：S14-A（需先有插件骨架才能索引）
- 验证：`/em pi` 列出 learning 插件；通用核 README 渲染正常
- 预估：S

### S14-E: 归档与收尾
- 内容：1) 归档 em-new-s10 五个产物（split/req/hardware/brainstorm/milestones + status.json + execution-log）到 `.emv2/history/2026/07/13/S10-learning-v4-design/` 2) em-skill-v4.1 原型保留为参考 3) 更新 `state.md`（S14 完成，下一步 `/em verify s14`）+ `project-spec.md` 步骤表追加
- 依赖：S14-D（最后一步，确保所有产物已落地再归档）
- 验证：`/em stat -v` 显示 S14 完成；history 目录结构正确
- 预估：S

## 关键决策（记入 decisions.md）
- [2026-07-13] 学习模式作为 `plugins/learning/` 物理解耦，遵循 v3.0 通用核零业务原则
- [2026-07-13] 学习状态目录归用户项目（`.em/learning/state.md`），插件只提供 schema
- [2026-07-13] 通用核 README 新增 `## Plugins` 章节，声明 EM-SKILL 是插件宿主
- [2026-07-13] S10 重档产物归档到 history，作为学习模式 v4.1 设计档案可追溯

## 升降档检查
- ✅ 子步骤数 = 5（符合中档 ≤ 5 约束）
- ✅ 每个子步骤可独立 verify
- ✅ 无新外设/协议栈，不触发升重档

---

生成时间: 2026-07-13 23:35