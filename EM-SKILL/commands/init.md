# 命令: /em init (项目初始化)

## 功能
从零开始新项目

## 触发
```
/em init <项目名称>
```

## 执行流程

1. **【项目类型智能识别】**（扫描嵌入式特征，详见下方「智能识别」章节）
2. **【芯片选择】**（支持 chips.json 中的已学习芯片，仅在识别为嵌入式时）
3. **询问开发环境**（Keil/IAR/GCC，仅在识别为嵌入式时）
4. **芯片学习**：用户选择/输入的芯片自动添加到全局 chips.json（仅在识别为嵌入式时）
5. **创建 .em/ 目录结构**（新项目使用 `.em/`，S10-B 通用化决策）
6. **创建 .em/project-spec.md**
7. **创建 .em/memory-log.md**
8. **更新全局索引** ~/.claude/embedded-projects-index.md
9. **输出初始化完成报告**

> ⚠️ **目录双轨制（S10-B）**：EM 优先识别 `.em/`，缺失时回退 `.emv2/`。
> 新建项目**统一创建 `.em/`**。详见末尾「动态检测逻辑」章节。

## 智能识别流程

init 命令在创建项目前会扫描项目根目录的嵌入式特征文件，自动判断项目类型。

### 1. 特征扫描规则

按以下顺序扫描项目根目录（含一层子目录）：

| 检测项 | 特征文件 / 模式 | 判定结果 |
|--------|----------------|----------|
| Keil MDK | `*.uvprojx`、`*.uvproj` | 🟢 嵌入式（ARM/Keil） |
| STM32CubeMX | `*.ioc` | 🟢 嵌入式（STM32） |
| ESP-IDF | `sdkconfig`、`CMakeLists.txt` 含 `idf_component_register` | 🟢 嵌入式（ESP32） |
| PlatformIO | `platformio.ini` | 🟢 嵌入式（跨平台） |
| Arduino | `*.ino` | 🟢 嵌入式（Arduino） |
| IAR | `*.eww`、`*.ewp` | 🟢 嵌入式（IAR） |
| Makefile (GCC) | `Makefile` 含 `arm-none-eabi-` 等交叉编译链 | 🟢 嵌入式（GCC） |

### 2. 判定逻辑

```
扫描结果 = ∅ ?
  ├── 是 → 项目类型不明确，询问用户
  │        提示：「未检测到嵌入式特征文件。是否启用嵌入式场景工具？」
  │        选项：[1] 通用项目  [2] 嵌入式项目
  │
  └── 否 → 命中至少一项特征
           判定 = 🟢 嵌入式项目
           提示：「检测到 [特征列表]，自动启用嵌入式场景工具 (.em/embedded/)」
```

### 3. 嵌入式 vs 通用项目

| 项目类型 | 状态目录 | 嵌入式工具 | 典型命令 |
|----------|----------|------------|----------|
| 🟢 嵌入式 | `.em/` + `.em/embedded/` | 串口/烧录/编译/芯片学习 | `/em initem`、串口监控 |
| ⚪ 通用 | `.em/` | 不加载 | 跳过 S5/S7/S9 嵌入式能力 |

### 4. 用户确认环节

智能识别**不明确**时，弹出选择菜单：

```
🔍 项目类型识别

未检测到嵌入式特征文件（Keil/CubeMX/ESP-IDF/PlatformIO 等）。

请选择项目类型：
  1. ⚪ 通用项目（Web/脚本/库开发等）
  2. 🟢 嵌入式项目（MCU/固件开发）

输入选择 (1-2): _
```

> 💡 智能识别**命中**时**不询问**用户，直接创建对应结构，仅打印提示信息。

## 芯片选择界面

```
📋 芯片选择

【已学习芯片】
1. GD32F407VET6 (GigaDevice) [最近: 2026-03-27]
2. STM32F407VET6 (ST) [最近: 2026-03-26]

【内置芯片 - ST】
3. STM32F103C8T6
4. STM32F405RGT6

【内置芯片 - GigaDevice】
5. GD32F405RGT6

【内置芯片 - WCH】
6. CH32V103C8T6
7. CH32V203C8T6

───────────────────────────────────
请选择 (1-7) 或输入芯片型号: _
```

> 注：芯片选择仅在识别为**嵌入式项目**时显示。

## 动态检测逻辑（统一规范）

EM 所有命令读取项目状态时，使用统一的目录检测函数：

```python
def get_state_dir(project_root: str) -> str | None:
    """
    S10-B 目录通用化：优先读 .em/，缺失时回退 .emv2/。

    返回:
        str  - 状态目录绝对路径（.em/ 或 .emv2/）
        None - 项目未初始化
    """
    em_dir   = os.path.join(project_root, '.em')
    emv2_dir = os.path.join(project_root, '.emv2')

    if os.path.isdir(em_dir):
        return em_dir       # 优先新格式
    elif os.path.isdir(emv2_dir):
        return emv2_dir     # 向后兼容旧格式
    else:
        return None         # 未初始化
```

**在命令文档中的引用规范**：

| 场景 | 文档写法 |
|------|----------|
| 读取现有项目状态 | `<STATE_DIR>/project-spec.md`（其中 `<STATE_DIR>` 由 `get_state_dir()` 解析） |
| 创建新项目 | 直接写 `.em/`（init/si 流程固定创建新目录） |
| 展示示例路径 | 标注「示例：`.em/`」并加注「实际读取走 `get_state_dir()`」 |

**提示规范**：恢复/读取类命令（`rec`、`stat`、`sum`）在执行时应打印一行：

```
[EM] 检测到状态目录：.em/    (或 .emv2/ 当 .em/ 不存在时)
```

## 迁移支持

`/em init` 用于**从零创建**新项目。如需将存量 `.emv2/` 项目升级到新格式（`.em/`），请使用 `/em migrate` 命令。

### 何时使用 migrate 而非 init

| 场景 | 使用命令 |
|------|----------|
| 全新项目（无 `.emv2/` 也无 `.em/`） | `/em init <name>` |
| 已有 `.emv2/` 目录，希望升级为 `.em/` | `/em migrate` |
| 已有 `.em/` 目录 | 无需 init/migrate |

### migrate 与 init 的关键差异

- `init`：**创建**新状态目录，从空白开始
- `migrate`：**复制** `.emv2/` → `.em/`，保留原 `.emv2/` 作为回退
- `init` 不修改 `.emv2/`；`migrate` 不创建空目录外的任何新内容

### 相关命令

- `/em migrate` — 存量 `.emv2/` 项目迁移到 `.em/`
- 详细迁移流程见：`commands/migrate.md`
- 嵌入式使用场景详见：`templates/em-migration.md`

## 相关文件
- workflows/chip-learning.md - 芯片学习机制
- workflows/discussion-flow.md - 讨论流程
- commands/migrate.md - `.emv2/` → `.em/` 迁移命令（S10-C）
- templates/em-migration.md - 嵌入式使用场景与迁移指南（S10-C）
