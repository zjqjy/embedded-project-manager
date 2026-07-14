# LPR 学习模式 — Milestones (落地步骤)

> 配套 brainstorm.md。本里程碑表为中档"标准"产出，按顺序执行。

## 总览

| 步骤 | 名称 | 产出 | 估时 |
|------|------|------|------|
| M0 | 状态目录初始化 | `.em/learning/` 骨架 | 5 min |
| M1 | 模板落地 | `knowledge.md` + `video-script.md` | 15 min |
| M2 | 命令文件落地 | 4 个新 `commands/*.md` | 20 min |
| M3 | SKILL.md 路由表更新 | `EM-SKILL/SKILL.md` | 10 min |
| M4 | 嵌入式插件联动 | serial-mcp 自动录屏 | 15 min |
| M5 | state.md 瘦身规范 | `.em/learning/state.md` 模板 | 10 min |
| M6 | 第一次实跑 | 选一个测试主题走 L1-L6 | 30 min |
| M7 | 验证 + 文档归档 | README + commit | 15 min |

**总估时**: ~2 小时。完成后即可对外宣传"EM-SKILL v3.1 学习模式"。

---

## M0 — 状态目录初始化

**前置**: 无
**开发内容**:
1. 创建 `D:\DeskTop\WorkSpace\Code\embedded-project-manager\.em\learning\` 目录
2. 创建子目录 `topics/` `knowledge/` `discussion/` `sessions/`
3. 写 `state.md`（≤50 行，参考现有 `.emv2/state.md` 风格）
4. 写 `topics/topics-index.md` 主题索引空模板

**验证方式**:
- `ls .em/learning/` 看到 4 个子目录 + 2 个 md 文件
- `state.md` ≤ 50 行

**优先级**: P0（阻塞后续所有步骤）

---

## M1 — 模板落地

**前置**: M0
**开发内容**:
1. 在 `EM-SKILL/templates/` 下新增 2 个文件：
   - `knowledge.md` — 字段：主题/目标读者/一手资料/关键概念/选型对比/易踩坑
   - `video-script.md` — 字段：标题/钩子/分镜（场景-画面-口播-字幕）/章节时间戳/CTA/口播风格
2. 两个模板都用 `<!-- 注释示例 -->` 占位，方便后续填充

**验证方式**:
- 用 `cp` 复制模板 → 在 `knowledge/_template-test/` 下能跑通字段填写

**优先级**: P1

---

## M2 — 命令文件落地

**前置**: M0
**开发内容**:
在 `EM-SKILL/commands/` 下新增 4 个命令文件，每个文件结构遵循现有 `commands/new.md` 风格：

1. `learn.md` — 触发: `/em learn <topic>` / 别名 `/em l`
   - 输入 topic → 创建 `.em/learning/knowledge/<topic>/` + 初始化 `knowledge.md`
   - 检查 `.em/learning/state.md` 当前主题，避免冲突
2. `kp.md` — 触发: `/em kp` / 别名 `/em pack`
   - 把当前主题的 `knowledge.md` 压缩为 `knowledge-pack.md`（≤100 行）
   - 强制 L1 收尾才允许执行
3. `retro.md` — 触发: `/em retro` / 别名 `/em r`
   - 扫当前主题的 `code/` `checkpoints/` `logs/` → 生成 `retro.md`
   - 字段：实测数据/踩坑清单/改进项/二次学习建议
4. `publish.md` — 触发: `/em publish` / 别名 `/em pub`
   - 读 `knowledge.md` + `knowledge-pack.md` + `retro.md` + `code/checkpoints/`
   - 生成 `video-script.md`（开场 15s 钩子 + 分镜 + 字幕 + CTA）
   - 同步生成 `blog-post.md` 草稿（可选用 `--blog` 开关）

**验证方式**:
- `/em help learn/kp/retro/publish` 能列出
- 每个命令在测试主题上跑通

**优先级**: P1

---

## M3 — SKILL.md 路由表更新

**前置**: M2
**开发内容**:
1. 打开 `EM-SKILL/SKILL.md`
2. 在"通用命令"表追加 4 行: `/em learn` `/em kp` `/em retro` `/em publish`
3. 在"子命令路由"表追加 4 行对应 `commands/*.md`
4. 在"项目类型"章节追加"LPR 学习模式"小节，引用本设计文档
5. 更新 `CHANGELOG.md` 到 v3.1.0

**验证方式**:
- 读 SKILL.md，4 个新命令在表中
- CHANGELOG 头部有 v3.1.0 段

**优先级**: P1

---

## M4 — 嵌入式插件联动

**前置**: M2
**开发内容**:
在 `EM-SKILL/plugins/embedded/` 下：
1. 修改 `PLUGIN.md` 加"LPR 实战录制"小节
2. 扩展 `serial-mcp` 工具：新增 `--record <session-id>` 参数
3. `/em verify` 在 L4 阶段自动调用录制（条件：当前在 `.em/learning/knowledge/<topic>/` 下）
4. 录屏文件落到主题目录的 `recordings/` 子目录

**验证方式**:
- 在学习主题目录下跑 `/em verify` → 自动生成 `recordings/<时间戳>.log`
- 不在学习主题目录下跑 → 不触发录制（避免误触发）

**优先级**: P2（嵌入式特定，非通用）

---

## M5 — state.md 瘦身规范

**前置**: M0
**开发内容**:
1. 写 `.em/learning/state.md` 模板（参考 `templates/state.md`）
2. 字段：当前主题 / 阶段 (L1-L6) / 最近 5 步 / 下一步动作
3. 写 `EM-SKILL/commands/rec.md` 的 LPR 适配：当检测到 `.em/learning/` 存在时，rec 命令额外加载 LPR state

**验证方式**:
- `wc -l .em/learning/state.md` ≤ 50
- 在嵌入式项目里 `/em rec` 同时加载 `.emv2/state.md` + `.em/learning/state.md`

**优先级**: P2

---

## M6 — 第一次实跑

**前置**: M1 + M2 + M3
**开发内容**:
选一个**低风险**的测试主题完整跑一遍 L1-L6：
- 建议主题: **"GD32F407 串口 DMA 接收"**（已在项目里、风险低、1 个视频时长合适）
- 跑通后产出：1 个 knowledge.md + 1 个 video-script.md + 1 个录屏
- 验证：视频脚本人工润色后能直接用

**验证方式**:
- `.em/learning/knowledge/gd32-usart-dma/` 下有完整 6 阶段产物
- video-script.md 通过"3 分钟讲清楚"可读性测试

**优先级**: P1（必须做，否则没法宣传）

---

## M7 — 验证 + 文档归档

**前置**: M6
**开发内容**:
1. 在 `EM-SKILL/README.md` 加"LPR 学习模式"特性小节（含 1 截图占位）
2. 更新 `EM-SKILL/CHANGELOG.md` v3.1.0 段
3. 跑 `git add .` + `git commit`（按 CLAUDE.md 规则提议）
4. 提议 git tag `v3.1.0-lpr`

**验证方式**:
- 提交后 `git log --oneline` 看到 v3.1.0 提交
- tag 已打

**优先级**: P1

---

## 依赖关系

```
M0 ─┬─→ M1 ──────────────────────────┐
    ├─→ M2 ─┬─→ M3 ──────────────────┤
    │       └─→ M4 (嵌入式可选)       │
    ├─→ M5 ──────────────────────────┤
    │                                ↓
    └────────────────────────────→ M6 ─→ M7
```

## 优先级总结

- **P0**: M0
- **P1**: M1, M2, M3, M6, M7
- **P2**: M4, M5
