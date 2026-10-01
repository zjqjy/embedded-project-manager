---
plugin: embedded
version: 1.1.0
description: 嵌入式开发场景插件 — 串口、烧录、编译、芯片学习、嵌入式 verify 流程
min_skill_version: 3.0.0
author: zjq <2339311136@qq.com>
license: MIT
prefix: ""  # S15-A: user-facing prefix; empty = 顶层命令（/em initem 等）

# S15-D: 移除 5 类文件探测项（*.uvprojx / *.uvproj / *.ioc / sdkconfig / platformio.ini）
# 加载策略改为 lazy-load + 命令前缀触发；不再做文件系统 stat 探测
# 一次性项目类型识别由 /em init / /em si 完成，结果缓存到 <STATE_DIR>/cache/project-profile.json
# 兼容性保留 type==embedded 检测作为 legacy hint（不影响加载）
enabled_when:
  - project.json.type == "embedded"  # legacy: 仅作 default-plugin-hint，不控制加载

# 提供能力清单
provides:
  commands:
    - name: initem
      file: commands/initem.md
      summary: 工具初始化（OpenOCD/Keil/串口路径注册）
    - name: build
      file: commands/build.md
      summary: Keil 编译
    - name: flash
      file: commands/flash.md
      summary: OpenOCD 烧录
    - name: serial
      file: commands/serial.md
      summary: 串口监控（CLI/MCP）

  workflows:
    - name: chip-learning
      file: workflows/chip-learning.md
      inject_into: [init, si, new]
      summary: 芯片识别 + 工具链学习
    - name: verify-embedded
      file: workflows/verify-embedded.md
      inject_into: verify
      summary: 编译→烧录→串口三连子流程

  # S17-B: adapter 注册表 —— 芯片×动词×adapter，单一事实来源见 tools/registry.json
  tools:
    - name: build-keil
      path: tools/adapters/build/keil.py
      kind: python
      verb: build
    - name: build-ccs
      path: tools/adapters/build/ccs.py
      kind: python
      verb: build
    - name: flash-openocd
      path: tools/adapters/flash/openocd.py
      kind: python
      verb: flash
    - name: flash-dslite
      path: tools/adapters/flash/dslite.py
      kind: python
      verb: flash
    - name: observe-serial
      path: tools/adapters/observe/serial.py
      kind: python
      verb: observe
    - name: tool-config
      path: tools/lib/tool_config.py
      kind: python
      internal: true   # 内部共享，不直接调用
  registry: tools/registry.json   # 能力矩阵：chips.{vendor}.{family} → verb → adapter+args

  templates:
    - name: serial-log-reference
      path: templates/serial-log-reference.md
    - name: serial-config
      path: templates/serial_config.json
    - name: hvr-template-embedded
      path: templates/hvr-template-embedded.md

  mcp_servers:
    - name: serial-mcp
      config: mcp-servers/serial-mcp.json
      transport: stdio
      command: python tools/serial-mcp/mcp_server.py
      capabilities: [serial_read, serial_status, serial_send, serial_log_file]

  # hooks: 暂无（曾声明 hooks/log-build.sh 但文件从未存在，S17 review 移除；实现后再声明）

# 依赖与冲突
depends:
  - core
conflicts: []

# 元数据
tags: [embedded, mcu, stm32, gd32, keil, openocd, serial]
keywords: 单片机 嵌入式 串口 烧录 编译 芯片学习
---

# EM-SKILL · 嵌入式插件

> 嵌入式开发场景的完整能力集合，**通用核（EM-SKILL）与本插件物理解耦**。
> 通用项目（type=general）不加载本插件，零负担。

> **规范版本**：v1.0（遵循 [PLUGIN-SPEC](../../docs/PLUGIN-SPEC.md)）
> **SKILL 版本要求**：≥ 3.0.0

## 插件加载机制

1. **项目级启用**：`<STATE_DIR>/project.json` 中 `"type": "embedded"`
2. **自动检测**：`/em init` 或 `/em si` 时检测 `enabled_when` 条件（Keil/CubeMX/ESP-IDF/PlatformIO 工程）→ 询问用户是否启用插件
3. **手动启用**：`/em initem` 也会写入 `project.json.type = "embedded"`

