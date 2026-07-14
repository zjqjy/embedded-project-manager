# EM-SKILL Plugin v1.0 规范

**版本**: v1.0
**日期**: 2026-07-01
**状态**: 草案
**作者**: Claude（基于 [[research/2026-07-01-github-references]] 产出）

---

## 0. 概述

EM-SKILL 采用「**通用核 + 插件**」架构。通用核（`SKILL.md`）提供 16 个核心命令；插件（`PLUGIN.md`）按需扩展场景能力。

本规范定义 **Plugin v1.0** 的目录布局、frontmatter schema、生命周期、依赖关系与启用机制。

### 0.1 设计目标
1. **物理解耦**：插件可独立增删，不影响通用核
2. **声明式**：所有元数据写在 `PLUGIN.md` frontmatter，运行时无需解析目录
3. **可发现**：通过 `INDEX.md` 集中索引所有插件
4. **可组合**：插件间可声明依赖（`depends`）/ 冲突（`conflicts`）
5. **可扩展**：frontmatter schema 版本化，向后兼容

### 0.2 兼容性
- 与 Claude Code 原生 plugin 系统**并行不冲突**（EM-SKILL 插件用 `.em/PLUGIN.md` 而非 `~/.claude/plugins/`）
- 与 MCP 协议**深度集成**（嵌入式工具的 MCP server 显式注册）
- 与 Superpowers 风格**相似但不等同**（frontmatter 字段借鉴但不强制统一）

---

## 1. 目录布局

### 1.1 仓库级布局
```
EM-SKILL/
├── SKILL.md                      # ⭐ 通用核入口（v3.0+）
├── commands/                     # 通用核命令
│   ├── rec.md
│   ├── new.md
│   └── ...
├── workflows/                    # 通用核工作流
│   ├── hvr-workflow.md
│   ├── new-light.md
│   └── ...
├── templates/                    # 通用核模板
│   ├── state.md
│   └── ...
├── tools/                        # 通用核工具
│   └── git-changelog/
├── plugins/                      # ⭐ 插件目录
│   ├── INDEX.md                  # ⭐ 插件索引
│   └── <plugin-name>/            # 单个插件
│       ├── PLUGIN.md             # ⭐ 插件 manifest
│       ├── commands/             # 插件命令（可选）
│       ├── workflows/            # 插件工作流（可选）
│       ├── templates/            # 插件模板（可选）
│       ├── tools/                # 插件工具（可选）
│       ├── mcp-servers/          # MCP server 配置（可选）
│       └── README.md             # 插件说明（可选）
└── docs/                         # 规范文档
    ├── PLUGIN-SPEC.md            # 本文件
    └── research/                 # 调研报告
```

### 1.2 插件目录命名
- 全小写、连字符分隔
- 简短、有意义：`embedded` `web` `ml` `data-pipeline` ...
- 避免通用词：`plugin` `extension` `addon` 是保留名

---

## 2. PLUGIN.md Frontmatter Schema

### 2.1 完整示例
```yaml
---
plugin: embedded                        # 必填：插件 ID（与目录名一致）
version: 1.0.0                          # 必填：插件语义化版本
description: 嵌入式开发场景插件          # 必填：一句话说明
min_skill_version: 3.0.0                # 推荐：依赖的 EM-SKILL 最低版本
author: zjq <zjq@example.com>           # 可选
license: MIT                            # 可选

# 启用条件（与项目状态文件 project.json 匹配时加载）
enabled_when:
  - project.json.type == "embedded"
  - 或 *.uvprojx / *.ioc / sdkconfig / platformio.ini 存在

# 提供能力清单（运行时可查询）
provides:
  commands:                             # 新增命令
    - name: initem
      file: commands/initem.md
      summary: 工具初始化（OpenOCD/Keil/串口路径）
    - name: build
      file: commands/build.md
      summary: 编译（Keil）
    - name: flash
      file: commands/flash.md
      summary: 烧录（OpenOCD）
    - name: serial
      file: commands/serial.md
      summary: 串口监控

  workflows:                            # 注入到通用命令的工作流
    - name: chip-learning
      file: workflows/chip-learning.md
    - name: verify-embedded
      file: workflows/verify-embedded.md
      inject_into: verify                # 注入到 /em verify

  tools:                                # 可调用工具（脚本）
    - name: build-keil
      path: tools/build-keil/scripts/keil_builder.py
      kind: python
    - name: flash-openocd
      path: tools/flash-openocd/scripts/openocd_flasher.py
      kind: python
    - name: serial-monitor
      path: tools/serial-monitor/scripts/serial_monitor.py
      kind: python

  templates:                            # 状态文件模板
    - name: serial-log-reference
      path: templates/serial-log-reference.md
    - name: serial-config
      path: templates/serial_config.json

  mcp_servers:                          # 提供的 MCP servers
    - name: serial-mcp
      config: mcp-servers/serial-mcp.json
      transport: stdio
      command: python tools/serial-mcp/mcp_server.py

  hooks:                                # 钩子（PreToolUse/PostToolUse 等）
    - event: PostToolUse
      matcher: Bash
      command: "echo 'EM-SKILL embedded: build/flash/serial logged'"
      script: hooks/post-build.sh

  agents:                               # 子代理（如有）
    - name: chip-identifier
      file: agents/chip-identifier.md
      description: 自动识别芯片型号

# 依赖与冲突
depends:                                # 依赖其他插件
  - core                                  # 始终依赖通用核
conflicts:                              # 冲突插件
  - legacy-embedded

# 元数据
tags: [embedded, mcu, stm32, keil, openocd]
keywords: 单片机 嵌入式 串口 烧录
---
```

