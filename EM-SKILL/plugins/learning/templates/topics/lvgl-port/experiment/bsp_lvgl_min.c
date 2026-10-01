/* bsp_lvgl_min.c — LVGL 9 显示移植最小移植层 (ESP-IDF + 裸 SPI 驱动上桥)
 *
 * 实验目标: 路线 A 手动移植 —— 约 40 行接通三个接口
 * 前置: lcd_set_window()/lcd_send_pixels() 为项目已有裸驱动接口
 *       (任何"设窗口+灌像素"式驱动都能对上)
 * 依赖: idf.py add-dependency "lvgl/lvgl^9"
 * 验证: 两步分离
 *   1) my_flush_cb 只保留 lv_display_flush_ready() → 烧板不崩 = LVGL 层通
 *   2) 放开三行真发送 → 出图 = 显示层通
 */
#include "lvgl.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/* ---- 你的屏: 换成实际分辨率与偏移 ---- */
#define MY_HOR_RES      240
#define MY_VER_RES      280
#define MY_Y_OFFSET     20      /* ST7789 240x280: 可视区=显存[20..299] */
#define BUF_LINES       40      /* 缓冲行数: 20~60, 40 是推荐值 */

/* ---- 你的裸驱动 extern (在 lcd_init.c 实现) ---- */
extern void lcd_set_window(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2);
extern void lcd_send_pixels(const uint16_t *px, uint32_t n);

static lv_display_t *s_disp;

/* 渲染缓冲放内部 RAM (静态数组即在内部), 别放 PSRAM */
static uint8_t buf1[MY_HOR_RES * BUF_LINES * 2];
static uint8_t buf2[MY_HOR_RES * BUF_LINES * 2];

static uint32_t my_get_ms(void)
{
    return (uint32_t)(esp_timer_get_time() / 1000);
}

static void my_flush_cb(lv_display_t *disp, const lv_area_t *area, uint8_t *px_map)
{
    uint32_t n = lv_area_get_size(area);

    /* 坑1: LVGL 小端渲染 -> ST7789 要大端, 发前交换 */
    lv_draw_sw_rgb565_swap(px_map, n);

    /* 坑2: 屏幕玻璃偏移, 设窗时补偿 */
    lcd_set_window(area->x1, area->y1 + MY_Y_OFFSET,
                   area->x2, area->y2 + MY_Y_OFFSET);

    lcd_send_pixels((const uint16_t *)px_map, n);   /* 阻塞 DMA */

    lv_display_flush_ready(disp);                   /* 忘调 = 只出第一块就冻结 */
}

void bsp_lvgl_init(void)
{
    lv_init();
    lv_tick_set_cb(my_get_ms);                 /* 毫秒时基 */

    s_disp = lv_display_create(MY_HOR_RES, MY_VER_RES);
    lv_display_set_flush_cb(s_disp, my_flush_cb);
    lv_display_set_buffers(s_disp, buf1, buf2, sizeof(buf1),
                           LV_DISPLAY_RENDER_MODE_PARTIAL);
}

/* ui_task: 钉核1(核0留给WiFi), 优先级8, 栈16KB */
void ui_task(void *arg)
{
    bsp_lvgl_init();

    /* TODO: 在这里建你的 UI —— lv_btn / lv_label / lv_image */
    /* lv_obj_t *btn = lv_btn_create(lv_screen_active());
     * lv_obj_set_size(btn, 80, 40);
     * lv_obj_center(btn); */

    while (1) {
        lv_timer_handler();             /* 驱动一轮渲染 */
        vTaskDelay(pdMS_TO_TICKS(5));   /* 5ms 周期 */
    }
}

/* 启动: xTaskCreatePinnedToCore(ui_task, "ui", 16384, NULL, 8, NULL, 1); */
