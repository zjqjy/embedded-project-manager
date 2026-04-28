<!-- 归档内容见 .emv2/history/2026/04/19/memory-log.md -->

# 项目记忆日志 - embedded-project-manager-v2

## 会话指纹
- **项目ID**: proj-emv2-260225
- **当前会话**: sess-20260428-001
- **会话链**: sess-20260225-001 → sess-20260227-001 → sess-20260327-001 → sess-20260415-001 → sess-20260416-001 → sess-20260417-001 → sess-20260419-001 → sess-20260419-002 → sess-20260428-001

## 快速恢复信息
```
恢复命令: /em rec emv2
最后活跃: 2026-04-28
状态: S7-讨论完成，GUI方案已确定
```

## 当前状态
- **步骤**: S7-EM-SKILL GUI（🚧 讨论完成）
- **状态**: S1-S6全部完成，S7-讨论完成
- **最后活跃**: 2026-04-28
- **最后会话ID**: sess-20260428-001

---

## 开发步骤状态

| 步骤 | 名称 | 状态 | 日期 |
|------|------|------|------|
| S1 | 存量接入 | ✅ 完成 | 2026-02-25 |
| S2 | 需求对齐讨论流程 | ✅ 规划完成 | 2026-03-27 |
| S3 | HVR工作流增强 | ✅ 完成 | 2026-04-16 |
| S4 | 芯片学习机制 | ✅ 完成 | 2026-04-16 |
| S5 | 串口调试工具 | 🚧 讨论完成 | 2026-04-19 |
| S6 | 文件归档机制 | ✅ 完成 | 2026-04-17 |
| S7 | EM-SKILL GUI | 🚧 讨论完成 | 2026-04-28 |

---

## 待办事项

### 已完成
- [完成] S5-A MCP工具开发 - 2026-04-22
  - tkinter UI + pyserial + MCP Server

### 已完成
- [完成] S4芯片学习机制 - 2026-04-16
- [完成] S6归档机制 - 2026-04-17
  - 阈值：memory-log > 600行，problem/decision > 300行
- [完成] S5讨论 - 2026-04-19
  - 确定：MCP工具 + tkinter UI + 人-AI协作验证流程

---

## 关键决策

- [2026-02-25] 项目初始化，创建基本功能结构
- [2026-03-27] 实用性修复方案讨论
- [2026-04-15] SKILL.md 重构，命令前缀 `/em`
- [2026-04-16] S4/S8验证完成
- [2026-04-16] S6归档讨论：memory-log和project-spec为主要归档目标
- [2026-04-19] S5讨论完成：
  - 定位：MCP工具 + GUI + 人-AI协作验证流程
  - 方案：C-b（MCP自带UI）
  - 技术：tkinter + pyserial + MCP Server
  - 功能：串口配置/收发/日志保存/MCP接口
- [2026-04-28] S7讨论完成：
  - 技术栈：Tauri + Vue3 + Vite + Element Plus
  - Claude通信：CLI管道（常驻子进程，stdin/stdout实时双向）
  - 定位：GUI是EM-SKILL的前端外壳，不替代原技能
  - 触发方式：桌面快捷方式为主
  - 串口工具：Vue重写（保留原tkinter工具）
  - 第一期：仅Windows，代码按跨平台写

---

## 会话历史

### sess-20260428-001 (2026-04-28) ← 当前
- **主要内容**:
  - S7 EM-SKILL GUI 讨论（/em new EM-SKILL GUI界面）
  - 技术栈确定：Tauri + Vue3 + Vite + Element Plus
  - Claude通信方案：CLI管道（常驻子进程，实时双向）
  - GUI定位：EM-SKILL前端外壳，不替代原技能
  - 触发方式：桌面快捷方式为主
  - 串口工具：Vue重写（保留原tkinter工具）
  - 第一期：仅Windows，代码按跨平台写
- **产出**: S7讨论完成，9个子步骤（S7-A~S7-I）已规划
- **下一步**: S7-A 技术验证（Claude CLI管道通信）