### 2.2 字段详表

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `plugin` | ✅ | string | 插件 ID，**必须与目录名一致** |
| `version` | ✅ | semver | 插件版本，遵循 semver 2.0 |
| `description` | ✅ | string | 一句话说明（≤80 字符） |
| `min_skill_version` | ⚠️ 推荐 | semver | 依赖的 EM-SKILL 最低版本 |
| `author` | — | string | 维护者 |
| `license` | — | string | 许可证 |
| `enabled_when` | ✅ | array | 启用条件列表（**OR 语义**）|
| `provides.commands` | — | array | 提供的命令 |
| `provides.workflows` | — | array | 注入的工作流 |
| `provides.tools` | — | array | 可调用工具 |
| `provides.templates` | — | array | 模板 |
| `provides.mcp_servers` | — | array | MCP servers |
| `provides.hooks` | — | array | 钩子 |
| `provides.agents` | — | array | 子代理 |
| `depends` | — | array | 依赖的其他插件 ID |
| `conflicts` | — | array | 冲突的插件 ID |
| `tags` | — | array | 标签 |
| `keywords` | — | array | 关键词 |

### 2.3 `enabled_when` 语法

支持以下条件（**OR 列表**）：

| 条件 | 说明 |
|------|------|
| `project.json.type == "embedded"` | 严格匹配 project.json |
| `*.uvprojx` 存在 | 工作区有 Keil 工程 |
| `*.ioc` 存在 | 工作区有 CubeMX 工程 |
| `sdkconfig` 存在 | 工作区有 ESP-IDF 工程 |
| `platformio.ini` 存在 | 工作区有 PlatformIO 工程 |
| `<STATE_DIR>/embedded.json` 存在 | 用户显式标记 |

未来扩展：`project.json.plugins contains "embedded"` 等

---

## 3. Plugin Lifecycle

### 3.1 状态机

```
                    ┌────────────┐
                    │  Installed │  ← 文件存在 plugins/<name>/PLUGIN.md
                    └─────┬──────┘
                          │ /em rec / /em init / /em si 触发扫描
                          ▼
                    ┌────────────┐
                    │  Detected  │  ← enabled_when 匹配
                    └─────┬──────┘
                          │ /em rec 完成加载
                          ▼
                    ┌────────────┐
                    │   Loaded   │  ← 路由表已合并到 SKILL.md
                    └─────┬──────┘
                          │ /em rec 后续访问
                          ▼
                    ┌────────────┐
                    │   Active   │  ← 命令可调用
                    └────────────┘

                    ┌────────────┐
                    │  Disabled  │  ← project.json.plugins 不含本插件 / 手动 /em plugin disable
                    └────────────┘
```

### 3.2 加载流程
1. **`/em rec` / `/em init` / `/em si`** 扫描 `EM-SKILL/plugins/*/PLUGIN.md`
2. 解析每个 `PLUGIN.md` 的 frontmatter
3. 对每个插件检查 `enabled_when`，匹配则标记为 `Detected`
4. 合并 `provides.commands` 到通用核路由表（`SKILL.md` 路由表）
5. 合并 `provides.workflows.inject_into` 到对应通用命令
6. 完成 `Loaded` 状态
7. 用户输入 `/em <command>` 时进入 `Active` 状态

### 3.3 卸载流程
- 物理卸载：删除 `EM-SKILL/plugins/<name>/` 整目录
- 项目级禁用：在 `<STATE_DIR>/project.json` 中 `"plugins": []` 不含本插件
- 冲突禁用：`conflicts` 列表中的另一个插件已加载 → 本插件不加载

---

## 4. 命令路由

### 4.1 路由表合并规则
通用核 `SKILL.md` 的「子命令路由」表格在加载插件后**追加**插件命令：

