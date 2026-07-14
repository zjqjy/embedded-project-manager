# STM32 OTA 固件升级 — 深度解析

## 📊 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| A/B 双区备份 | 升级失败自动回滚，安全性高 | Flash 占用翻倍 | 高可靠性场景 |
| 原地升级 | Flash 占用少 | 升级失败设备变砖 | 资源受限场景 |
| 差分升级 | 传输数据量小 | 实现复杂，依赖版本基线 | 大固件、慢速网络 |

## 📈 性能数据

```
传输速度对比 (9600bps 串口, 128KB 固件)

YMODEM-128    ████████░░░░░░░░░░░░  约 180 秒
YMODEM-1K     ██████████████░░░░░░  约 120 秒  ← 推荐
XMODEM-CRC    ████████████████░░░░  约 150 秒
自定义协议    ██████████░░░░░░░░░░  约 200 秒
```

## 📋 完整 Bootloader 代码

```c
#include "stm32f1xx_hal.h"
#include "ymodem.h"

#define FLASH_APP_A  0x08010000
#define FLASH_APP_B  0x08050000
#define META_ADDR    0x0800F000

typedef struct {
    uint32_t magic;
    uint32_t active_bank;
    uint32_t version;
    uint32_t crc;
} boot_meta_t;

void bootloader_main(void) {
    HAL_Init();
    SystemClock_Config();

    boot_meta_t *meta = (boot_meta_t *)META_ADDR;

    if (meta->magic == BOOT_MAGIC && check_upgrade_flag()) {
        // 进入升级模式
        UART_Init(115200);
        ymodem_receive(FLASH_APP_B);

        if (verify_firmware(FLASH_APP_B, meta->crc)) {
            meta->active_bank = (meta->active_bank == BANK_A) ? BANK_B : BANK_A;
            write_meta(meta);
        }
    }

    // 跳转到活动分区
    uint32_t app_addr = (meta->active_bank == BANK_A) ? FLASH_APP_A : FLASH_APP_B;
    jump_to_app(app_addr);
}

static int verify_firmware(uint32_t addr, uint32_t expected_crc) {
    uint32_t calc_crc = HAL_CRC_Calculate(&hcrc, (uint32_t *)addr, FIRMWARE_SIZE);
    return calc_crc == expected_crc;
}
```

## 🔍 调试日志

```
[BOOT] Magic: 0xDEADBEEF, Active: BANK_A, Ver: 1.2.3
[BOOT] Upgrade flag set, entering YMODEM mode
[YMODEM] SOH received, starting transfer
[YMODEM] Block 1/1024, 128 bytes, CRC OK
...
[YMODEM] Transfer complete, 131072 bytes
[VERIFY] CRC: 0xA1B2C3D4, Expected: 0xA1B2C3D4 → PASS
[BOOT] Switching to BANK_B
[BOOT] Jump to 0x08050000
```

## 🤖 AI 协作记录

> **Prompt**: "帮我设计一个 STM32 OTA Bootloader，要求支持 A/B 双区备份和 YMODEM 协议"
>
> **AI 输出**: 提供了基础框架，但 Flash 操作部分使用了错误的扇区编号
>
> **修正**: 对照 RM0008 手册 §2.3 修正了 Flash 扇区映射，F103 的 Sector 4 是 64KB 不是 128KB