### sess-20260419-002 (2026-04-19)
- **主要内容**:
  - S5工作流讨论（/em disc S5）
  - 修正工作流：/em result应在验证阶段
  - 明确失败流程：AI读MCP + 人类观察 → 共同分析 → 共同修改
- **产出**: 更新hvr-workflow.md反映正确工作流

### sess-20260419-001 (2026-04-19)
- **主要内容**:
  - S5串口调试工具讨论
  - 确定S5核心定位：MCP工具 + GUI + 人-AI协作验证流程
  - 选定方案C-b（MCP自带tkinter UI）
  - 确定技术栈：tkinter + pyserial + MCP Server
  - 确定功能：串口配置/收发/日志保存/MCP接口
  - S5开发完成（14:40）
  - MCP测试通过
- **产出**: S5讨论完成，S5验证通过

### sess-20260417-001 (2026-04-17)
- **主要内容**:
  - S6归档机制验证（/em verify s6）
  - 更新归档阈值（memory-log > 600行，其他 > 300行）
  - 更新 arch.md 和 history-index.md
- **产出**: S6验证通过
- **下一步**: /em verify s5

### sess-20260416-001 (2026-04-16)
- **主要内容**:
  - S4芯片学习验证（/em si AI_test，GD32F7xx识别成功）
  - S6归档机制讨论（memory-log和project-spec为归档重点）
- **产出**: S4验证通过，S6讨论完成

---

## 最近更新

### 2026-04-28
- S7 EM-SKILL GUI 讨论完成（/em new）
  - 技术栈：Tauri + Vue3 + Vite + Element Plus
  - Claude通信：CLI管道（常驻子进程，stdin/stdout实时双向）
  - 定位：GUI是EM-SKILL的前端外壳，不替代原技能
  - 触发方式：桌面快捷方式为主
  - 串口工具：Vue重写（保留原tkinter工具）
  - 第一期：仅Windows，代码按跨平台写
  - 开发步骤：S7-A~S7-I（9个子步骤）
  - 讨论目录：`.emv2/discussion/20260428-em-skill-gui/`
  - 下一步：S7-A 技术验证（Claude CLI管道通信）

### 2026-04-28
- `/em disc` 讨论：new 命令步骤编号机制
  - 问题：new 流程没有标号，无法指示当前步骤位置
  - 方案：`/em new` 自动分配 S(N+1)，编号格式 S<数字>
  - 存量从 S7 开始递增
  - 讨论目录：`.emv2/discussion/20260428-new-step-id/`
  - 待执行任务：修改 new.md、project-spec.md（补号）、stat.md、verify.md

### 2026-04-20
- embed-ai-tool 整合讨论
  - 探索 embed-ai-tool：17个技能，6大类（构建/烧录/调试/协议/驱动/流水线）
  - 确定最终方案：协作分工（EM流程控制 + embed-ai-tool具体执行）
  - 整合点：verify 阶段调用 embed-ai-tool 技能
  - 待执行任务：更新 verify.md 和 hvr-workflow.md
- 讨论目录：`.emv2/discussion/20260420-embed-ai-tool-integration/`

### 2026-04-19
- S5讨论完成
  - 确定：MCP工具 + tkinter UI + 人-AI协作验证流程
  - 方案：C-b（MCP自带UI）
  - 技术：tkinter + pyserial
  - 功能：串口配置/收发/日志保存/MCP接口
  - 更新：hvr-workflow.md、discussion目录
- S5开发完成（14:40）
  - MCP集成到serial_monitor.py
  - 通过文件共享与Claude通信
  - MCP测试：serial_status/serial_read/serial_log_file 全部通过
  - HVR-S5-001验证通过

### 2026-04-17
- S6归档机制验证通过
  - 更新归档阈值：memory-log > 600行，problem/decision > 300行
  - arch.md 已更新支持新类型
  - history-index.md 已更新支持新类型

### 2026-04-16
- S4芯片学习验证通过
  - GD32F7xx正确识别
  - chips.json已更新
- S6归档讨论完成
  - 确定memory-log和project-spec为归档重点

---
