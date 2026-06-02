# EM-SKILL 嵌入式使用场景与迁移指南

> 本文档说明嵌入式项目下 EM-SKILL 的完整使用场景：智能识别、工具索引、典型工作流、迁移指南。
> 适用于 `S10-C` 之后的项目（v2.0+），可作为嵌入式项目从存量 `.emv2/` 升级到 `.em/` 的参考。

---

## 目录

1. [项目类型智能识别](#1-项目类型智能识别)
2. [工具索引（嵌入式专属）](#2-工具索引嵌入式专属)
3. [嵌入式项目典型工作流](#3-嵌入式项目典型工作流)
4. [S5/S7/S9 已完成能力](#4-s5s7s9-已完成能力)
5. [迁移指南：`.emv2/` → `.em/`](#5-迁移指南-emv2--em)
6. [常见问题](#6-常见问题)

---

## 1. 项目类型智能识别

EM-SKILL 在 `/em init` 初始化时自动扫描项目根目录的嵌入式特征文件，无需用户手动指定。

### 1.1 特征扫描规则

按以下顺序扫描项目根目录（含一层子目录）：

| 检测项 | 特征文件 / 模式 | 判定结果 |
|--------|----------------|----------|
| Keil MDK | `*.uvprojx`、`*.uvproj` | 嵌入式（ARM/Keil） |
| STM32CubeMX | `*.ioc` | 嵌入式（STM32） |
| ESP-IDF | `sdkconfig`、`CMakeLists.txt` 含 `idf_component_register` | 嵌入式（ESP32） |
| PlatformIO | `platformio.ini` | 嵌入式（跨平台） |
| Arduino | `*.ino` | 嵌入式（Arduino） |
| IAR | `*.eww`、`*.ewp` | 嵌入式（IAR） |
| Makefile (GCC) | `Makefile` 含 `arm-none-eabi-` 等交叉编译链 | 嵌入式（GCC） |

### 1.2 判定逻辑

```
扫描结果 = ∅ ?
  ├── 是 → 项目类型不明确，询问用户
  │        提示：「未检测到嵌入式特征文件。是否启用嵌入式场景工具？」
  │        选项：[1] 通用项目  [2] 嵌入式项目
  │
  └── 否 → 命中至少一项特征
           判定 = 嵌入式项目
           提示：「检测到 [特征列表]，自动启用嵌入式场景工具 (.em/embedded/)」
```

### 1.3 嵌入式 vs 通用项目

| 项目类型 | 状态目录 | 嵌入式工具 | 典型命令 |
|----------|----------|------------|----------|
| 嵌入式 | `.em/` + `.em/embedded/` | 串口/烧录/编译/芯片学习 | `/em initem`、串口监控 |
| 通用 | `.em/` | 不加载 | 跳过 S5/S7/S9 嵌入式能力 |

### 1.4 智能识别命中时

- 自动创建 `.em/` 目录结构
- 自动加载嵌入式工具索引
- 仅打印提示信息，不打断用户

### 1.5 智能识别不明确时

弹出选择菜单：

```
项目类型识别

未检测到嵌入式特征文件（Keil/CubeMX/ESP-IDF/PlatformIO 等）。

请选择项目类型：
  1. 通用项目（Web/脚本/库开发等）
  2. 嵌入式项目（MCU/固件开发）

输入选择 (1-2): _
```

---

## 2. 工具索引（嵌入式专属）

EM-SKILL 集成 4 个嵌入式工具，全部位于 `EM-SKILL/tools/` 目录。调用方式：通过 `~/.claude/settings.json` 中配置的 MCP/CLI 工具直接调用。

### 2.1 工具清单

| 工具 | 路径 | 用途 | 步骤 | 调用方式 |
|------|------|------|------|----------|
| `serial-mcp` | `EM-SKILL/tools/serial-mcp/` | 串口 GUI 工具（图形化监控） | S5 | MCP |
| `serial-monitor` | `EM-SKILL/tools/serial-monitor/` | 串口 CLI 工具（自动化） | S9 | CLI |
| `build-keil` | `EM-SKILL/tools/build-keil/` | Keil 编译脚本 | S9 | CLI |
| `flash-openocd` | `EM-SKILL/tools/flash-openocd/` | OpenOCD 烧录脚本 | S9 | CLI |

### 2.2 serial-mcp（串口 GUI）

**用途**：图形化串口监控工具，适合实时观察 MCU 输出。

**典型场景**：
- 调试阶段观察 `printf` 输出
- 多串口并行监控
- 协议解析（HEX/ASCII 自动识别）

**调用**：通过 MCP 工具名称 `serial-mcp` 直接调用，传入串口号与波特率。

### 2.3 serial-monitor（串口 CLI）

**用途**：命令行串口监控工具，适合自动化与脚本集成。

**典型场景**：
- CI/批处理中的串口日志采集
- 烧录后自动连接并校验启动日志
- 与 `result` 命令联动记录测试输出

**调用**：CLI 命令行调用，参数含串口、波特率、超时。

### 2.4 build-keil（Keil 编译）

**用途**：调用 Keil MDK 编译工程，输出 ELF/HEX/BIN。

**典型场景**：
- 自动化构建（替代手动点 Keil 的 Build 按钮）
- 与 `result` 命令联动记录编译产物
- CI 集成

**调用**：`build-keil/keil_build.sh <project.uvprojx>`。

### 2.5 flash-openocd（OpenOCD 烧录）

**用途**：通过 OpenOCD 烧录固件到目标 MCU（首选 STM32/GD32 等 ARM Cortex-M）。

**典型场景**：
- 自动化烧录（替代手动点 Keil 的 Download）
- JTAG/SWD 协议烧录
- 多板批量烧录

**调用**：`flash-openocd/openocd_flash.sh <interface> <target> <firmware>`。

**OpenOCD 安装指引**（嵌入式场景首次使用）：
- macOS：`brew install open-ocd`
- Linux：`sudo apt install openocd`
- Windows：下载预编译包并加入 PATH
- 详细：见 `/em initem` 输出的 OpenOCD 下载指引

### 2.6 工具集成入口

所有工具的安装与配置通过 `/em initem` 触发：

```
/em initem    # 检查并安装上述 4 个工具，更新 ~/.claude/settings.json
```

---

## 3. 嵌入式项目典型工作流

嵌入式项目在 `init` 后，按以下流程展开开发：

```
1. /em init <name>          # 智能识别为嵌入式项目，创建 .em/
2. /em initem               # 初始化工具（首次使用，配置 MCP/CLI）
3. /em rec                  # 恢复项目状态
4. /em new <功能描述>        # 进入新功能开发，自动分配 S 编号
5. /em disc                 # 讨论需求（产出 requirements/rules/hardware/milestones）
6. /em verify s<N>          # 验证步骤
7. 编译 → 烧录 → 串口 流程：
   - build-keil/keil_build.sh <project.uvprojx>
   - flash-openocd/openocd_flash.sh <interface> <target> <firmware>
   - serial-mcp 或 serial-monitor 监控
8. /em result s<N>-<result>  # 记录测试结果
9. /em arch                 # 归档已验证步骤
```

### 3.1 编译 → 烧录 → 串口 三件套

| 阶段 | 工具 | 脚本 | 产物 |
|------|------|------|------|
| 编译 | `build-keil` | `keil_build.sh <project.uvprojx>` | `.elf` / `.hex` / `.bin` |
| 烧录 | `flash-openocd` | `openocd_flash.sh <interface> <target> <firmware>` | 目标板已烧录 |
| 串口 | `serial-monitor` / `serial-mcp` | CLI / MCP | 启动日志、应用输出 |

### 3.2 自动化测试循环

嵌入式项目的典型测试循环（结合 `/em result`）：

```
编译成功 → 烧录成功 → 串口输出匹配预期 → 标记 PASS
                                              ↓
                                         写入 HVR 文件
                                              ↓
                                       /em arch 归档
```

---

## 4. S5/S7/S9 已完成能力

EM-SKILL 在 v2.0 之前已落地以下嵌入式能力，作为"使用场景"章节在 SKILL.md 中引用。

### 4.1 S5：串口 GUI 工具（serial-mcp）

- 图形化监控串口输出
- 支持多串口并行
- 自动协议解析（HEX/ASCII）
- 适合调试阶段实时观察

### 4.2 S7：测试结果记录

- `/em result <step>-<result>` 提交测试结果
- 状态自动推进（PASS / FAIL / BLOCKED）
- 写入 `checkpoints/HVR-S<X>-<N>.md` 文件
- 与 `/em verify` 联动

### 4.3 S9：嵌入式三件套

- **`serial-monitor`**（CLI）：自动化串口监控
- **`build-keil`**：Keil 编译脚本
- **`flash-openocd`**：OpenOCD 烧录脚本
- 三者通过 `~/.claude/settings.json` 配置的 CLI 工具调用

---

## 5. 迁移指南：`.emv2/` → `.em/`

### 5.1 何时迁移

**满足以下任一条件时建议执行 `/em migrate`**：

- 项目仍使用 `.emv2/` 目录（v1.x 时期的存量项目）
- 希望统一为 v2.0+ 的新格式
- EM 启动时打印了"建议运行 `/em migrate` 升级到 `.em/`"提示

### 5.2 迁移前准备

- 备份项目（虽然 `migrate` 设计为非破坏性，但备份是好习惯）
- 确认当前工作目录是项目根目录
- Windows 用户：如希望建立 `.emv2` 软链接回退，需开启「开发者模式」（Settings → Update & Security → For Developers）

### 5.3 迁移步骤

```
# 1. 在项目根目录执行
/em migrate

# 2. 查看迁移报告
# 输出示例：
# 复制统计: 文件 42 个，子目录 7 个
# 软链接模式: symlink (或 copy 在 Windows 无权限时)
# .emv2/ 保留为: 软链接 → .em/

# 3. 验证可正常恢复
/em rec
# 应打印：[EM] 检测到状态目录：.em/

# 4. （可选）测试回退
mv .em .em.bak
/em rec
# 应打印：[EM] 检测到状态目录：.emv2/  (旧格式回退)
mv .em.bak .em
```

### 5.4 迁移行为详解

`/em migrate` 不会破坏现有数据：

| 操作 | 行为 | 数据完整性 |
|------|------|------------|
| 创建 `.em/` | 新建空目录 | 100% |
| 复制 `.emv2/` → `.em/` | 递归 `shutil.copy2` 保留元数据 | 100% |
| 创建 `.emv2` 软链接 | 先删 `.emv2/` 目录再建链 | 100%（内容未丢） |
| 软链接失败（Windows） | 保留 `.emv2/` 目录作为独立副本 | 100% |

### 5.5 迁移后

- EM 启动逻辑自动优先读 `.em/`
- `.emv2/` 仍可作为回退（1-2 版本过渡期）
- 1-2 版本后（v2.1+）可手动删除 `.emv2/`

### 5.6 回滚迁移

如需回滚到迁移前状态：

```bash
# 方案 A：删除 .em/，把 .emv2 软链接换成 .emv2/ 目录
rm -rf .em
rm .emv2   # 删除软链接
# 从备份恢复 .emv2/ 目录（如有备份）

# 方案 B：如软链接未建立（Windows 副本模式）
# .emv2/ 目录还在，.em/ 是独立副本
# 直接删除 .em/ 即可
rm -rf .em
```

> 注：方案 A 中"从备份恢复"在大多数情况下不必要，因为 `.emv2/` 目录在迁移过程中未被破坏（软链接模式）或仍是独立副本（Windows 副本模式）。

---

## 6. 常见问题

### 6.1 迁移后 `.emv2/` 是什么形态？

- **Linux / macOS / Windows 开发者模式**：`.emv2` 是软链接，指向 `.em/`
- **Windows 普通模式**：`.emv2/` 仍是独立目录，与 `.em/` 内容相同

EM 启动逻辑通过 `get_state_dir()` 统一处理两种形态。

### 6.2 能否跳过 `.emv2/` 软链接直接删除？

可以，但不建议在过渡期（v2.0-v2.1）执行。建议保留 1-2 个版本，确认 EM 工具链无 `.emv2/` 兼容问题后再删除。

### 6.3 迁移失败如何处理？

迁移失败会触发回滚（删除已部分创建的 `.em/`），原 `.emv2/` 不受影响。检查错误信息后重试。

### 6.4 通用项目需要迁移吗？

不需要。通用项目使用 `init` 创建的就是 `.em/`，不存在迁移需求。`/em migrate` 仅针对存量 `.emv2/` 项目。

### 6.5 能否指定迁移后的目录名？

S10-C 决策为固定 `.em/`，不接受自定义。如有特殊需求，可手动 `mv .em <other>`，但 EM 工具链将无法识别。

---

## 相关命令

- `/em migrate` — 迁移命令本体
- `/em rec` — 迁移后验证
- `/em init` — 新项目初始化（嵌入式智能识别）
- `/em initem` — 嵌入式工具初始化

## 相关文件

- `commands/migrate.md` — 迁移命令完整定义
- `commands/init.md` — 智能识别 + `get_state_dir()` 函数
- `commands/rec.md` — 状态目录检测逻辑
- `EM-SKILL/SKILL.md` — 主入口（含工具索引章节）
- `EM-SKILL/tools/` — 4 个嵌入式工具的实际位置