详见 [PLUGIN-SPEC §1.3 启用条件](../../docs/PLUGIN-SPEC.md#13-enabled_when-语法)

## 插件入口路由

加载本插件后，SKILL.md 路由表自动追加以下命令：

| 命令 | 文件 |
|------|------|
| `/em initem` | `commands/initem.md` |
| `/em build` | `commands/build.md` |
| `/em flash` | `commands/flash.md` |
| `/em serial` | `commands/serial.md` |

并对以下通用命令注入嵌入式分支：

| 命令 | 注入点 |
|------|--------|
| `/em verify` | 编译/烧录/串口子流程 → `workflows/verify-embedded.md` |
| `/em init` | 芯片选择 + 工具链选择 → `workflows/chip-learning.md` |
| `/em si` | 嵌入式特征扫描 → `workflows/chip-learning.md` |
| `/em new` | 嵌入式需求维度（硬件/协议/实时性）→ `workflows/chip-learning.md` |

## 嵌入式工具集

| 工具 ID | 路径 | 用途 | 动词 |
|---------|------|------|------|
| `build-keil` | `tools/adapters/build/keil.py` | Keil 编译 adapter | build |
| `build-ccs` | `tools/adapters/build/ccs.py` | TI CCS headless 编译 adapter（S17-C）| build |
| `flash-openocd` | `tools/adapters/flash/openocd.py` | OpenOCD 烧录 adapter | flash |
| `flash-dslite` | `tools/adapters/flash/dslite.py` | TI DSLite 烧录 adapter（S17-C）| flash |
| `observe-serial` | `tools/adapters/observe/serial.py` | 串口 CLI adapter（自动化抓日志）| observe |
| `serial-mcp` | `tools/serial-mcp/` | 串口 GUI（tkinter + MCP）| — |
| `tool-config` | `tools/lib/tool_config.py` | 工具路径配置共享库（内部）| — |
| **registry** | `tools/registry.json` | **能力矩阵**：芯片×动词→adapter+参数（S17-B 单一事实来源）| — |

调用方式：脚本通过 `~/.claude/settings.json` 中的路径白名单直接调用（`initem` 命令负责注册）。

## MCP Server 集成

本插件提供 `serial-mcp` MCP server（stdio transport），提供 4 个工具：

| MCP 工具 | 说明 |
|----------|------|
| `serial_read` | 读取串口日志 |
| `serial_status` | 获取连接状态 |
| `serial_send` | 发送命令 |
| `serial_log_file` | 获取日志文件 |

启用方式：`/em initem` 读取 `mcp-servers/serial-mcp.json` 并注册到 `~/.claude/settings.json`。

详见：[`mcp-servers/serial-mcp.json`](mcp-servers/serial-mcp.json)

## 嵌入式状态目录扩展

启用插件后，`<STATE_DIR>/` 额外使用以下目录：

```
<STATE_DIR>/
├── logs/               # 串口/编译日志（serial_<step>_<time>.log）
└── embedded/           # 可选：芯片配置、引脚映射等（自管理）
```

## 何时**不**用此插件

- 纯软件项目（Web/App/CLI/库）
- 没有真实硬件、不需要烧录的项目
- 单片机模拟器 / QEMU 跑的项目（视情况）

## 卸载

- 物理卸载：删除 `EM-SKILL/plugins/embedded/` 整目录
- 项目级停用：把 `project.json.type` 改回 `"general"`
- 冲突禁用：本插件无冲突项

## 相关文件

- `commands/initem.md` `commands/build.md` `commands/flash.md` `commands/serial.md`
- `workflows/chip-learning.md` `workflows/verify-embedded.md`
- `tools/adapters/{build,flash,observe}/` + `tools/lib/` + `tools/registry.json` + `tools/serial-mcp/`
- `templates/{serial-log-reference.md, serial_config.json, hvr-template-embedded.md}`
- `mcp-servers/serial-mcp.json`
- 通用核入口：[`../../SKILL.md`](../../SKILL.md)
- 插件规范：[`../../docs/PLUGIN-SPEC.md`](../../docs/PLUGIN-SPEC.md)
- 插件索引：[`../INDEX.md`](../INDEX.md)

## 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-10-01 | S17-B/C：tools 重构为 `adapters/{build,flash,observe}/` + `lib/`；新增 `registry.json` 能力矩阵（芯片×动词×adapter 数据驱动）；新增 ccs/dslite adapter（TI，实测待做）；移除从未存在的 hooks 声明；verify-embedded/initem/build/flash/serial 改为组合驱动 |
| 1.0.0 | 2026-07-01 | 应用 PLUGIN-SPEC v1.0 规范；补全 frontmatter（version/requires/hooks/mcp_servers）；注册 build/flash/serial 三个新命令；添加 MCP server 配置引用 |
| 0.x | 2026-06-03 | S11 重构：物理解耦到 plugins/embedded/ |
| 0.x | 2026-05-09 | V0.1260509 工具整合（远程）|
