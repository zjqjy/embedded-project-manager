# 人工验证请求 [{{HVR_ID}}] — 嵌入式扩展模板

> 嵌入式项目专用（type=embedded）。通用模板见 `templates/hvr-template.md`。
> 本模板由 `plugins/embedded/workflows/verify-embedded.md` 在 verify 阶段加载注入。

**验证类型**: {{VERIFICATION_TYPE}}
**所属步骤**: {{STEP_NAME}}
**前置条件**: {{PREREQUISITES}}
**芯片**: {{CHIP}}
**调试器**: {{INTERFACE}}

---

## 一、嵌入式执行记录（AI 自动跑三连）

| 步骤 | 工具 | 结果 | 关键产物/字段 |
|------|------|------|---------------|
| 编译 | build-keil | ⬜ 待执行 / ✅ 成功 / ❌ 失败 | 错误:N 警告:N / Flash≈N KB / `*.axf` |
| 烧录 | flash-openocd | ⬜ 待执行 / ✅ 成功 / ❌ 失败 | interface=stlink/jlink/cmsis-dap / verified |
| 串口 | serial-monitor | ⬜ 待执行 / ✅ 抓到启动日志 / ❌ 未抓到 | `logs/serial_<step>_<ts>.log` |

### 启动日志节选（serial-monitor 抓取）
```
[BOOT] ...
[INIT] ...
[LOOP] ...
```

---

## 二、操作清单（人工执行）

### 步骤 1：烧录前
- [ ] {{FLASH_PRE_1}}
- [ ] {{FLASH_PRE_2}}

### 步骤 2：硬件连接
- [ ] {{HARDWARE_STEP_1}}
- [ ] {{HARDWARE_STEP_2}}
- [ ] {{HARDWARE_STEP_3}}
- [ ] {{HARDWARE_STEP_4}}

### 步骤 3：上电观察
- [ ] {{OBSERVE_STEP_1}}
- [ ] {{OBSERVE_STEP_2}}
- [ ] {{OBSERVE_STEP_3}}

### 步骤 4：波形检查（如有逻辑分析仪）
- [ ] {{WAVEFORM_STEP_1}}
- [ ] {{WAVEFORM_STEP_2}}
- [ ] {{WAVEFORM_STEP_3}}

---

## 三、预期结果
- {{EXPECTED_1}}
- {{EXPECTED_2}}
- {{EXPECTED_3}}

---

## 四、实际结果（人工填写）

### 串口输出
```
[粘贴串口启动日志]
```

### 波形观察
- [ ] {{WAVEFORM_CHECK_1}}
- [ ] {{WAVEFORM_CHECK_2}}
- [ ] {{WAVEFORM_CHECK_3}}

### 物理现象
[LED 闪烁频率、电平、按键响应等 — 用户口述]

---

## 五、结论

- [ ] ✅ 通过
- [ ] ❌ 失败
- [ ] ⚠️ 部分通过（备注）：________________

---

## 六、AI 工具执行记录

| 时间 | 工具 | 命令 | 结果 |
|------|------|------|------|
| {{ts}} | build-keil | `keil_builder.py --project xx --target xx` | ✅/❌ |
| {{ts}} | flash-openocd | `openocd_flasher.py --interface xx ...` | ✅/❌ |
| {{ts}} | serial-monitor | `serial_monitor.py --port xx --baud xx ...` | ✅/❌ |

---

## 七、共同决策（AI + 用户）

[本次验证中达成的共同决策，会同步到 decisions.md]

---

**提交结果命令**：
- 通过：`/em result {{STEP_ID}}-通过`
- 失败：`/em result {{STEP_ID}}-失败-<现象描述>`
