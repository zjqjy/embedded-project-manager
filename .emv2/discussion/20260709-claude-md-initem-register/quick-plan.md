# quick-plan: S13-claude-md-initem-register

## 一句话目标
在 `/em initem` 末尾追加一步，把「编译/烧录/串口」三组关键词 →
命令文档路径写入 `~/.claude/CLAUDE.md`，按需动态加载（不灌全文）。

## 改动清单（≤ 5 项）
- [ ] `EM-SKILL/plugins/embedded/commands/initem.md` — 新增「步骤 5: 注册全局 CLAUDE.md」
- [ ] 新建 `EM-SKILL/plugins/embedded/templates/claude-md-snippet.md` — 指针 section 模板
- [ ] 用户机器 `~/.claude/CLAUDE.md` — 不存在则创建；存在则幂等追加 `## EM-SKILL 嵌入式工具（动态加载）` section
- [ ] `EM-SKILL/.emv2/project-spec.md` — 步骤表追加 S13 行
- [ ] `EM-SKILL/.emv2/state.md` — 当前步骤 = S13（开发中），下一步 = `/em verify s13`

## 验证方式
1. 跑 `/em initem` → `~/.claude/CLAUDE.md` 含三行关键词表
2. 再跑一次 → 内容幂等（不重复追加）
3. 对话说「帮我编译」 → Claude 自动 Read `commands/build.md`
4. 对话说「烧录固件」 → Claude 自动 Read `commands/flash.md`
5. 删除全局 CLAUDE.md 后再跑 → 干净重建
6. `cat ~/.claude/CLAUDE.md` → 含动态加载说明 + 3 行指针表（≤ 10 行）

## 不做的事（边界）
- 不改 `/em init`（用户明确：仅 initem 写）
- 不写项目级 CLAUDE.md（用户明确：全局）
- 不在 CLAUDE.md 灌完整用法（指针 + 按需加载）
- 不改 initem 现有 1-4 步
- 不改其他嵌入式命令文件
- 不引入新依赖（纯 Markdown）