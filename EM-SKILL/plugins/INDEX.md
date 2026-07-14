# EM-SKILL 插件索引

> 通用核（EM-SKILL）的所有扩展插件在此注册。  
> 物理解耦：每个插件可独立卸载，通用核不依赖。

## 已注册插件

| 插件 | 路径 | 启用条件 | 提供能力 |
|------|------|----------|----------|
| [embedded](embedded/PLUGIN.md) | `plugins/embedded/` | `project.json.type == "embedded"` 或检测 Keil/CubeMX/ESP-IDF/PlatformIO | `/em initem` + 串口/烧录/编译工具链 + 嵌入式 verify |
| [learning](learning/PLUGIN.md) | `plugins/learning/` | `project.json.type == "learning"` 或检测 `.em/learning/` | `/em learn new/verify/status` + LPR 5 阶段 + 多格式构建 |

> 协同说明：`/em learn` 命令前缀需要由通用核识别；具体 CLAUDE.md 触发器注册逻辑由 S13 统一处理。

## 插件开发规范

1. **路径**：`plugins/<plugin-name>/`
2. **入口文档**：`<plugin>/PLUGIN.md`（含 YAML frontmatter）
3. **命令**：`commands/<cmd-name>.md`
4. **工作流**：`workflows/<flow-name>.md`
5. **工具**：`tools/<tool-name>.py`（可选）
6. **模板**：`templates/<template-name>.md`（可选）

## 添加新插件

1. 创建 `plugins/<new-plugin>/` 目录
2. 写 `PLUGIN.md`（含 frontmatter 的 `enabled_when` 条件）
3. 在本 INDEX.md 表格追加一行
4. 通用核 README 加章节
