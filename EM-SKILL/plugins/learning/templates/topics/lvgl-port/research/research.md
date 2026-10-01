# 调研资料索引 — LVGL 显示移植

> L1-Learn 阶段产物 · 2026-09-21

## 官方文档

| 资料 | 链接 | 用途 |
|------|------|------|
| LVGL 9 Display 移植 | https://docs.lvgl.io/master/porting/display.html | flush_cb/set_buffers/渲染模式 权威出处 |
| LVGL indev 移植(触摸) | https://docs.lvgl.io/master/porting/indev.html | 下一步: CST816 接 lv_indev |
| esp_lvgl_port v2.9.0 | https://components.espressif.com/components/espressif/esp_lvgl_port | 路线 B 适配组件 |
| esp_lcd 组件 | https://components.espressif.com/components/espressif/esp_lcd | 路线 B 显示驱动框架 |
| LVGL×ESP-IDF 集成指南 | https://lvgl.io/docs/open/integration/chip_vendors/espressif/add_lvgl_to_esp32_idf_project | component manager 拉取 |
| ST7789 数据手册 | https://www.displayfuture.com/Display/datasheet/ST7789.pdf | 显存窗口/偏移依据 |

## 案例来源

- **ai_roboot 项目**（ESP32-S3-N16R8 + P169H002 1.69" ST7789 240×280 + 裸 SPI 驱动）:
  裸驱动接入 LVGL 9 的实战结论（y+20 偏移、大端字节序、PARTIAL 渲染缓冲选型）均来自该项目
  bring-up 记录；配图源脚本 [img/gen_diagrams.py](../img/gen_diagrams.py)。

## 待验证 / 进阶

- [ ] esp_lvgl_port 在 IDF 6.1 的 lock 开销实测
- [ ] LVGL 9.3 新渲染器（draw unit 抽象）对小 MCU 的收益
- [ ] 猫 GIF 播放器融合 lv_image 管线的拷贝开销
