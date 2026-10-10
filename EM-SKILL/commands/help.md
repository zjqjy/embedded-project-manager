# 命令: /em help (帮助)

## 功能
显示帮助信息

## 触发
```
/em help [命令]
```

## 无参数时
显示命令列表（v3.0 重构后）：

```
项目管理:
  init <name>      项目初始化（自动识别 general/embedded；最小生成 2 文件）
  si <path>        存量接入
  rec [name]       恢复项目（只读 state.md，瘦身；>50 行硬拒绝）
  stat [-v/steps/next]  状态查看（默认极简）
  sessions [id]    会话历史浏览
  migrate          迁移 .emv2/ → .em/
  migrate-state    一键生成 state.md（瘦身）
  logs-clean [-n N] 日志滚动清理（保留最新 N 份，默认 10）

开发流程（new 三档分流，superpower 风格，S18 追问先行/落盘最后）:
  new <描述> [--light/--std/--deep]   AI 推荐档位
    三档必经 R0 追问轮: 一次一问澄清 → 理解摘要确认后才出方案（至少问：轻1/中2/重每子系统1；不设上限，意图清晰为准）
    轻档 → R0 + 对话内 quick-plan（不落盘）(5 min)
    中档 → R0 + R1/R2 对话 → R3 统一落盘 plan.md (15 min) — 默认
    重档 → R0 + 5 阶段 disc (45 min)
    硬闸门: 理解未确认禁止写任何文档
  disc [id]        独立触发讨论（重档）
  verify s<N>      验证（按 type 选 HVR 模板；嵌入式注入三连）
  result <步>-<结果>  提交结果（自动推进 + 写会话日志）
  pro <描述>       上报 EM-SKILL 问题到管家项目 problem-log

工具/索引:
  arch             归档（主步骤完成自动 tag + CHANGELOG；problem-log closed 归档）
  sum              上下文摘要
  pi               项目索引
  gi               全局索引
  sw <项目>        跨项目切换
  help [命令]      查看帮助

插件命令（lazy-load，敲命令时按需加载，S15）:
  initem / build / flash / serial   嵌入式（tools/adapters/ + registry.json，S17-B）
  learn new/verify/status/humanize  学习模式（LPR 闭环）
```

## Git 集成（S10-D）

```
git 工作流:
  tools/git-changelog/   CHANGELOG 自动生成（Python，零依赖）
  arch (主步骤完成)      自动打 tag + 更新 CHANGELOG
  verify (HVR 完成)      提议 commit（用户确认后执行）
  problem-log close      提议 commit（用户确认后执行）

手动生成 CHANGELOG:
  python EM-SKILL/tools/git-changelog/changelog_gen.py
    --from <tag> --to <ref> --version <ver> --dry-run

Git 权限（initem.md 配置）:
  ✅ status / diff / log / add / commit / checkout -b / tag
  ❌ push（禁止，user 手动推）
```

## 有参数时
显示指定命令的详细帮助：

```
/em help rec        # rec 瘦身策略
/em help new        # new 三档分流（含启发式表）
/em help verify     # verify + 嵌入式注入
/em help sessions   # 会话浏览
/em help migrate    # .emv2/ → .em/ 深度迁移
/em help migrate-state # 一键生成 state.md
```

## 工作流细则

| 工作流 | 文件 |
|--------|------|
| R0 需求澄清（三档共用）| `workflows/new-clarify.md` |
| HVR 工作流 | `workflows/hvr-workflow.md` |
| 讨论流程（重档）| `workflows/discussion-flow.md` |
| new 轻档 | `workflows/new-light.md` |
| new 中档 | `workflows/new-standard.md` |

## 嵌入式插件

| 资源 | 文件 |
|------|------|
| 插件清单 | `plugins/embedded/PLUGIN.md` |
| 嵌入式 verify 子流程 | `plugins/embedded/workflows/verify-embedded.md` |
| 芯片学习 | `plugins/embedded/workflows/chip-learning.md` |
| 嵌入式 HVR 模板 | `plugins/embedded/templates/hvr-template-embedded.md` |
