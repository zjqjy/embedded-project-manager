# LVGL 显示移植 — 速查卡

## 核心 API（显示移植只需这 8 个）

| API | 说明 | 备注 |
|-----|------|------|
| `lv_init()` | 初始化 LVGL | 最先调用，一次 |
| `lv_tick_set_cb(fn)` | 注册毫秒时基 | `esp_timer_get_time()/1000` |
| `lv_display_create(w, h)` | 创建显示器 | 返回 `lv_display_t*` |
| `lv_display_set_flush_cb(d, fn)` | 注册送显回调 | LVGL 每渲染完一块调用一次 |
| `lv_display_set_buffers(d, b1, b2, sz, mode)` | 注册渲染缓冲 | 传两块 = 双缓冲 |
| `lv_display_flush_ready(d)` | 完成通知 | 忘调 = 只出第一块就冻结 |
| `lv_draw_sw_rgb565_swap(buf, n)` | 小端转大端 | flush_cb 里发屏前调 |
| `lv_timer_handler()` | 主循环驱动 | 5ms 一次，别在中断里调 |

## 渲染缓冲模式

| 模式 | 渲染缓冲 | 场景 |
|------|------|------|
| `LV_DISPLAY_RENDER_MODE_PARTIAL` | 小块（如 240×40 行 ×2） | 默认推荐 |
| `LV_DISPLAY_RENDER_MODE_DIRECT` | 全屏 ×1~2 | 复杂叠层 |
| `LV_DISPLAY_RENDER_MODE_FULL` | 全屏 ×1 | 简单场景 |

## 关键参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 缓冲行数 | 20~60 行 | 越大越快越费内存，40 行是推荐值 |
| 缓冲位置 | 内部 RAM | PSRAM 有 cache/DMA 抖动 |
| ui_task 周期 | 5ms | 过大动画卡顿，过小空耗 |
| ui_task 栈 | 16KB | 渲染递归深 |
| ui_task 核心 | 核 1 | 核 0 留给 WiFi/协议栈 |
| `lvgl/lvgl` 组件 | `^9` | `idf.py add-dependency` |
| SPI 时钟 | 40MHz 起 | 花屏再降（案例 26→40 实测翻倍 fps） |

## 坑速查（症状 → 病根 → 药方）

| 症状 | 病根 | 药方 |
|------|------|------|
| 红蓝互换 | RGB565 字节序 | flush_cb 里 `lv_draw_sw_rgb565_swap` |
| 画面错位/白边 | 屏玻璃偏移（如 [20..299]） | 设窗时 y+OFFSET |
| 只出第一块就冻结 | 忘 `flush_ready` | 发送完成处补调 |
| 显示对但动画/触摸死 | tick 没接 | `lv_tick_set_cb` 真毫秒 |
| 黑屏 | 层次不明 | 两步分离：先空 flush 验不崩，再接真发送验出图 |
| 花屏/撕裂 | 缓冲放 PSRAM 或对齐问题 | 缓冲回内部 RAM，并对齐 cache 行 |

## 调试口诀

1. **先空后真**：flush_cb 只调 `flush_ready()` → 不崩 = LVGL 层通
2. **纯色标偏**：全屏红/绿/蓝各 1s，标定偏移与字节序
3. **症状定层**：显示错 → 查 flush_cb；动画死 → 查 tick；不出块 → 查 `lv_timer_handler` 有没有被调

## 路线 B 一页纸（esp_lvgl_port）

```c
esp_lvgl_port_cfg_t cfg = { .task_priority = 8, .task_stack = 16384, ... };
esp_lvgl_port_init(&cfg);
esp_lvgl_port_display_cfg_t disp_cfg = {
    .io_handle = io_handle, .panel_handle = panel_handle,   // 只认 esp_lcd 句柄!
    .buffer_size = 240 * 40, .double_buffer = true,
    .swap_bytes = true,                                     // 大端坑交给它
};
lv_disp_t *disp = esp_lvgl_port_add_disp(&disp_cfg);
/* UI 前后: lvgl_port_lock() / lvgl_port_unlock() */
```
