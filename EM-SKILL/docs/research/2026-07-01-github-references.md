# GitHub 参考项目调研 — EM-SKILL 插件化方向

**日期**: 2026-07-01
**作者**: Claude (基于已有知识 + 远程无法访问的现状)
**目标**: 为 EM-SKILL 规范化（plugin + skill）提供外部参考

---

## 0. 调研方法说明

### 0.1 环境限制
- ❌ WebSearch 持续 400 错误（API 受限）
- ❌ WebFetch github.com / docs.claude.com / modelcontextprotocol.io 全被组织防火墙拦截
- ✅ **本报告基于训练数据（截止 2026-01）的已有知识**

### 0.2 调研方法
1. 优先找"元仓库"（管理其他 skill/plugin 的仓库）
2. 优先找"spec/manifest 文件"（schema/配置规范）
3. 关注与 EM-SKILL 同类的"工作流 + 命令"型 skill
4. 关注 MCP 协议（嵌入式工具已用 MCP server 形式）

### 0.3 置信度标注
- 🟢 **高置信**：训练数据中反复出现 / 广泛引用
- 🟡 **中置信**：见过但细节可能不准确
- 🟠 **低置信**：可能存在但细节需用户验证

---

## 1. Anthropic 官方生态（🟢 高置信）

### 1.1 `anthropics/skills`
- **URL**: https://github.com/anthropics/skills
- **类型**: 官方 skill 仓库
- **关键规范**:
  - `SKILL.md` 顶层 frontmatter
  - `name / description` 必填
  - 子目录按 `category/skill-name/` 组织
- **可借鉴**:
  - frontmatter 字段设计
  - 目录布局惯例

### 1.2 `anthropics/claude-cookbooks`
- **URL**: https://github.com/anthropics/claude-cookbooks
- **类型**: 官方 cookbook
- **可借鉴**:
  - skill 模板
  - `tools/` `workflows/` `agents/` 的组织方式

### 1.3 Claude Code Plugin 机制
- **位置**: Claude Code v1.0+ 内置
- **关键规范** (从 CC 文档训练数据):
  - 插件存放在 `~/.claude/plugins/<plugin-name>/`
  - 每个插件有 `plugin.json` 元数据
  - 支持 `commands / agents / hooks / mcp_servers`
  - 启用方式：`/plugin install <name>` 或 `plugin.json` 配置
- **可借鉴**:
  - **plugin.json 字段**：`name / version / description / provides / hooks / mcp_servers`
  - 插件启用/禁用机制

---

## 2. Superpowers 框架（🟢 高置信 — EM-SKILL state.md 明确引用）

### 2.1 `obra/superpowers`
- **URL**: https://github.com/obra/superpowers
- **类型**: Claude Code skill 集合
- **特点**:
  - "TDD 驱动"工作流
  - 多个 skill 协作完成复杂任务
  - 用 `superpowers:` 前缀路由 skill
- **可借鉴**:
  - **三档分流**（quick / standard / deep）— EM-SKILL new 三档分流直接借鉴
  - **skill frontmatter 模板**
  - **skill 路由表**（哪个 skill 触发哪个流程）

### 2.2 关键 skill
- `brainstorming` — 需求澄清（EM-SKILL 的 `discussion-flow.md` 类似）
- `writing-plans` — 设计文档（EM-SKILL 的 `milestones.md` 类似）
- `test-driven-development` — TDD 流程
- `verification-before-completion` — 验证门控

### 2.3 与 EM-SKILL 的对比
| 维度 | Superpowers | EM-SKILL |
|------|-------------|----------|
| 主入口 | `superpowers:brainstorming` | `/em new` |
| 状态文件 | 无（依赖 CC 会话）| `state.md`（≤50 行）|
| 项目类型 | 不区分 | 通用 / 嵌入式 二选一 |
| HVR 流程 | 用 TDD 替代 | 独立 HVR workflow |
| 插件机制 | 纯 skill 集合 | 通用核 + 嵌入式插件 |

---

## 3. Model Context Protocol（🟢 高置信）

### 3.1 协议本身
- **URL**: https://modelcontextprotocol.io
- **GitHub**: https://github.com/modelcontextprotocol
- **版本**: 2024-11 发布，2025 多次迭代
- **核心概念**:
  - **MCP Server**: 提供 tools / resources / prompts
  - **MCP Client**: 消费 server 能力的客户端（如 Claude Code）
  - **Transport**: stdio / SSE / WebSocket
