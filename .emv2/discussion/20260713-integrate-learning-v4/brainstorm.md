# brainstorm: S14-整合 S10 学习模式 v4.1 到元仓库

## 需求理解

S10（em-new-s10/）已完成学习模式 v4.1 的**设计阶段**（重档 5 阶段：split/req/hardware/brainstorm/milestones），确定了 LPR 闭环、主题 README 卡片、知识图谱、调研管理、多格式构建等核心机制。
em-skill-v4.1/.em/learning/ 已落地**原型**：README.md（学习拓扑 + 主题卡片墙 + 知识图谱）+ _index.json（结构化主题元数据）+ state.md（学习状态）+ scripts/templates/topics/。

S14 任务是把这两份产物**整合进 EM-SKILL 元仓库**，使其成为 EM-SKILL 自身的子系统（而非外挂测试目录）。核心问题：**学习模式在 EM-SKILL 元仓库哪里放、怎么挂载、如何与现有 /em 通用命令交互**。

## 候选方案

### 方案 A: `plugins/learning/` 物理解耦 + `/em learn` 子命令 ⭐ (推荐)
- 思路：与 `plugins/embedded/` 同级新增 `plugins/learning/` 目录，内含 commands/workflows/templates/tools，命令用 `/em learn new <topic>` `/em learn verify` 等子命令前缀挂载
- 优点：
  - 哲学一致：延续 v3.0 "通用核 + 插件" 解耦设计（EM-SKILL 自身学习模式也是一类"插件"）
  - 零污染通用核（通用 16 命令不变）
  - 未来可独立分发（学习模式作为独立 skill 包）
  - 嵌入式 + 学习双插件并存：通用项目用 embedded，开发者用 learning
- 缺点 / 风险：
  - 命令路径变深：`/em learn new` 比 `/em new` 多一层（但比 Notion/飞书学习工作流仍极简）
  - 需要在通用核注册 learn 命令前缀（轻改动）
  - 元仓库体积增加约 50-80 个文件（可控）

### 方案 B: 通用核 `commands/learn.md` + `workflows/learn-*`（融入 16 命令）
- 思路：把 `/em learn new` `/em learn verify` 直接加到 16 个通用命令里，作为 `/em new` 的姐妹命令
- 优点：
  - 命令路径短：用户上手快（`/em learn` 一目了然）
  - 不需要新插件加载机制
- 缺点 / 风险：
  - **破坏 v3.0 设计原则**：通用核膨胀，未来加更多子模式时失控
  - 学习模式与嵌入式插件**哲学不一致**（嵌入式是 plugin，学习是 core）→ 用户困惑
  - 后续分发麻烦（学习模式想给外部项目用必须从通用核剥离）

### 方案 C: `templates/learning/` + `/em new --learning` flag 复用
- 思路：把学习模式作为模板（templates/learning/）挂到现有 /em new 命令下，加 --learning flag 触发
- 优点：
  - 改动最小：零新命令、零新目录结构
  - 复用现有 /em new 三档分流机制
- 缺点 / 风险：
  - **复用错位**：/em new 设计目标是"新功能开发"（5-15-45 min），学习主题是"长期沉淀"（2-3 周主题），心智模型冲突
  - 学习模式特有的 LPR 闭环、主题卡片墙无法在 /em new 模板里表达
  - 未来扩展性差（如果加 /em verify --learning、/em arch --learning 等会污染 /em 主命令）

## 推荐

**方案 A（plugins/learning/ 物理解耦 + /em learn 子命令）**

理由：
1. **哲学一致性**：与 v3.0 "通用核 + plugins/embedded/" 完全同构，EM-SKILL 元仓库的"学习模式"和"嵌入式插件"是平等的两类扩展
2. **可分发性**：未来学习模式可独立打包成 `.skill` 分发（与 EM-SKILL 自身解耦）
3. **长期演进**：如果将来加 "AI 协作模式"、"项目管理模式" 等，可继续按 plugin 模式扩展，不破坏通用核
4. **风险可控**：方案 B/C 都有"破坏现有设计"的风险，方案 A 是 v3.0 设计的自然延伸

## 关键技术点

- **插件注册机制**：通用核新增 plugins/ 索引（参考 plugins/INDEX.md）→ 学习模式自动被发现
- **命令前缀分发**：`/em learn *` 路由到 `plugins/learning/commands/learn-*.md`
- **模板复用**：em-skill-v4.1/.em/learning/templates/ 整体迁入 plugins/learning/templates/
- **数据格式兼容**：em-skill-v4.1/.em/learning/_index.json 格式直接采用（已稳定）
- **状态独立**：学习模式有自己的 state.md（不污染通用核 state.md）
- **文档入口**：plugins/learning/README.md 作为学习模式的入口文档（Mermaid 拓扑图复用）
- **与 S13 协同**：S13 的"initem 注册全局 CLAUDE.md 触发器"机制可作为学习模式插件加载的参考实现

## 待用户确认的细节

1. 学习模式是否需要**独立的 .em/ 状态目录**？还是复用项目级 state.md？
2. 学习主题（topics/）放插件内 templates/ 还是允许用户项目内创建？
3. 是否需要在通用核 README.md 加 `plugins/` 章节列出所有插件？
4. 整合是否包含 em-new-s10 的**重档产物归档**（作为历史讨论存档）？

---

生成时间: 2026-07-13 23:30
S14 推荐档位: 中（brainstorm + milestones）