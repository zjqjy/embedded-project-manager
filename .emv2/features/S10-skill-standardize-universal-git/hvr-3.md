## 人工验证请求 [HVR-S10-E-GENERAL]

**验证类型**: 全流程端到端验证（通用场景）
**所属步骤**: S10-E 全流程验证
**场景**: 通用项目（新建，非嵌入式）
**前置条件**: S10-A / S10-B / S10-C / S10-D 已完成
**创建时间**: 2026-06-02
**验证范围**: init 不命中嵌入式特征、`.em/` 创建、Git 工作流

---

### 验证目标

在**通用项目**（不带 Keil/CubeMX/ESP-IDF/PlatformIO 特征）上验证 S10 全套子步骤：
1. `init` 智能识别为通用项目
2. 不加载嵌入式工具（无 `.em/embedded/`）
3. `.em/` 主目录正常工作
4. Git 集成在通用项目上正常工作
5. CHANGELOG 自动生成

---

### 技能声明
| 技能 | 工具 | 状态 |
|------|------|------|
| changelog_gen | `EM-SKILL/tools/git-changelog/changelog_gen.py` | ✅ 通过 (L1) |
| init 智能识别 | `EM-SKILL/commands/init.md` | ⏳ L2 待用户在通用项目验证 |
| rec (无嵌入式目录时) | `EM-SKILL/commands/rec.md` | ⏳ L2 待用户验证 |
| Git 集成 (通用项目) | `EM-SKILL/commands/{verify,arch,initem}.md` | ⏳ L2 待用户验证 |
| 不加载嵌入式工具 | init.md 第 3 节"嵌入式 vs 通用项目" | ⏳ L2 待用户验证 |

### L1 自动化结果（子代理执行）

#### 1. SKILL.md 项目类型章节校验 ✅

SKILL.md 中"项目类型"章节（行 137-202）已明确定义：
- **通用项目**: HVR 工作流 + 状态管理 + 讨论机制 + 验证闭环
- **嵌入式场景 ⭐**: 嵌入式专属命令 + 工具索引 + 嵌入式项目快速开始

通用项目 init 时**不加载**嵌入式工具（SKILL.md 行 148 明确说明）。

#### 2. commands/init.md 智能识别逻辑校验 ✅

init.md 第 26-80 行"智能识别流程"包含：
- **特征扫描规则**: 7 类嵌入式特征文件（Keil/CubeMX/ESP-IDF/PlatformIO/Arduino/IAR/GCC Makefile）
- **判定逻辑**:
  - 扫描结果 = ∅ → 询问用户（"通用项目 vs 嵌入式项目"）
  - 命中至少一项 → 自动判定为嵌入式
- **嵌入式 vs 通用项目对照表**:
  - 嵌入式: `.em/` + `.em/embedded/` + 串口/烧录/编译/芯片学习
  - 通用: `.em/`（不加载嵌入式工具）

#### 3. commands/rec.md 不区分项目类型 ✅

rec.md 通过 `get_state_dir()` 检测状态目录，**不依赖**项目类型：
- `.em/` 优先 → 使用
- 回退 `.emv2/` → 使用
- 都不存在 → 提示运行 `/em init`

通用项目和嵌入式项目共用同一套恢复逻辑。

#### 4. commands/initem.md Git 权限独立性 ✅

initem.md "Git 权限配置"章节对所有项目类型一致：
- 白名单: `git status/diff/log/add/commit/checkout -b/tag`
- 禁止: `git push/*`
- 触发点: HVR 验证、问题解决、归档完成

通用项目无需工具初始化步骤（`/em initem` 中的"探测工具"是嵌入式场景专用），
但**Git 权限配置章节**对通用项目同样适用。

#### 5. commands/verify.md 提议 commit 通用性 ✅

verify.md 的"提议 commit 流程"**不依赖**项目类型：
- AI 提议 commit message + 文件列表
- 用户确认/取消/修改
- 跳过条件（无变更、纯日志、用户暂不提交）

通用项目和嵌入式项目共用同一套提议 commit 流程。

#### 6. changelog_gen.py 通用性 ✅

changelog_gen.py **与项目类型无关**：
- 只读 `git log` 输出
- 按 EM 自定义 commit 格式（`[Sx] type: message`）解析
- 按 Keep a Changelog 规范输出