- **可借鉴**:
  - **三分类模型**: tools（行为）/ resources（数据）/ prompts（模板）
  - **JSON-RPC 协议**（标准消息格式）
  - **capability 协商**

### 3.2 MCP server 目录结构（参考 `mcp-server-filesystem`）
```
mcp-server-<name>/
├── README.md
├── pyproject.toml / package.json
├── src/
│   └── server.py
├── tests/
└── examples/
```

### 3.3 EM-SKILL 嵌入式工具现状
- `EM-SKILL/plugins/embedded/tools/serial-mcp/` **已经是 MCP server**（mcp_server.py + mcp_client.py）
- 缺：MCP 配置文件（`mcp_config.json`）

### 3.4 `modelcontextprotocol/servers` 仓库
- **URL**: https://github.com/modelcontextprotocol/servers
- 官方参考实现列表
- 包含：filesystem / git / github / postgres / puppeteer 等
- **可借鉴**: 各类 server 的 `package.json` / manifest 设计

---

## 4. 元仓库 / Skill 集合（🟡 中置信）

### 4.1 `hesreallyhim/awesome-claude-code`
- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **类型**: CC 资源聚合
- **可借鉴**: skill 分类法 / 命名规范

### 4.2 `getAsterisk/claudia`
- **URL**: https://github.com/getAsterisk/claudia
- **类型**: CC 桌面 GUI
- **可借鉴**: plugin 启用 UI / 市场浏览

### 4.3 `eyaltoledano/claude-task-master`
- **URL**: https://github.com/eyaltoledano/claude-task-master
- **类型**: 任务管理 skill
- **可借鉴**: workflow + agents 组合模式

### 4.4 其他可能的参考
- 🟠 `punkpeye/awesome-mcp-servers` — MCP 资源聚合
- 🟠 `ComposioHQ/composio` — 工具集成平台
- 🟠 `langchain-ai/langchain` — 工具调用框架（早期参考）

---

## 5. 关键设计决策（基于上述参考）

### 5.1 EM-SKILL 定位
- **不是** skill 集合（像 superpowers）
- **不是** 通用 AI 编程工具（像 Cursor / Continue）
- **而是**：**嵌入式开发的工作流管家 + 通用项目管理器**，以 **plugin 形式** 扩展场景

### 5.2 借鉴优先级
| 借鉴源 | 借鉴内容 | 优先级 |
|--------|----------|--------|
| Claude Code Plugin | plugin.json 字段 + 启用机制 | 🟢 P0 |
| MCP 协议 | tools/resources/prompts 分类 + mcp_config | 🟢 P0 |
| Superpowers | 三档分流 + frontmatter 模板 | 🟡 P1 |
| Anthropic Skills | 目录布局 + description 写法 | 🟡 P1 |

### 5.3 EM-SKILL Plugin v1.0 关键选择
- ✅ 沿用 **PLUGIN.md** 作为 plugin manifest（不用 plugin.json，更符合 CC skill 风格）
- ✅ 沿用 **frontmatter + Markdown** 形式（与 SKILL.md 风格一致）
- ✅ 借鉴 MCP 协议：**显式声明 mcp_servers**
- ✅ 借鉴 CC Plugin：**显式声明 hooks / agents / commands**
- ✅ 借鉴 Superpowers：**frontmatter 模板 + 路由表**

---

## 6. 待用户验证的项

由于无法实时访问，下列项目**细节可能不准确**，请用户确认或补充：

1. ☐ `anthropics/skills` 是否仍存在？目录结构是否变化？
2. ☐ `obra/superpowers` 最新版的 frontmatter 模板
3. ☐ Claude Code Plugin 系统的最新 spec（`/plugin` 命令是否仍是入口？）
4. ☐ MCP 协议最新版本号和 capability 列表
5. ☐ EM-SKILL 是否需要兼容 Claude Code 原生 plugin？还是独立体系？

---

## 7. 参考引用

### 7.1 内部引用
- [[PLUGIN-SPEC]] — EM-SKILL Plugin v1.0 规范（基于本调研产出）
- [[embedded/PLUGIN]] — 嵌入式插件（应用规范）
- [[SKILL]] — 通用核入口

### 7.2 外部链接（待用户验证可访问性）
- https://github.com/anthropics/skills
- https://github.com/anthropics/claude-cookbooks
- https://github.com/obra/superpowers
- https://github.com/modelcontextprotocol
- https://github.com/modelcontextprotocol/servers
- https://modelcontextprotocol.io
