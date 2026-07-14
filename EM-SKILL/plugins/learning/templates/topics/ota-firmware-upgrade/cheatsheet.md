# STM32 OTA 升级 — 速查卡

## 常用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `HAL_FLASH_Unlock()` | 解锁 Flash 写入 | 写入前必须调用 |
| `HAL_FLASH_Lock()` | 锁定 Flash | 写入后必须调用 |
| `HAL_FLASH_Program()` | 写入 Flash | `HAL_FLASH_Program(TYPEWORD, addr, data)` |
| `HAL_CRC_Calculate()` | 计算 CRC | `HAL_CRC_Calculate(&hcrc, data, len)` |
| `__set_MSP()` | 设置主栈指针 | 跳转 App 前调用 |
| `NVIC_SystemReset()` | 系统复位 | 切换分区后调用 |

## 关键参数

| 参数 | 取值 | 说明 |
|------|------|------|
| YMODEM 包大小 | 128 / 1024 / 2048 | 推荐 1024 (1K) |
| 串口波特率 | 9600 / 115200 | 推荐 115200 |
| Flash 页大小 | 1KB / 2KB | F103: 1KB (小页) |
| 双区大小 | 各 64KB / 128KB | 根据芯片 Flash 分配 |

## 地址映射

| 名称 | 地址 | 大小 | 说明 |
|------|------|------|------|
| Bootloader | 0x08000000 | 64KB | 启动代码 |
| App A | 0x08010000 | 128KB | 主程序 A 区 |
| App B | 0x08050000 | 128KB | 主程序 B 区 |
| 元数据 | 0x0800F000 | 4KB | 分区信息 |

## 快速诊断

| 现象 | 可能原因 | 排查方法 |
|------|----------|----------|
| 升级后死机 | 中断向量表未重映射 | 检查 `__set_MSP()` 调用 |
| Flash 写入失败 | 未解锁或地址不对 | 检查 `HAL_FLASH_Unlock()` 和地址对齐 |
| YMODEM 超时 | 波特率不匹配 | 确认双方波特率一致 |
| CRC 校验失败 | 数据损坏或算法错误 | 对比发送端和接收端 CRC 值 |
| 回滚无效 | 元数据未正确更新 | 检查 `write_meta()` 原子性 |
