---
plugin: embedded
description: 嵌入式开发场景插件 — 串口、烧录、编译、芯片学习、嵌入式 verify 流程
provides:
  commands:
    - initem        # /em initem 工具初始化
  workflows:
    - chip-learning
    - verify-embedded
  tools:
    - build-keil
    - flash-openocd
    - serial-mcp
    - serial-monitor
    - shared (tool_config)
  templates:
    - serial-log-reference
    - serial_config.json
enabled_when:
  - project.json.type == "embedded"
  - 或检测到 Keil/CubeMX/ESP-IDF/PlatformIO 工程文件
---

# EM-SKILL · 嵌入式插件

> 嵌入式开发场景的完整能力集合，**通用核（EM-SKILL）与本插件物理解耦**。
> 通用项目（type=general）不加载本插件，零负担。

## 插件加载机制

1. **项目级启用**：`<STATE_DIR>/project.json` 中 `"type": "embedded"`
2. **自动检测**：`/em init` 或 `/em si` 时检测到以下任一特征 → 询问用户是否启用插件
   - `*.uvprojx` / `*.uvproj`（Keil 工程）
   - `*.ioc`（CubeMX 工程）
   - `sdkconfig` + `main/CMakeLists.txt`（ESP-IDF）
   - `platformio.ini`（PlatformIO）
   - `system_<stm32|gd32|ch32>f?xx.c` / `startup_*.s`
3. **手动启用**：`/em initem` 也会写入 `project.json.type = "embedded"`

## 插件入口路由

加载本插件后，SKILL.md 路由表自动追加以下命令：

| 命令 | 文件 |
|------|------|
| `/em initem` | `plugins/embedded/commands/initem.md` |

并对以下通用命令注入嵌入式分支：

| 命令 | 注入点 |
|------|--------|
| `/em verify` | 编译/烧录/串口子流程 → `plugins/embedded/workflows/verify-embedded.md` |
| `/em init` | 芯片选择 + 工具链选择 → `plugins/embedded/workflows/chip-learning.md` |
| `/em si` | 嵌入式特征扫描 → `plugins/embedded/workflows/chip-learning.md` |

## 嵌入式工具集

| 工具 | 路径 | 用途 |
|------|------|------|
| `serial-mcp` | `plugins/embedded/tools/serial-mcp/` | 串口 GUI（tkinter + MCP）|
| `serial-monitor` | `plugins/embedded/tools/serial-monitor/` | 串口 CLI（自动化抓日志）|
| `build-keil` | `plugins/embedded/tools/build-keil/` | Keil 编译脚本 |
| `flash-openocd` | `plugins/embedded/tools/flash-openocd/` | OpenOCD 烧录脚本 |
| `shared/tool_config.py` | `plugins/embedded/tools/shared/` | 工具路径配置共享库 |

调用方式：脚本通过 `~/.claude/settings.json` 中的路径白名单直接调用（`initem` 命令负责注册）。

## 嵌入式状态目录扩展

启用插件后，`<STATE_DIR>/` 额外使用以下目录（已存在结构，无需新建）：

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

物理卸载：删除 `plugins/embedded/` 整目录即可，通用核不依赖。
项目级停用：把 `project.json.type` 改回 `"general"`。

## 相关文件
- `commands/initem.md` — 工具初始化
- `workflows/chip-learning.md` — 芯片学习/识别
- `workflows/verify-embedded.md` — 嵌入式 verify 子流程（编译/烧录/串口）
- 通用核入口：`../../SKILL.md`
