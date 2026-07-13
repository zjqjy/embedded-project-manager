# I²C / IIC — 深度解析

> 占位文档（L1-Learn 骨架）—— 完整架构详解在 L2 Pack / L3 Practice 阶段产出。

## 📊 方案对比（占位）

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| {{硬件 I2C 外设}} | ... | ... | ... |
| {{软件 bitbang}} | ... | ... | ... |
| {{IO 模拟}} | ... | ... | ... |

## 📈 性能数据（占位）

```
{{ASCII 性能图 或 表格}}
```

## 📋 完整代码（占位）

```c
/* I2C Master 发送 + 接收示例（HAL 风格） */
HAL_StatusTypeDef i2c_master_tx_rx(I2C_HandleTypeDef *hi2c,
                                    uint16_t dev_addr,
                                    uint8_t *tx_buf, uint16_t tx_len,
                                    uint8_t *rx_buf, uint16_t rx_len)
{
    HAL_StatusTypeDef status;
    status = HAL_I2C_Master_Transmit(hi2c, dev_addr << 1,
                                      tx_buf, tx_len, 1000);
    if (status != HAL_OK) return status;
    return HAL_I2C_Master_Receive(hi2c, (dev_addr << 1) | 0x01,
                                   rx_buf, rx_len, 1000);
}
```

## 🔍 调试日志（占位）

- 待 L3/L4 阶段补：编译/链接/运行时报错及定位

## 🤖 AI 协作记录（占位）

> **Prompt**: {{关键 prompt}}
> **结果**: {{AI 输出摘要}}
> **修正**: {{实际修正点}}

---

*Skeleton from `topic-deep-dive.md` template · 2026-07-13*