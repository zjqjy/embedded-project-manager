# SKILL.md Tab补齐优化

**讨论ID**: 20260416-skill-tab-completion
**日期**: 2026-04-16
**状态**: ✅ 讨论完成，待开发

---

## 需求描述

- 技能名称 `/em` 可用
- 子命令 `si`, `verify`, `result` 等不支持 tab 补齐
- 希望子命令参数也能 tab 补齐

---

## 需求拆分

### 1. SKILL.md 主入口
- 类型：配置定义
- 简述：命令声明和参数定义，参与 tab 补齐

### 2. commands/ 子命令文档
- 类型：详细文档
- 简述：供 AI 查阅的详细命令说明

### 3. Skill 加载机制
- 类型：系统机制
- 简述：Claude Code 如何解析 SKILL.md 并提供补齐

---

## 命令参数选项化

| 命令 | 参数 | 选项 | 可选项化 |
|------|------|------|----------|
| `/em si` | `path` | 路径 | ❌ |
| `/em init` | `name` | 项目名 | ❌ |
| `/em new` | `feature` | 功能名 | ❌ |
| `/em disc` | - | 无 | - |
| `/em verify` | `step` | s1, s2, s3, s4, s5, s6 | ✅ |
| `/em result` | `info` | s1-通过, s1-失败-xxx, s2-通过, s2-失败-xxx, ... | ✅ |
| `/em stat` | - | 无 | - |
| `/em rec` | `path` | 路径（可选） | ❌ |
| `/em sw` | `name` | 项目名/路径 | ❌ |
| `/em arch` | - | 无 | - |
| `/em sum` | - | 无 | - |
| `/em pi` | - | 无 | - |
| `/em gi` | - | 无 | - |
| `/em help` | `command` | si, init, new, disc, verify, result, stat, rec, sw, arch, sum, pi, gi, help | ✅ |

---

## 头脑风暴结论

### 难点1: 新格式是否被 Claude Code 支持
- 方案A: 直接修改 SKILL.md 并测试
- 方案B: 先查 Claude Code 文档确认
- **决策: 方案A - 直接测试，边用边调**

### 难点2: 与现有 commands/ 的关系
- 方案A: SKILL.md 只做命令声明，commands/ 保留详细文档
- 方案B: 合并到 SKILL.md，删除 commands/
- **决策: 方案A - SKILL.md 做命令+参数声明，commands/ 保留详细说明供 AI 查阅**

### 难点3: Tab 补齐的生效条件
- 方案A: `/em verify` → 提示 s1-s6
- 方案B: `/em verify ` → 提示 s1-s6
- **决策: 方案B - 空格后触发**

---

## 子流程拆分

### S7-A: SKILL.md 命令格式重构
- **所属子系统**: SKILL.md 主入口
- **开发内容**:
  1. 修改 `name`, `description` 头部
  2. 按新格式重写所有命令定义（14个命令）
  3. 其中3个命令添加 Parameters 选项（verify, result, help）
- **前置条件**: 无
- **验证方式**: 测试 `/em verify [TAB]` 是否提示 s1-s6
- **优先级**: 1

### S7-B: commands/ 目录处理
- **所属子系统**: 详细文档
- **开发内容**:
  1. 保留 commands/ 目录（供 AI 查阅详细说明）
  2. 不删除现有文件
- **前置条件**: S7-A 完成
- **验证方式**: 检查 `/em help verify` 是否正常输出
- **优先级**: 2

---

## 参考格式

```markdown
### /build [target]

Build the project with specified target.

**Parameters:**
- `target`: Build target
  - `debug` - Debug build with symbols
  - `release` - Optimized release build
  - `test` - Test build

**Example:**
/build debug
```
