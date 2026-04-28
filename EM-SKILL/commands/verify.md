# 命令: /em verify (准备验证)

## 功能
生成人工验证请求 (HVR)，并启动S5串口工具

## 触发
```
/em verify s<编号>    # 如 /em verify s7
```

**步骤参数使用 new 命令分配的 S 编号**（如 S7），详见 new.md。

## 执行流程

1. 读取项目当前步骤
2. 生成 HVR 文件（增强版）
3. 保存到 `.emv2/checkpoints/HVR-<步骤>-<序号>.md`
4. 启动S5串口工具
5. 输出验证清单

## HVR 文件格式（增强版）

```markdown
## 人工验证请求 [HVR-S<N>-<序号>]

**验证类型**: [硬件功能测试/Skill功能测试]
**所属步骤**: [步骤名称]
**前置条件**: [已编译通过/其他]
**创建时间**: {{DATETIME}}
**S5工具**: Serial Monitor & AI Assistant

---

### 操作清单（人类执行）
- [ ] 1. 在S5工具配置串口参数
- [ ] 2. 点击连接
- [ ] 3. 执行验证操作
- [ ] 4. 观察物理现象
- [ ] 5. 口述观察结果给AI

### 预期结果
- [预期1]
- [预期2]

---

### 【人类观察输入】（AI记录口述）
| 时间 | 观察内容 |
|------|----------|
| | |

### 【AI分析】
```
[AI分析结论]
```

### 【共同决策】
```
决策: □ 通过  □ 失败  □ 部分通过  □ 不确定
原因: [决策原因]
下一步: [后续行动]
```

---

**提交命令**: /em result S<N>-通过 或 /em result S<N>-失败-[描述]
```

## S5工具启动

AI自动启动S5串口工具：

```bash
# Windows - 后台启动
start "" "EM-SKILL\tools\serial-mcp\start.bat"

# 或手动指定
start "" "python" "EM-SKILL\tools\serial-mcp\serial_monitor.py"
```

**注意**: GUI程序启动后独立运行，AI继续其他工作

## 工作流位置

```
用户: /em verify s3
   ↓
AI: 生成HVR文件（增强版）
   ↓
AI: 自动启动S5工具（后台）
   ↓
用户: 在S5工具配置串口 → 连接
   ↓
用户: 执行验证 → 口述观察
   ↓
AI: 调用MCP读取日志 → 分析 → 记录
   ↓
用户: /em result s3-通过/失败
```

## 相关文件
- workflows/hvr-workflow.md - HVR工作流细则
- tools/serial-mcp/ - S5串口工具
