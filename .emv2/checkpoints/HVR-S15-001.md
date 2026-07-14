# HVR — S15-A 插件 lazy-load loader 与缓存

**步骤**: S15-A — 写 `plugins/_loader.py` + 缓存机制
**验证时间**: 2026-07-14
**验证人**: zjq + Claude
**关联失败**: problem-log.md P3-1

---

## 验证目标

实现插件 lazy-load 的基础组件：
1. `plugins/_loader.py` — 解析所有 `PLUGIN.md`，构建 `{prefix → cmd → file}` 注册表
2. `<STATE_DIR>/cache/plugin-registry.json` — mtime 校验的缓存
3. CLI 入口支持：`--build` / `--query` / `--resolve` / `--list` / `--json`
4. 兼容两种 `provides.commands` 格式（PLUGIN-SPEC v1.0 对象形式 + learning 简单列表形式）

---

## 验证结果

### ✅ 单元测试（`plugins/tests/test_loader.py`）

| 测试组 | 通过/总数 |
|---|---|
| build 类（5 个：发现插件、命令总数、创建缓存、幂等、force 重建）| 5/5 |
| resolve 类（5 个：直接匹配、前缀拼接、多词后缀、找不到、空）| 5/5 |
| list 类（3 个：所有、过滤、无匹配）| 3/3 |
| format 兼容（2 个：对象形式 + 简单列表形式）| 2/2 |
| cache 失效（1 个：mtime 变更后重建）| 1/1 |
| **总计** | **16/16 ✅** |

### ✅ 集成测试（CLI）

| 调用 | 结果 |
|---|---|
| `python _loader.py --build` | ✓ 2 plugins, 7 commands |
| `python _loader.py --list` | ✓ 7 行输出 |
| `python _loader.py --resolve initem` | ✓ embedded/initem.md |
| `python _loader.py --resolve "learn new"` | ✓ learning/learn-new.md |
| `python _loader.py --resolve "learn verify"` | ✓ learning/learn-verify.md |
| `python _loader.py --resolve "learn status"` | ✓ learning/learn-status.md |
| `python _loader.py --resolve build` | ✓ embedded/build.md |
| `python _loader.py --resolve flash` | ✓ embedded/flash.md |
| `python _loader.py --resolve serial` | ✓ embedded/serial.md |
| `python _loader.py --resolve "nonexistent"` | ✓ exit=1, stderr 报错 |
| 缓存命中构建耗时 | 125 ms（含 Python 启动）|

### ✅ 缓存机制

- 缓存位置：`.em/cache/plugin-registry.json`（实际写入路径）
- 失效触发：任一 `PLUGIN.md` mtime 变更后立即重建
- 缓存格式：JSON，含 `version` / `built_at` / `plugins` / `registry` 四节

### ✅ 兼容性

| 项 | 状态 |
|---|---|
| Windows GBK console 编码 | ✓ 自动转 UTF-8（`sys.stdout` 重新包装）|
| 缺失 frontmatter 的 PLUGIN.md | ✓ WARN 跳过，不中断 |
| 命令文件路径不存在 | ✓ WARN 跳过，不中断 |
| 两种 `provides.commands` 格式 | ✓ 都解析（对象形式 + 简单列表形式）|

---

## 文件清单

### 新增

- `EM-SKILL/plugins/_loader.py` — 350 行（含 CLI + PluginLoader 类 + UTF-8 stdout fix）
- `EM-SKILL/plugins/tests/test_loader.py` — 16 个测试用例
- `.emv2/discussion/20260714-plugin-lazy-load/brainstorm.md`
- `.emv2/discussion/20260714-plugin-lazy-load/milestones.md`
- `.emv2/discussion/20260714-plugin-lazy-load/status.json`
- `.emv2/checkpoints/HVR-S15-001.md`（本文件）

### 修改

- `EM-SKILL/plugins/embedded/PLUGIN.md` — frontmatter 新增 `prefix: ""`
- `EM-SKILL/plugins/learning/PLUGIN.md` — frontmatter 新增 `prefix: learn`
- `.emv2/problem-log.md` — 记录 P3-1 失败
- `.emv2/state.md` — 当前步骤更新
- `.emv2/project-spec.md` — 步骤表 + 当前步骤更新

### 不入版本库

- `.em/cache/plugin-registry.json`（运行时产物，应加入 `.gitignore`）

---

## 关键设计决策

1. **`prefix` 字段**：每个 PLUGIN.md 声明 user-facing 前缀（embedded 空 / learning `learn`）
   - 解决「user 敲 `/em learn new`」与「PLUGIN.md 命令名 `learn-new`」的映射问题
2. **两种 commands 格式支持**：spec 对象形式 + learning 简单列表形式
   - 不破坏现有 PLUGIN.md，向后兼容
3. **mtime 缓存**：避免每次 `/em *` 都扫所有 PLUGIN.md（O(1) 查表）
4. **UTF-8 stdout**：Windows GBK 编码的中文输出自动修复
5. **resolve 双策略**：(1) 直接命令名匹配；(2) 前缀+后缀拼接

---

## 已知限制 / 后续步骤

- **S15-B**：SKILL.md 路由表指针化（仍为静态声明；动态 `_loader.py` 后续集成）
- **S15-D**：嵌入式 `enabled_when` 多文件探测移除（共用 `_loader.py` 缓存机制）
- **S15-E**：端到端验证 + 性能对比（trace 文件读取次数）

---

## 结论

✅ **S15-A 通过验证**，可提交。

下一步：commit → 进入 S15-B。