# embed-ai-tool 整合 - 开发任务

## 讨论ID
`20260420-embed-ai-tool-integration`

## 最终方案
**协作分工**
- EM = 流程控制（verify 命令）
- embed-ai-tool = 具体执行（编译/烧录/调试）

**注意**：串口监控使用 EM 自带的 S5 工具，不整合 embed-ai-tool serial-monitor

## 整合顺序

| 步骤 | 工具 | 状态 |
|------|------|------|
| 1 | build-keil | 待整合 |
| 2 | flash-openocd | 待整合 |

## 调用方式
- B + C：Skill工具调用 + AI自动判断

## 信息传递
看工具 SKILL.md 的"必要输入"，verify 时按需传递

## 结果回收
脚本 stdout 结构化输出 + 失败分类

## 使用场景
verify 阶段

---

## 开发任务

### 任务1: 整合 build-keil（编译）

**文件**: `C:\Users\23393\.claude\skills\EM-SKILL\commands\verify.md`

**修改内容**:
1. 添加 build-keil 技能调用说明
2. 添加编译验证流程说明

**整合点**:
- verify 编译 → 调用 build-keil

---

### 任务2: 整合 flash-openocd（烧录）

**文件**: `C:\Users\23393\.claude\skills\EM-SKILL\commands\verify.md`

**修改内容**:
1. 添加 flash-openocd 技能调用说明
2. 添加烧录验证流程说明

**整合点**:
- verify 烧录 → 调用 flash-openocd

---

### 任务3: 更新 hvr-workflow.md

**文件**: `C:\Users\23393\.claude\skills\EM-SKILL\workflows\hvr-workflow.md`

**修改内容**:
1. 在 HVR 模板中添加 embed-ai-tool 技能声明
2. 说明 AI 在验证时应调用合适的技能

---

### 任务4: 验证整合效果

**验证步骤**:
1. `/em verify 编译` - 测试编译流程
2. `/em verify 烧录` - 测试烧录流程
3. 检查 HVR 文件是否正确记录

## 状态
- [ ] 任务1: 整合 build-keil
- [ ] 任务2: 整合 flash-openocd
- [ ] 任务3: 更新 hvr-workflow.md
- [ ] 任务4: 验证整合效果

## 讨论日期
2026-04-20
