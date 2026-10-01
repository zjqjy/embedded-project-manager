# 命令: /em init (项目初始化)

> **通用核版本**：先选项目类型，嵌入式特征自动加载 embedded 插件流程。

## 功能
从零开始新项目，生成 `<STATE_DIR>/` 标准结构。

## 触发
```
/em init <项目名称>                # 自动检测类型，给推荐
/em init <项目名称> --type=general  # 强制通用
/em init <项目名称> --type=embedded # 强制嵌入式（加载 embedded 插件）
```

## 执行流程（总入口）

1. **【目录检测】** 当前目录已有 `.em/` → 提示「项目已初始化」+ 给 `/em rec` 建议
   > 旧版 `.emv2/` 项目（v3.0 之前）请先 `/em migrate` 升级到 `.em/`
2. **【类型判定】**
   - 命令带 `--type=...` → 直接采用
   - 否则按下表启发式扫描，给推荐：

| 信号（任一命中）| 推荐类型 |
|------|---------|
| `*.uvprojx` / `*.uvproj` | embedded（Keil） |
| `*.ioc` | embedded（CubeMX） |
| `sdkconfig` + `main/CMakeLists.txt` | embedded（ESP-IDF） |
| `platformio.ini` | embedded（PlatformIO） |
| `*.ino` | embedded（Arduino） |
| `*.eww` / `*.ewp` | embedded（IAR） |
| `system_<stm32\|gd32\|ch32>f?xx.c` / `startup_*.s` | embedded |
| Makefile 含 `arm-none-eabi-` 等交叉编译链 | embedded |
| 上述均无 | general |

   - 输出推荐 + 让用户确认：
     ```
     📋 项目类型判定
        扫描结果: <匹配的特征，或"未命中"> 
        推荐类型: <general|embedded>
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        输入 `继续` 采用推荐，或 `general` / `embedded` 改选。
     ```

3. **【创建 `<STATE_DIR>/`】** 新项目默认 `.em/`，**最小生成**（S17-A 止血包：只建 2 个文件，其余首次写入时才创建）：
   ```
   .em/
   ├── state.md           # ✅ 创建（唯一恢复源，≤50 行）
   ├── project.json       # ✅ 创建（类型/插件元数据，含 embedded 锁定位）
   ├── features/          # 目录骨架（每步骤一目录；README 索引首次 new 时创建）
   ├── history/
   └── logs/
   # journal.md / problem-log.md 首次写入时创建（journal 条目由 result/arch 追加）
   ```
   > ❌ **不再预创建** project-spec.md / decisions.md / problem-log.md 空表头文件——
   > 分别由 `/em new`（写步骤表）、首次记决策、首次记问题时**首次写入自动创建**（套 templates/ 模板）。
   > 新项目 init 完成的文件产物 = 2 个。

4. **【按类型分支】**
   - **general**：到此结束 → 提示 `/em new <第一个功能>`
   - **embedded**：
     - 加载 `plugins/embedded/commands/initem.md`（工具初始化）
     - 加载 `plugins/embedded/workflows/chip-learning.md`（芯片选择 + chips.json 学习）
     - 写 `project.json.embedded = { chip, toolchain, interface }`
     - 完成后回到这里输出报告

5. **【更新全局索引】** `~/.claude/embedded-projects-index.md`（沿用名称，含通用+嵌入式所有项目）

6. **【写 state.md】** 首次状态：
   - 当前步骤: `S0`（待 `/em new` 创建第一个步骤）
   - 下一步动作: `/em new <功能描述>`

7. **【输出初始化完成报告】**

## 输出格式

### general 项目

```
✅ 通用项目初始化完成

项目: <名称>
路径: <绝对路径>
类型: general
状态目录: .em/

📁 已创建文件（最小生成，S17-A）:
  state.md / project.json + 空目录骨架
  （project-spec / decisions / problem-log 首次写入时自动创建）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
下一步:
  /em new <功能描述>   # 进入新功能开发（默认中档 superpower 风格）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### embedded 项目

```
✅ 嵌入式项目初始化完成

项目: <名称>
类型: embedded
芯片: <型号>
工具链: <Keil|IAR|GCC>
状态目录: .em/

📁 已创建文件: (同上)
🔌 已加载插件: plugins/embedded/ (PLUGIN.md)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
下一步:
  /em initem    # 工具初始化（首次使用 / 配置工具路径）
  /em new ...   # 新功能开发
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 设计原则

- ✅ 类型先选，能力按需加载（披露式）
- ✅ 通用项目零嵌入式负担
- ✅ 嵌入式项目 init 时自动跑插件初始化流
- ✅ 全局索引统一管理（不区分类型）

## 双轨制兼容（旧版回退）

新项目统一创建 `.em/`。所有命令读取项目状态用 `get_state_dir()`：

```python
def get_state_dir(project_root: str) -> str | None:
    em_dir = os.path.join(project_root, '.em')
    if os.path.isdir(em_dir): return em_dir
    return None
```

旧版 `.emv2/` 项目 → 请先 `/em migrate` 升级（v3.1 起 init/si 不再生成 `.emv2/`）。

## 相关文件
- `commands/rec.md` — 恢复时也读 `project.json` 决定是否加载嵌入式插件
- `commands/migrate.md` — 旧版 `.emv2/` → `.em/` 一次性迁移（v3.1 起 init/si 不再生成 `.emv2/`）
- `plugins/embedded/PLUGIN.md` — 嵌入式插件清单
- `plugins/embedded/commands/initem.md` — 嵌入式工具初始化
- `plugins/embedded/workflows/chip-learning.md` — 芯片学习/识别
