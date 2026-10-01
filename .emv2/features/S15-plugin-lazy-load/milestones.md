# milestones: S15-插件 lazy-load 重构

## 选定方案

**方案 B（路由表 + 插件 manifest 双层 + 启动时缓存）**

- 通用核只声明「插件目录索引」；每个插件 PLUGIN.md 仍声明 `provides.commands`
- **启动时一次性读所有 PLUGIN.md**，构建 `{prefix → cmd_file}` 映射并缓存到 `<STATE_DIR>/cache/plugin-registry.json`（带 mtime 校验）
- 命令执行时按缓存路由（O(1) 查表）
- 元仓库试用 learning 插件不再需要切 `project.json.type`

## 子步骤

### S15-A: 写 `plugins/_loader.py` + 缓存机制
- **内容**：新增 `EM-SKILL/plugins/_loader.py`；遍历 `plugins/*/PLUGIN.md` 解析 `provides.commands`；构建 `{prefix → cmd_file}` 映射；缓存到 `<STATE_DIR>/cache/plugin-registry.json`，带 mtime 校验
- **依赖**：无
- **验证**：`python plugins/_loader.py --build` 生成缓存；`--query learn new` 返回正确命令文件路径
- **预估**：M

### S15-B: SKILL.md 路由表指针化改造
- **内容**：SKILL.md 路由表从「16 命令清单 + 嵌入式 4 命令清单」改为「指针 + 前缀声明」；通用核不展开命令清单，由 `_loader.py` 提供
- **依赖**：S15-A 完成
- **验证**：读 SKILL.md 确认表项 ≤ 10 行（之前 20+ 行）；启动时一次性读 PLUGIN.md 总耗时 < 50ms
- **预估**：S

### S15-C: `project.json.type` 降级 + 元仓库 `trial_mode` 清理
- **内容**：`_type_enum` 增加 `null`；`type` 字段语义改为 `default-plugin-hint`（只影响 `/em help`）；删除元仓库 `trial_mode` 字段、`is_meta.trial_mode.since`；`type = "general"` 不再控制加载
- **依赖**：S15-B 完成
- **验证**：`project.json.type = "general"` 时 `/em learn new` 仍能正常加载 learning 插件
- **预估**：S

### S15-D: 嵌入式插件 `enabled_when` 多文件探测移除
- **内容**：删除 `plugins/embedded/PLUGIN.md` 里 `*.uvprojx` `*.uvproj` `*.ioc` `sdkconfig` `platformio.ini` 5 类文件探测项；改 `init` / `si` 时一次性识别 + 缓存到 `<STATE_DIR>/cache/project-profile.json`；运行时按缓存路由
- **依赖**：S15-A 完成（共用 `_loader.py` 缓存机制）
- **验证**：`/em stat` 不再触发 `*.uvprojx` 等文件 stat 调用（用 `strace` / `fs_usage` 验证）
- **预估**：M

### S15-E: 端到端验证 + 性能对比
- **内容**：
  1. 对比 `/em rec` / `/em stat` / `/em pi` 在重构前后的文件读取次数（用 trace）
  2. 验证 `/em learn new iic-test` 在 `type=general` 下能正常加载
  3. 验证 `/em initem` 在 `type=general` 下能正常加载（嵌入式插件）
  4. 验证元仓库 `trial_mode` 删除后 learning 插件仍可用
  5. 生成 `checkpoints/HVR-S15-001.md` 总结
- **依赖**：S15-A~D 全部完成
- **验证**：HVR 列出 5 项验证结果
- **预估**：M

## 关键决策（记入 decisions.md）

- [2026-07-14] S15: 插件加载从 eager/type 驱动改为 lazy/命令驱动；缓存策略采用「启动时一次性 + mtime 校验」
- [2026-07-14] S15: `project.json.type` 降级为 `default-plugin-hint`，不再控制加载
- [2026-07-14] S15: 元仓库 `trial_mode` 字段废弃；learning 插件按需触发

## 关联

- **失败记录**: `problem-log.md` P3-1（[2026-07-14] S14-失败-1）
- **架构文档**: `EM-SKILL/docs/PLUGIN-SPEC.md`（需 S15 完成后补充 lazy-load 章节）
- **设计档案**: `discussion/20260714-plugin-lazy-load/brainstorm.md`