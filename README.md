# EM-SKILL - 嵌入式项目开发管家

Claude Code 嵌入式项目管理技能，专注于固件开发场景的人机协作验证流程。

## 核心定位

```
EM-SKILL = 流程控制（verify 命令）+ 工具执行（build/flash/serial）
```

- **EM-SKILL**：流程编排、人工验证协调、项目状态管理
- **embed-ai-tool**：具体执行（编译、烧录、监控）

## 主要功能

| 命令 | 功能 |
|------|------|
| `/em verify s<N>` | 执行验证流程：编译 → 烧录 → 串口 |
| `/em new [功能]` | 新功能开发流程 |
| `/em disc [话题]` | 需求讨论流程 |
| `/em result <结果>` | 记录验证结果 |
| `/em initem` | 初始化工具环境 |
| `/em rec` | 恢复项目状态 |

## 内置工具（来源：LeoKemp223/embed-ai-tool）

### 编译：build-keil
Keil MDK 工程编译，支持多目标。

```bash
python EM-SKILL/tools/build-keil/scripts/keil_builder.py \
  --project ./project.uvprojx \
  --target "Target1"
```

### 烧录：flash-openocd
OpenOCD 统一烧录接口，支持 ST-Link、J-Link、CMSIS-DAP。

```bash
python EM-SKILL/tools/flash-openocd/scripts/openocd_flasher.py \
  --artifact build/firmware.axf \
  --interface stlink \
  --target target/stm32f4x.cfg
```

### 监控：serial-monitor
串口日志抓取，支持关键字等待、复位捕获。

```bash
python EM-SKILL/tools/serial-monitor/scripts/serial_monitor.py \
  --port COM5 \
  --baud 115200 \
  --duration 5 \
  --save .emv2/logs/serial_S9.log
```

## 工具来源

| 工具 | 来源 | 说明 |
|------|------|------|
| **build-keil** | [embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) | Keil MDK 编译 |
| **flash-openocd** | [embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) | OpenOCD 烧录 |
| **serial-monitor** | [embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) | 串口监控 |
| **OpenOCD** | [xPack OpenOCD](https://github.com/xpack-dev-tools/openocd-xpack) | 开源调试工具 |
| **Keil MDK** | [ARM/Keil](https://www.keil.com/) | 商业 IDE |
| **J-Link** | [SEGGER](https://www.segger.com/) | 商业调试器 |

> OpenOCD + ST-Link 是免费组合。Keil MDK 和 J-Link 需要商业许可证。

## 项目结构

```
embedded-project-manager/
├── EM-SKILL/              # EM-SKILL 技能定义
│   ├── commands/          # /em 命令定义
│   ├── tools/             # 整合的工具（来源：embed-ai-tool）
│   │   ├── build-keil/   # Keil 编译工具
│   │   ├── flash-openocd/ # OpenOCD 烧录工具
│   │   └── serial-monitor/ # 串口监控工具
│   ├── workflows/          # 工作流细则
│   └── templates/          # 模板文件
├── .emv2/                 # 项目元数据
│   ├── checkpoints/        # HVR 检查点文件
│   ├── discussion/         # 讨论记录
│   └── logs/              # 串口日志
└── README.md
```

## 快速开始

### 一、安装 EM-SKILL 技能

在 Claude Code 对话中输入：

```
帮我安装 https://github.com/zjqjy/embedded-project-manager.git 的 skill，指定 embed-ai-tool整合 分支
```

这会克隆整个项目仓库，其中包含：
- EM-SKILL 流程框架
- 内置工具（build-keil、flash-openocd、serial-monitor）

### 二、初始化工具环境

```bash
/em initem
```

这会自动：
1. 探测并注册工具路径（Keil、OpenOCD、J-Link）
2. 配置 Claude 权限

### 三、接入已有项目

```bash
/em si /path/to/project
```

### 四、开发流程

```
/em new [功能]   # 新功能开发
/em disc [话题]   # 需求讨论
/em verify s3     # 执行验证
/em result 通过   # 记录结果
```

## 验证流程

```
┌─────────────────────────────────────────────────────────┐
│  编译 (build-keil)                                   │
│  ├── 自动查找 .uvprojx 文件                          │
│  └── 输出：编译状态、产物路径、错误信息               │
└────────────────────────┬────────────────────────────────┘
                         │ 成功
┌────────────────────────▼────────────────────────────────┐
│  烧录 (flash-openocd)                                 │
│  ├── 自动探测调试器                                   │
│  └── 输出：烧录状态、校验结果                         │
└────────────────────────┬────────────────────────────────┘
                         │ 成功
┌────────────────────────▼────────────────────────────────┐
│  串口 (serial-monitor)                                │
│  ├── 自动保存日志到 .emv2/logs/                      │
│  └── 输出：启动日志、错误分析                         │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌─────────▼─────────┐
              │  用户口述观察结果  │
              └───────────────────┘
```

## 参考链接

- [embed-ai-tool (LeoKemp223)](https://github.com/LeoKemp223/embed-ai-tool)
- [xPack OpenOCD](https://github.com/xpack-dev-tools/openocd-xpack/releases)
- [SEGGER J-Link](https://www.segger.com/downloads/jlink/)
- [Keil MDK](https://www.keil.com/mdk5/)

## 致谢

本项目整合了 [LeoKemp223/embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) 的优秀工具，感谢小智学长的开源贡献！
