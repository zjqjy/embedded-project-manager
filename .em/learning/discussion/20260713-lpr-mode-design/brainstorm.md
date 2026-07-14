# LPR 学习模式 — Brainstorm

> 配套状态目录: `.em/learning/discussion/20260713-lpr-mode-design/`
> 范围: 只设计学习模式；OTA 升级示范留给后续。

## 1. 定位

LPR (Learn–Practice–Retro) 是与 HVR 平行的**第二条工作流**，专门服务"以项目为驱动的工程化学习"。
- HVR 服务"项目开发交付"
- LPR 服务"学习 + 沉淀 + 视频化分享"
- 两者互不破坏，可独立启动

## 2. 核心闭环（6 阶段）

```
L1 调研 Learn     /em learn <topic>      →  knowledge.md          (一手资料)
L2 沉淀 Pack      /em kp                 →  knowledge-pack.md     (内化压缩)
L3 编码 Practice  /em new (三档)         →  code/ + checkpoints/  (复用 new)
L4 实战 Verify    /em verify + result    →  实测日志/录屏         (复用 verify)
L5 复盘 Retro     /em retro              →  retro.md              (经验固化)
L6 视频 Publish   /em publish            →  video-script.md       (视频脚本)
              ↑                                            ↓
              └──────── 进入下一轮 / 下一主题 ────────────┘
```

## 3. 知识库结构

```
.em/learning/
├── state.md                # LPR 全局状态（≤50 行）
├── topics/                 # 主题索引
│   └── topics-index.md
├── knowledge/              # 沉淀库
│   └── <topic>/
│       ├── knowledge.md           # L1 调研产出
│       ├── knowledge-pack.md      # L2 沉淀产出
│       ├── code/                  # L3 编码产出
│       ├── checkpoints/           # L3 里程碑快照
│       ├── retro.md               # L5 复盘
│       ├── video-script.md        # L6 视频脚本
│       └── refs/                  # 引用材料（PDF/链接/截图）
├── discussion/             # 讨论目录
└── sessions/               # 每会话一文件
```

## 4. 命令扩展（4 个新命令）

| 命令 | 别名 | 作用 | 类比 |
|------|------|------|------|
| `/em learn <topic>` | `/em l` | 启动主题学习，L1 调研 | 类似 `/em new` 但服务于"学" |
| `/em kp` | `/em pack` | 把 L1 调研压缩为知识包 | 类似 `/em result` 收尾 |
| `/em retro` | `/em r` | 复盘当前主题 L3-L4 | 新增 |
| `/em publish` | `/em pub` | 生成视频脚本 + 博客稿 | 新增 |

## 5. 模板扩展（2 个新模板）

| 模板 | 字段要点 |
|------|---------|
| `knowledge.md` | 主题 / 目标读者 / 一手资料（链接/PDF）/ 关键概念 / 选型对比表 / 易踩坑 |
| `video-script.md` | 标题 / 钩子（开头 15s）/ 分镜（场景/画面/口播）/ 字幕 / 章节时间戳 / CTA |

## 6. 关键设计决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 状态目录 | **独立** `.em/learning/` | 与 `.emv2/` 解耦，避免污染项目状态 |
| 命名 | **LPR**（Learn–Practice–Retro）| 3 字易记，与 HVR 对仗 |
| 流程阶段 | **6 阶段** | L1-L2 学习侧 / L3-L4 实战侧 / L5-L6 输出侧 |
| 与 new 的关系 | **复用** `/em new` 作为 L3 | 保持代码实践环节的三档分流 |
| 视频脚本生成 | **半自动** | AI 起草 + 人工口播风格调整 |
| 知识库主题粒度 | **一个主题一目录** | 复用性好，跨主题可索引 |
| L1 资料来源 | 文档/手册/视频 + MiniMax 搜索 | 优先 MiniMax 搜索（CLAUDE.md 偏好）|
| L4 实战录制 | 嵌入式插件自动录串口+录屏 | 复用现有 serial-mcp 录制能力 |

## 7. 与现有 EM-SKILL 的耦合点

| 复用项 | 位置 |
|--------|------|
| `/em new` 三档 | L3 编码 |
| `/em verify` + `/em result` | L4 实战 |
| `state.md` 瘦身原则 | 扩展到 LPR 的 state.md |
| 嵌入式插件（serial-mcp）| L4 自动录屏 |
| 讨论目录规范 | 复用 `discussion/<YYYYMMDD>-<slug>/` |

## 8. 不做的事（Out of Scope）

- ❌ 不动 HVR、不动 `/em new` 三档
- ❌ 不做 OTA 升级示范（本轮只设计模式）
- ❌ 不做视频自动剪辑（只生成脚本）
- ❌ 不做 AI 自动口播生成（半自动）
- ❌ 不改通用核 .em/ 体系，独立 `.em/learning/`

## 9. 风险与缓解

| 风险 | 缓解 |
|------|------|
| L1 调研资料太多沉没 | 强制 `knowledge.md` ≤ 200 行，超出拆 `refs/` |
| L6 视频脚本同质化 | 模板留"口播风格"字段，每次手填 |
| 学习主题与项目混 | `.em/learning/` 完全独立目录 |
| 视频素材脱敏 | `retro.md` 不含客户/产线敏感信息 |

## 10. 与"自媒体博主"定位的对齐

- **可持续**: 每个学习主题 = 1 个视频选题（L6 直接产脚本）
- **工程化**: L1-L5 沉淀成知识库，可复用不重学
- **可视化**: L4 自动录屏 + L6 视频脚本 = 一条龙
- **可追溯**: `retro.md` + `checkpoints/` = 案例库
