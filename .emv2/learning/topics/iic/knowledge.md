# I²C / IIC — 核心概念清单（L1 Learn 阶段产物）

> 50 行起步，按"物理层 → 协议层 → 应用层 → 陷阱"四段组织。每条概念可在 [deep-dive.md](./deep-dive.md) 展开。

## 1. 物理层（4 条）

### 1.1 开漏输出 + 上拉电阻
I²C 总线只有 SCL（时钟）和 SDA（数据）两根线，所有设备（主/从）都使用**开漏（Open-Drain）/ 开集电极**输出。
- 必须外接上拉电阻（典型 4.7kΩ @ 100kHz / 2.2kΩ @ 400kHz）拉到 VCC。
- 开漏的"线与"特性允许多主机仲裁，是 I²C 多主能力的物理基础。

### 1.2 总线空闲 = 两条线都被上拉为高
STOP 之后 SDA/SCL 都为高。任何一方拉低即视为占用。

### 1.3 电平不匹配 = 上拉接到错的 VCC
3.3V MCU 配 5V 从机：上拉必须接到 **3.3V**（不是 5V），否则 SDA 高电平会被钳位在 3.3V，从机读到低。反之同理需电平转换器（如 BSS138 MOSFET）。

### 1.4 总线电容 ≤ 400pF
规定了最大上升时间和总线物理长度上限（典型 ≤ 1m）。超过会出现上升沿过缓、时序违例。

---

## 2. 协议层（10 条）

### 2.1 START 条件（S）
SCL 高电平期间，SDA **从高到低**的下降沿。

### 2.2 STOP 条件（P）
SCL 高电平期间，SDA **从低到高**的上升沿。

### 2.3 重复 START（Sr / Repeated START）
主机不发 STOP、紧接着再发 START。常用于"读 → 切换方向 → 读"而不释放总线。

### 2.4 数据有效性
SCL 高电平期间 SDA 必须稳定；只有 SCL 低电平时 SDA 才允许变化。

### 2.5 ACK / NACK（第 9 个时钟）
- **ACK**：从机在第 9 个 SCL 高电平期间拉低 SDA → 数据/地址已被接收。
- **NACK**：从机不拉低 → 接收失败 / 主机读最后一字节通知从机"不要更多数据"。

### 2.6 7-bit 寻址（主流）
```
[S] [A6 A5 A4 A3 A2 A1 A0 R/W] [ACK] [DATA...] [P]
```
地址字节 = 7 位从机地址 + 1 位 R/W（0=写 / 1=读）。地址范围 `0x00~0x7F`，其中 `0x00` 保留为通用广播，`0x78~0x7F` 部分保留。

### 2.7 10-bit 寻址（扩展）
首字节格式 `11110 A9 A8 R/W`，第二字节 `A7~A0`。用于从机数 > 127 的场景，极少用。

### 2.8 三种典型事务
- **主机写**：S → 地址+W → ACK → DATA → ... → P
- **主机读**：S → 地址+R → ACK → DATA → ... → NACK → P（最后一字节主机发 NACK）
- **复合（写寄存器）**：S → 地址+W → ACK → reg → ACK → Sr → 地址+R → ACK → DATA → NACK → P

### 2.9 时钟拉伸（Clock Stretching）
按 NXP UM10204 §3.1.9：从机（target）在 ACK 后**主动拉低 SCL**，迫使主机等待。规范分两个层级：
- **byte-level**：从机收到字节后需要时间存储/准备下一字节（handshake，见 spec Figure 7）。
- **bit-level**：从机处理单个 bit 都需要更多时间。
> **规范明文**：Clock stretching is optional；多数从机**不含 SCL 驱动**所以不支持；而**主机（controller）必须支持**两种层级。
> **Rev. 7.0 术语变化**：master/slave → controller/target（对齐 MIPI I3C）；章节编号相对 Rev. 6 有偏移。
> 软件模拟主机不支持时会导致从机丢数据或主机误判超时。

### 2.10 总线仲裁（多主机）
多主机同时发 START 时，遵循"线与"规则：
- 谁先发高、对方发低 → 对方赢，自己立刻转为从机监听。
- 数据阶段仲裁保证最终只有一个主机完成完整事务。

---

## 3. 速度档位（5 条）

| 模式 | 速率 | 上拉典型值 | 备注 |
|------|------|-----------|------|
| Standard-mode | 100 kHz | 4.7 kΩ | 最常见 |
| Fast-mode | 400 kHz | 2.2 kΩ | 多数传感器支持 |
| Fast-mode Plus | 1 MHz | 1 kΩ | 较少见 |
| High-speed | 3.4 MHz | 需主动上拉 | 主从都要 HS 模式握手 |
| Ultra Fast | 5 MHz | 单向推挽 | **无仲裁能力**，非真正 I²C |

---

## 4. 应用层（6 条）

### 4.1 i2cdetect 扫描地址
```bash
i2cdetect -y 1          # 扫总线 1 上所有地址
i2cdetect -y -r 1       # 快速模式（read）
```
看到 `UU` 表示被驱动占用，`--` 表示无应答，`XX` 是该地址有应答。

