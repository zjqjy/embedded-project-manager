## 人工验证请求 [{{HVR_ID}}]

**验证类型**: {{VERIFICATION_TYPE}}
**所属步骤**: {{STEP_NAME}}
**前置条件**: {{PREREQUISITES}}

---

### 操作清单（人工执行）

#### 步骤1: 烧录固件
- [ ] {{FLASH_STEP_1}}
- [ ] {{FLASH_STEP_2}}

#### 步骤2: 硬件连接
- [ ] {{HARDWARE_STEP_1}}
- [ ] {{HARDWARE_STEP_2}}
- [ ] {{HARDWARE_STEP_3}}
- [ ] {{HARDWARE_STEP_4}}

#### 步骤3: 上电观察
- [ ] {{OBSERVE_STEP_1}}
- [ ] {{OBSERVE_STEP_2}}
- [ ] {{OBSERVE_STEP_3}}

#### 步骤4: 波形检查（如有逻辑分析仪）
- [ ] {{WAVEFORM_STEP_1}}
- [ ] {{WAVEFORM_STEP_2}}
- [ ] {{WAVEFORM_STEP_3}}

---

### 预期结果
- {{EXPECTED_1}}
- {{EXPECTED_2}}
- {{EXPECTED_3}}

---

### 实际结果（人工填写）

#### 串口输出
```
[粘贴串口输出]
```

#### 波形观察
- [ ] {{WAVEFORM_CHECK_1}}
- [ ] {{WAVEFORM_CHECK_2}}
- [ ] {{WAVEFORM_CHECK_3}}
- [ ] {{WAVEFORM_CHECK_4}}

#### 现象描述
[描述看到的现象]

---

### 结论
- [ ] 通过（进入下一步）
- [ ] 失败（进入问题追踪）
- [ ] 部分通过（备注）: ________________

---

**提交验证结果命令**: `提交结果 {{STEP_ID}}-通过` 或 `提交结果 {{STEP_ID}}-失败-现象描述`
