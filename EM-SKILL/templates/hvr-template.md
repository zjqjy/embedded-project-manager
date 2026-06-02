# 人工验证请求 [{{HVR_ID}}]

> 通用项目模板（type=general）。嵌入式项目模板见 `plugins/embedded/templates/hvr-template-embedded.md`。

**验证类型**: {{VERIFICATION_TYPE}}
**所属步骤**: {{STEP_NAME}}
**前置条件**: {{PREREQUISITES}}

---

## 一、验证操作（人工或脚本执行）

### 步骤 1：准备
- [ ] {{SETUP_STEP_1}}
- [ ] {{SETUP_STEP_2}}

### 步骤 2：运行
- [ ] {{RUN_STEP_1}}
- [ ] {{RUN_STEP_2}}

### 步骤 3：观察
- [ ] {{OBSERVE_STEP_1}}
- [ ] {{OBSERVE_STEP_2}}

---

## 二、预期结果

- {{EXPECTED_1}}
- {{EXPECTED_2}}
- {{EXPECTED_3}}

---

## 三、实际结果（验证后填写）

### 输出 / 现象
```
[粘贴命令输出 / 日志 / 截图描述]
```

### 检查清单
- [ ] {{CHECK_1}}
- [ ] {{CHECK_2}}
- [ ] {{CHECK_3}}

### 现象描述
[一段话描述实际观察到的现象，含与预期的差异]

---

## 四、结论

- [ ] ✅ 通过（进入下一步）
- [ ] ❌ 失败（进入问题追踪）
- [ ] ⚠️  部分通过（备注）：________________

---

## 五、签字

- **执行人**: {{EXECUTOR}}
- **日期**: {{DATE}}
- **会话**: {{SESSION_ID}}

---

**提交结果命令**：
- 通过：`/em result {{STEP_ID}}-通过`
- 失败：`/em result {{STEP_ID}}-失败-<现象描述>`

> 💡 嵌入式项目额外有「嵌入式执行记录」表（编译/烧录/串口三连），由 verify-embedded.md 注入。