### 4.2 i2cdump 读全部寄存器
```bash
i2cdump -y 1 0x50       # dump 地址 0x50 全部 256 寄存器
```

### 4.3 i2cget / i2cset 读写单寄存器
```bash
i2cget -y 1 0x50 0x00           # 读
i2cset -y 1 0x50 0x00 0xFF      # 写
```

### 4.4 常见从机地址速记
- `0x50~0x57`：AT24C 系列 EEPROM（地址脚 A0/A1/A2 决定）
- `0x68`：MPU6050 / DS3231
- `0x3C / 0x3D`：SSD1306 OLED（看 SA0 脚）
- `0x1E`：HMC5883L / LSM303
- `0x39 / 0x29`：TSL2561 / VL53L0X

### 4.5 平台抽象层
裸机：HAL_I2C_Master_Transmit / Master_Receive；
Linux：`/dev/i2c-N` + ioctl(I2C_RDWR)；
RTOS：建议互斥锁保护总线，因为 I²C 慢速但常被多任务共享。

### 4.6 GPIO 模拟 vs 硬件外设
- 硬件外设：CPU 占用低、时序准、支持 DMA/中断；
- GPIO 模拟（bitbang）：可换引脚、调试方便、引脚冲突时备用；
- 生产代码优先用硬件外设，bitbang 仅做 fallback。

---

## 5. 陷阱与踩坑（10 条）⭐ 高频考点

### 5.1 总线死锁（SDA 一直被拉低）
**症状**：`i2cdetect` 全 `UU` 或全无应答；总线永远 busy。
**原因**：从机异常（如 MCU 复位中）拉低 SDA 没释放。
**规范名**：UM10204 Rev. 03 §3.1.16 **Bus clear**。
**恢复步骤**（Linux kernel 官方实现 + 实战博客交叉验证）：
1. 检测 SDA 持续低电平 ≥ N ms
2. 主机推 **9 个 SCL 脉冲**（GPIO 模拟 / 或用 controller 硬件产生 dummy clocks）—— 把从机卡在 ACK 位的那一位"拿走"
3. SDA 恢复高后，发一个 **STOP** 完整复位总线
4. 重新初始化 I²C 外设（HAL: `HAL_I2C_DeInit` + `HAL_I2C_Init`）
> 参考：Linux commit `i2c: Add bus recovery infrastructure`（提供 generic `i2c_recover_bus()`，要么走 controller，要么走 GPIO 模拟）。

### 5.2 地址冲突
两个从机跳线到相同地址 → 谁都不应答。`i2cdetect` 看不到地址或两个地址混淆。

### 5.3 上拉电阻太大
SDA 上升沿过缓，时序违例。表现为偶尔成功偶尔失败。
**估算公式**：`R_pullup ≤ (t_rise) / (0.8473 × C_bus)`，C_bus 一般按 10pF/器件 + 5pF/线估算。

### 5.4 上拉电阻太小
灌电流过大（超过 3mA），可能烧毁 MCU 引脚或从机。高速模式更要小心。

### 5.5 主机不支持 Clock Stretching
从机较慢时丢字节。验证方法：逻辑分析仪看 SCL 是否被从机拉长。

### 5.6 10-bit 寻址兼容性
不是所有 HAL 都默认支持，读驱动源码确认。

### 5.7 重复 START 时序错误
常见错误：发完 Sr 后漏 Sr 后的 ACK 等待。逻辑分析仪最容易抓到。

### 5.8 电平不匹配（上拉接到错误电压）
3.3V 主机 + 5V 从机，上拉接 5V → 高电平被钳位 → 从机读到逻辑低，地址错乱。

### 5.9 读最后一字节忘发 NACK
最后一字节应主机回 NACK，否则从机会误以为还有下一字节，拉低 SDA 等数据。

### 5.10 多任务未加锁
RTOS 下两个任务同时操作同一 I²C 总线 → 事务错乱，常见于传感器轮询与用户命令冲突。

---

## 6. 自检清单（L1 完成信号）

- [ ] 能用 3 句话讲清 I²C（线与/开漏/同步时钟）
- [ ] 能默写 7-bit 写事务的完整时序：`S → ADDR+W → ACK → DATA → ACK → ... → P`
- [ ] 能解释 5.1（总线死锁）的恢复原理
- [ ] 能说出 3 种典型从机地址（EEPROM / IMU / OLED）
- [ ] `bib.json` ≥ 3 条引用已落地

---

## 7. 引用与下一步

- **bib.json**：见 [research/bib.json](./research/bib.json)（待 L1 调研阶段补全）
- **L2 Pack**：基于本文件 + bib.json 生成 `knowledge-pack.md` + 概念图
- **L3 Practice**：`/em new iic-scan` 起手做最小 demo

---

*Stage: L1-Learn · Drafted 2026-07-14 · 130+ 行覆盖物理/协议/应用/陷阱四段*