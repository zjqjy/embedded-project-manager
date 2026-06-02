# 命令: /em help (帮助)

## 功能
显示帮助信息

## 触发
```
/em help [命令]
```

## 无参数时
显示命令列表

```
项目管理:
  si <path>    存量接入
  init <name>  项目初始化
  stat         当前步骤状态
  rec [name]   恢复项目
  migrate      迁移 .emv2/ → .em/（S10-C）

开发流程:
  new <描述>   新功能开发（自动分配S编号）
  disc [id]    讨论流程（5阶段）
  verify s<N>  验证（自动状态变更）
  result <步>-<结果>  提交结果（自动推进）

工具:
  arch         归档（主步骤完成自动 tag + CHANGELOG）
  help [命令]  查看帮助
  sum          上下文摘要
  pi           项目索引
  gi           全局索引
  sw <项目>    跨项目切换
  initem       工具初始化（含 Git 权限配置）
```

## Git 工具（S10-D）

EM-SKILL 集成 Git 工作流，提供以下工具与触发点：

```
git 工作流:
  tools/git-changelog/  CHANGELOG 自动生成工具（Python，零依赖）
  arch (主步骤完成)     自动打 tag + 更新 CHANGELOG
  verify (HVR 完成)     提议 commit（用户确认后执行）
  problem-log close     提议 commit（用户确认后执行）

手动生成 CHANGELOG（推荐）:
  python EM-SKILL/tools/git-changelog/changelog_gen.py
    # 在项目根目录执行，输出 ./CHANGELOG.md
    # 常用参数: --from <tag> --to <ref> --version <ver> --dry-run

Git 权限（已在 initem.md 配置）:
  ✅ status / diff / log / add / commit / checkout -b / tag
  ❌ push（禁止，user 手动推）
```

## 有参数时
显示指定命令的详细帮助

```
/em help verify    # 显示 verify 命令
/em help new       # 显示 new 命令（含编号规则）
/em help result    # 显示 result 命令（含状态推进逻辑）
/em help disc      # 显示 disc 命令（讨论流程）
/em help arch      # 显示 arch 命令（含 S10-D 自动 tag 流程）
```

## 工作流细则

| 工作流 | 文件 |
|--------|------|
| HVR工作流 | workflows/hvr-workflow.md |
| 讨论流程 | workflows/discussion-flow.md |
| 芯片学习 | workflows/chip-learning.md |
