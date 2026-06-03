# 命令: /em result (提交结果)

## 功能
提交验证结果，触发后续流程。

## 触发
```
/em result <步骤>-<结果>     # 如 /em result s1-通过 / s1-a-失败
```

## 执行流程

### 通过时
```
1. 解析结果 → 提取步骤编号（如 s1-a）
2. 🟢 更新 HVR 文件 → 验证结果区段填写「通过」+ 用户口述要点
3. 🟢 更新 state.md
   - 当前步骤 → ✅ 完成
   - 下一步动作 → 自动推进
4. 🟢 自动推进
   - 读 project-spec.md 步骤表找下一子步骤
   - state.md 当前步骤 = 下一子步骤(开发中)
   - 无下一子 → 主步骤完成 → 提示 /em result s<N>-通过 收尾
5. 同步 project-spec.md 步骤表
6. 追加本次会话日志：<STATE_DIR>/sessions/sess-<id>.md
   - 主要内容 / 产出 / 下一步
7. 如有闭环问题 → 更新 problem-log.md 闭环
8. 如触发归档阈值（见 commands/arch.md） → 提示 /em arch
9. 更新全局索引
```

### 失败时
```
1. 解析失败信息 → 提取步骤编号
2. 🔴 更新 state.md
   - 当前步骤 → 🔁 返工中
   - 阻塞项 → 追加一行（指向新 problem 条目）
3. 📖 自动读取最新日志：扫描 <STATE_DIR>/logs/ 取最新（嵌入式：串口/编译；通用：测试输出/构建日志）
4. 更新 HVR 文件
   - 验证结果区段 → 失败 + 日志摘要 + 物理/可观察现象
5. 创建 problem-log.md 条目（错误分析 + 引用 HVR 文件）
6. 追加会话日志：sess-<id>.md
   - 主要内容 / 失败现象 / 下一步排查方向
7. 进入问题讨论模式（可选 /em disc）
8. 分析问题根因（结合日志内容）
9. 记录讨论结论和解决方案到 decisions.md
```

## 路径占位符（v3.0 通用化）

| 占位符 | 实际 |
|--------|------|
| `<STATE_DIR>` | `.em/` 优先，回退 `.emv2/`，由 `get_state_dir()` 解析 |
| `<STATE_DIR>/logs/` | 日志目录（嵌入式串口/编译；通用测试输出） |
| `<STATE_DIR>/sessions/sess-<id>.md` | 单会话日志（v3.0 替代旧 memory-log.md 的会话历史段） |
| `<STATE_DIR>/state.md` | 最小状态文件（v3.0 替代旧 memory-log.md 的当前状态段） |
| `<STATE_DIR>/decisions.md` | 决策日志（v3.0 替代旧 memory-log.md 的关键决策段） |

## 旧版兼容（无 state.md / sessions/ 时）

- 无 `state.md` → 直接读写 `memory-log.md` 的「当前状态」与「会话历史」段
- 无 `sessions/` → 追加到 `memory-log.md` 的「会话历史」段
- 行为兼容，不破坏旧项目；建议老项目运行 `/em migrate-state` 升级

## 关键提醒

⚠️ **失败时必须先更新 HVR 文件，再进入讨论模式**
⚠️ **不再写入 memory-log.md**（v3.0 拆为 state.md + sessions/ + decisions.md）

## 相关文件
- `workflows/hvr-workflow.md` — HVR 模板与流程图
- `commands/verify.md` — 通用 verify 入口（生成 HVR）
- `templates/state.md` / `templates/session.md` — 模板
- `commands/migrate-state.md` — 旧版 memory-log → state.md 一键迁移
