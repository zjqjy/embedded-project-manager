# 头脑风暴 - 20260602-skill-standardize-universal-git

## 阶段状态
✅ 阶段 4/5 完成 - 4/4 子系统技术难点已识别并选定方案

---

## 子系统 1: Skill 标准化

| 难点 | 选择 | 备注 |
|------|------|------|
| 1.1 skill-install 模板 vs 现有结构 | **B. 顶部加 YAML frontmatter** | 最小改动，向后兼容 |
| 1.2 按需加载机制 | **A. 现有加载模式** | 单文件整加载，不拆分 |
| 1.3 双轨制目录 | **取消** | 现有结构即可 |

---

## 子系统 2: Skill 通用化

| 难点 | 选择 | 备注 |
|------|------|------|
| 2.1 目录重命名迁移 | **C. 双目录共存期** | 优先 `.em/`，回退 `.emv2/` |
| 2.2 嵌入式专属边界 | **上表划分** | 串口/烧录/编译/芯片学习 → `.em/embedded/` |
| 2.3 通用项目初始化 | **智能分析 + 不明确时询问** | init 扫描 Keil/CubeMX/ESP-IDF/PlatformIO 特征，命中自动启用；不明确才问 |

### 2.2 嵌入式专属能力清单

| 能力 | 归属 | 处置 |
|------|------|------|
| 步骤推进(verify) | 通用 | 保留核心 |
| 问题追踪(problem) | 通用 | 保留核心 |
| 决策记录(decision) | 通用 | 保留核心 |
| 讨论(disc) | 通用 | 保留核心 |
| 归档(arch) | 通用 | 保留核心 |
| 状态机(memory-log) | 通用 | 保留核心 |
| 串口(serial-mcp / serial-monitor) | **嵌入式专属** | → `.em/embedded/serial/` |
| 烧录(flash-openocd) | **嵌入式专属** | → `.em/embedded/flash/` |
| 编译(build-keil) | **嵌入式专属** | → `.em/embedded/build/` |
| 芯片学习(chip-learning) | **嵌入式专属** | → `.em/embedded/chip/` |
| embed-ai-tool 整合 | **嵌入式专属** | → `.em/embedded/integration/` |

---

## 子系统 3: Git 工作流集成

| 难点 | 选择 | 备注 |
|------|------|------|
| 3.1 AI 提议 commit UX | **A. 对话中输出** | AI 打印 message + 文件列表，用户回复"确认" |
| 3.2 feature 分支命名 | **A. 主步骤级** | `feature/s10`，子步骤同分支 |
| 3.3 CHANGELOG 工具 | **C. EM 自写 Python 脚本** | `tools/git-changelog/`，零外部依赖 |
| 3.4 tag 触发 | **A. 仅主步骤** | 步骤 5/5 归档完成时打 tag |
| 3.5 initem Git 权限 | **扩展 initem.md** | 白名单：status/diff/log/add/commit/checkout/tag；**禁止 push** |

### 3.5 Git 权限白名单（最终）

| 操作 | 授权 |
|------|------|
| `git status / diff / log`（只读） | ✅ |
| `git add`（暂存） | ✅ |
| `git commit -m "..."` | ✅ |
| `git checkout -b feature/...` | ✅ |
| `git tag v...` | ✅ |
| `git push` | ❌ **禁止**（用户手动推） |

---

## 子系统 4: 嵌入式能力保留

| 难点 | 选择 | 备注 |
|------|------|------|
| 4.1 加载机制 | **现有模式** | 单 SKILL.md 整加载，不拆分扩展 |
| 4.2 老项目升级 | **提供 `em migrate` 命令** | 非强制，老项目按需迁移 |
| 4.3 工具位置 | **保持 `EM-SKILL/tools/` 原位** | SKILL.md 加工具索引 |
| 4.4 文档结构 | **单 SKILL.md + 嵌入式章节** | 章节：快速开始 \| 通用命令 \| 嵌入式场景 \| 工具索引 |

### 4.2 升级流程

1. 用户 `git pull` 升级 EM-SKILL
2. 项目内 `.emv2/` 目录不变
3. EM 启动提示"检测到 `.emv2/`，建议迁移 `em migrate`"
4. `em migrate` 将 `.emv2/` 内容复制到 `.em/`，保留 `.emv2/` 软链接
5. 1-2 版本后提示可删除 `.emv2/`

### 4.4 SKILL.md 章节结构

```
EM-SKILL/SKILL.md
├── description (YAML frontmatter)
├── 快速开始
├── 通用命令 (/em rec / new / disc / verify / result / stat / sw / arch / sum / pi / gi / help)
├── 项目类型
│   ├── 通用项目（默认）
│   └── 嵌入式场景 ⭐
│       ├── 嵌入式专属命令 (/em initem 含 OpenOCD 下载指引)
│       ├── 工具索引 (serial-mcp / flash-openocd / build-keil / chip-learning)
│       ├── 嵌入式项目快速开始
│       └── S5/S7/S9 已完成能力说明
└── 详细命令文档
```

---

## 关键设计原则（最终汇总）

1. **标准化轻量化** — 仅加 YAML frontmatter，不重构目录
2. **现有加载模式** — 单 SKILL.md 整加载
3. **目录双轨制** — 优先 `.em/`，回退 `.emv2/`，1-2 版本后弃用
4. **嵌入式按域收纳** — `.em/embedded/` 子目录
5. **init 智能识别** — 自动检测嵌入式特征，不明确才问
6. **Git 自动化但用户把关** — AI 提议 + 用户确认 commit；禁止 push
7. **零外部依赖** — CHANGELOG 用 EM 自写 Python 脚本
8. **完全向后兼容** — 现有嵌入式项目零配置升级