```markdown
### 嵌入式插件命令（按需加载）

| `$0` | 读取的文件 |
|------|-----------|
| `initem` | `plugins/embedded/commands/initem.md` |
| `build` | `plugins/embedded/commands/build.md` |
| `flash` | `plugins/embedded/commands/flash.md` |
| `serial` | `plugins/embedded/commands/serial.md` |
```

### 4.2 工作流注入
`provides.workflows[].inject_into` 声明该工作流注入到哪个通用命令：

| 通用命令 | 注入点 |
|----------|--------|
| `/em verify` | 嵌入式 verify 子流程（编译/烧录/串口）|
| `/em init` | 芯片选择 + 工具链 |
| `/em si` | 嵌入式特征扫描 |
| `/em new` | 嵌入式需求维度（硬件/协议/实时性等）|

注入方式：通用命令执行时**首先**调用注入的工作流，**然后**走通用逻辑。

### 4.3 冲突处理
- 多个插件提供同名命令 → 报错并要求用户 `disable` 其一
- 插件命令与通用核命令同名 → 插件**覆盖**通用核（带 warning）

---

## 5. MCP Server 集成

### 5.1 mcp-servers/ 配置目录
每个 MCP server 配一个 `<name>.json`：

```json
// plugins/embedded/mcp-servers/serial-mcp.json
{
  "name": "serial-mcp",
  "version": "1.0.0",
  "transport": "stdio",
  "command": "python",
  "args": ["${PLUGIN_DIR}/tools/serial-mcp/mcp_server.py"],
  "env": {
    "SERIAL_CONFIG": "${PLUGIN_DIR}/tools/serial-mcp/serial_config.json"
  },
  "capabilities": {
    "tools": ["serial_read", "serial_status", "serial_send", "serial_log_file"]
  }
}
```

### 5.2 变量替换
- `${PLUGIN_DIR}` — 插件根目录绝对路径
- `${SKILL_DIR}` — 通用核根目录绝对路径
- `${STATE_DIR}` — 项目状态目录绝对路径

### 5.3 启用流程
1. `/em initem` 读取 `plugins/embedded/mcp-servers/serial-mcp.json`
2. 替换变量写入 `~/.claude/settings.json` 的 `mcpServers` 字段
3. Claude Code 重启时自动加载 MCP server

---

## 6. Hooks

### 6.1 支持的事件
| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `PreToolUse` | 工具调用前 | 拦截/校验 |
| `PostToolUse` | 工具调用后 | 日志/清理 |
| `Stop` | 会话结束 | 归档/提交 |
| `SessionStart` | 会话开始 | 恢复项目 |

### 6.2 Hook 配置示例
```yaml
hooks:
  - event: PostToolUse
    matcher: Bash           # 工具名匹配（支持通配符）
    command: "echo 'embedded tool used'"
  - event: Stop
    script: hooks/on-stop.sh
```

### 6.3 路径
- `command` 字符串命令
- `script` 相对插件根目录的脚本路径

---

## 7. 版本与兼容性

### 7.1 版本策略
- 插件版本遵循 **semver 2.0**：`MAJOR.MINOR.PATCH`
- `MAJOR` 不兼容 → 必须修改 `min_skill_version` 或 `plugin` ID
- `MINOR` 新增能力 → 向后兼容
- `PATCH` bugfix → 透明升级

### 7.2 `min_skill_version` 校验
- 加载插件时检查通用核版本 ≥ `min_skill_version`
- 不满足则警告但不阻止（让用户决定）

### 7.3 Schema 演进
- `PLUGIN-SPEC.md` 自身有版本号（v1.0）
- 新增字段用 `*_v2` 后缀，向后兼容
- 字段重命名/删除需 major version bump

---

## 8. 插件索引（INDEX.md）

### 8.1 位置
`EM-SKILL/plugins/INDEX.md`

### 8.2 格式
```markdown
# EM-SKILL Plugin Index

**最后更新**: 2026-07-01
**总数**: 1
**已启用**: 0（项目级）

## 内置插件

| ID | 版本 | 描述 | 启用条件 |
|----|------|------|----------|
| `embedded` | 1.0.0 | 嵌入式开发场景插件 | `project.json.type == "embedded"` 或 Keil/CubeMX/ESP-IDF/PlatformIO 工程 |

## 第三方插件

（待扩展）

## 添加插件

1. 创建 `EM-SKILL/plugins/<plugin-name>/`
2. 写 `PLUGIN.md` 遵循本规范
3. 在本 INDEX.md 追加一行
4. 提交 PR
```

---

## 9. 相关文档

- [[research/2026-07-01-github-references]] — GitHub 参考项目调研
- [[SKILL]] — 通用核入口
- [[plugins/embedded/PLUGIN]] — 嵌入式插件示例（应用本规范）

## 10. 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-01 | 初版（基于 S11 物理解耦 + remote merge 整合）|