任何 git 仓库（无论 Web/App/CLI/嵌入式）均可使用。

#### 7. 目录双轨制对通用项目的支持 ✅

- 新通用项目: `/em init <name>` → 创建 `.em/`
- 旧 `.emv2/` 项目: `/em migrate` 升级到 `.em/`
- 通用项目 init 不创建 `.em/embedded/`（无嵌入式工具）

---

### L2 待用户验证项（新建通用项目端到端）

下列项目需要在新建通用项目上由用户手动验证：

#### A. 通用项目初始化
- [ ] 在一个无嵌入式特征文件的目录（如纯 Python/JS 库）中执行 `/em init <name>`
- [ ] 验证弹出"项目类型识别"菜单（"未检测到嵌入式特征文件"）
- [ ] 选择"1. 通用项目"
- [ ] 验证仅创建 `.em/` 目录，**不创建** `.em/embedded/`
- [ ] 验证 `.em/project-spec.md` 与 `.em/memory-log.md` 创建
- [ ] 验证全局索引 `~/.claude/embedded-projects-index.md` 更新

#### B. 不加载嵌入式工具
- [ ] 验证通用项目下 `/em initem` 行为合理（应跳过工具探测，仅配置 Git 权限）
- [ ] 验证通用项目不引用 `EM-SKILL/tools/build-keil/` 等
- [ ] 验证通用项目执行 `/em rec` 不报错

#### C. Git 工作流（通用项目）
- [ ] 在通用项目内做一次代码修改
- [ ] 执行 `/em verify s1`（或某 step）触发 HVR 文件生成
- [ ] 验证 AI 提议 commit message（`[S<n>] type: message`）
- [ ] 用户确认后执行 `git add` + `git commit`
- [ ] 验证 `git push` 仍被禁止
- [ ] 主步骤完成时 `/em arch` 打 tag + 生成 CHANGELOG
- [ ] 验证 CHANGELOG.md 内容符合 Keep a Changelog 规范

#### D. 跨项目对比
- [ ] 在同一会话内同时加载 OTA 项目（嵌入式）和通用项目
- [ ] 验证 `/em rec <name>` 切换正常
- [ ] 验证 init 智能识别对不同项目根目录表现不同（嵌入式 vs 通用）

---

### 【AI 工具执行记录】
| 时间 | 工具/命令 | 状态 |
|------|----------|------|
| 2026-06-02 | 读取 SKILL.md"项目类型"章节 | ✅ 通用+嵌入式双轨明确 |
| 2026-06-02 | 校验 init.md 智能识别流程 | ✅ 7 类特征 + 询问菜单 |
| 2026-06-02 | 校验 rec.md 通用性 | ✅ 不区分项目类型 |
| 2026-06-02 | 校验 initem.md Git 权限独立性 | ✅ 与项目类型解耦 |
| 2026-06-02 | 校验 verify.md 提议 commit 通用性 | ✅ 不依赖项目类型 |
| 2026-06-02 | 校验 changelog_gen.py 通用性 | ✅ 与项目类型无关 |

### 【已知问题】
1. **L2 验证需新建项目**：本环境无新建通用项目，需用户手动创建一个测试目录并执行 `/em init`。
2. **initem.md 工具探测**: initem.md 当前包含嵌入式工具探测（detect_tools.py）。对通用项目，理论上应跳过，但需验证 initem 在通用项目上下文中的实际行为。
3. **全局索引**: 通用项目是否写入 `~/.claude/embedded-projects-index.md` 需用户验证（按 init.md 描述，所有 init 项目都更新索引）。

### 【共同决策】
```
决策: ☐ 通过  ☐ 失败  ☑ 部分通过（L1 全通过 / L2 待用户）
原因:
  L1: 文档结构和逻辑校验全部通过（6/6 项）
  L2: 需用户手动创建通用测试项目并执行 init/rec/verify/arch
下一步:
  - 用户创建通用项目测试目录
  - 执行 A/B/C/D 验证
  - 全部通过后填 /em result S10-E-GENERAL-通过
```

---

**提交命令**: /em result S10-E-GENERAL-通过 或 /em result S10-E-GENERAL-失败-[描述]
