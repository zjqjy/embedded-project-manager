# brainstorm: S15-插件 lazy-load 重构

## 需求理解

当前 EM-SKILL 插件加载是「eager + type 驱动」架构：每次执行 `/em *` 命令时，SKILL.md 路由表会：
1. 读 `<STATE_DIR>/state.md` + `project.json`
2. 检查 `project.json.type` 字段
3. 嵌入式插件额外扫描 `*.uvprojx` `*.uvproj` `*.ioc` `sdkconfig` `platformio.ini` 共 5 类文件
4. 学习插件额外扫描 `.em/learning/state.md` `_index.json` 存在性

**核心问题**（来自 P3-1）：
- 即使用户本轮命令**完全用不到**插件，也要读完所有这些文件
- 元仓库试用 learning 插件必须改 `project.json.type = "learning"`，用完再改回 → `trial_mode` 字段是设计妥协痕迹
- 哲学上违反「按需加载」（类比 Linux `modprobe` / VS Code extension activation）

**S15 目标**：
- 改为「lazy + 命令驱动」——路由表启动时一次性建立，命令执行时按需读 1 个文件
- 元仓库不再需要 `trial_mode` 来回切
- `/em rec` / `stat` / `pi` 等非插件命令 → 零插件开销

## 候选方案

### 方案 A: SKILL.md 路由表硬编码（最小改动）
- **思路**：SKILL.md 路由表直接列出所有命令前缀→插件命令文件映射；删除所有 `enabled_when` 检测逻辑
- **优点**：
  - 改动最小（只动 SKILL.md 和 PLUGIN.md 解析逻辑）
  - 零运行时探测，性能立竿见影
  - 学习成本零（路由表就是文档）
- **缺点 / 风险**：
  - SKILL.md 路由表膨胀（每加一个插件命令都要改通用核）
  - 插件独立性下降（必须改通用核）
  - **与 v3.0 "通用核零业务"哲学冲突**
- **预估工作量**：S

### 方案 B: 路由表 + 插件 manifest 双层 + 启动时缓存 ⭐ (已选定)
- **思路**：
  1. 通用核只声明「插件目录索引」(`plugins/INDEX.md` 已知存在)
  2. 每个插件 PLUGIN.md 仍声明 `provides.commands`（保留自描述）
  3. **启动时一次性读所有 PLUGIN.md**，构建 `{prefix → cmd_file}` 映射并缓存到 `.em/cache/plugin-registry.json`
  4. 命令执行时按缓存路由（O(1) 查表）
- **优点**：
  - 哲学一致：保留插件独立性（PLUGIN.md 还是插件自描述）
  - 启动时一次性读取 ≈ 微秒级（不扫文件系统）
  - 运行时按命令前缀查缓存 → O(1)
  - 元仓库试用 learning **不再需要切 type**
- **缺点 / 风险**：
  - 启动时仍读所有 PLUGIN.md（vs 方案 A 零读取；但一次性 vs 当前每命令扫）
  - 缓存失效需 mtime 校验（修改 PLUGIN.md 后怎么办）
- **预估工作量**：M

### 方案 C: 纯 lazy 按需探测插件目录
- **思路**：完全不预读任何插件信息；用户敲 `/em learn new` 时扫描 `plugins/` 目录找到匹配的命令文件
- **优点**：零启动开销、零预读、完全按需
- **缺点 / 风险**：
  - 每命令都扫描 `plugins/` 目录（vs 缓存方案）
  - 命令路由错误信息不友好（用户敲错命令不知道去哪查）
  - 元数据完全隐藏在文件系统（IDE 不友好）
- **预估工作量**：M

## 推荐（已选定）

**方案 B（路由表 + 插件 manifest 双层 + 启动时缓存）**

理由：
1. **兼顾两边**：插件独立性（哲学不变）+ 运行时零开销（用户感知）
2. **改动集中**：SKILL.md + 一个轻量级 `plugins/_loader.py`（缓存逻辑）
3. **验证 P3-1 根本诉求**：元仓库试用 learning 不再需要切 type
4. **可演进**：未来加新插件只需写 PLUGIN.md 的 `provides.commands`，通用核零改动

## 关键技术点

1. **新增 `plugins/_loader.py`**
   - 遍历 `plugins/*/PLUGIN.md`，解析 `provides.commands`
   - 构建 `{prefix → cmd_file}` 映射
   - 缓存到 `.em/cache/plugin-registry.json`（带 mtime 校验）
   - 缓存失效：读 PLUGIN.md mtime 与缓存记录比对，不一致则重建

2. **SKILL.md 路由表改造**
   - 从「列出 16 个命令 + 嵌入式插件命令」改为「指针化」
   - 只声明已知插件前缀：`learn` / `initem` / `build` / `flash` / `serial` / `chip-learning` 等
   - 不再展开具体命令清单（由 `_loader.py` 提供）

3. **`project.json.type` 降级**
   - 从「加载开关」→ `default-plugin-hint`（UI 推荐用 / 默认偏好）
   - 不再控制加载行为，只影响 `/em help` 等命令的默认推荐
   - `_type_enum` 增加 `null` 选项（无默认偏好）

4. **元仓库清理**
   - 删 `trial_mode` 字段
   - `project.json.type = "general"`
   - learning 插件通过 `/em learn new` 触发加载，**无需切 type**

5. **嵌入式插件同步重构**
   - 移除 `enabled_when` 里 `*.uvprojx` `*.uvproj` `*.ioc` `sdkconfig` `platformio.ini` 5 类文件探测
   - 改 `init` / `si` 时一次性识别 + 缓存到 `.em/cache/project-profile.json`

6. **保留向后兼容**
   - 旧 `type == "embedded"` 项目依然可用（只是 type 不再控制加载）
   - `.emv2/` 旧项目兼容（state.md 读取路径不变）

## 子目标拆解（preview）

- S15-A: 写 `plugins/_loader.py` + `.em/cache/plugin-registry.json` 缓存逻辑
- S15-B: SKILL.md 路由表指针化改造
- S15-C: `project.json.type` 降级 + 元仓库 `trial_mode` 清理
- S15-D: 嵌入式 `enabled_when` 多文件探测移除 + `init`/`si` 一次性识别
- S15-E: 端到端验证（rec 学习 / stat 学习 / learn new / initem 各路径计时对比）

---

生成时间: 2026-07-14
S15 推荐档位: 中（brainstorm + milestones）
用户确认: 选 B