/* main.c — STM32F407VET6 LED Blinker (PA0)
 * EM-SKILL test-runs/embedded-blink  S1: 方案 A 阻塞延时
 * 注意：此文件用于 mock 验收，未真实编译。
 */
#include "stm32f4xx.h"

static void uart1_puts(const char *s);
static void delay_ms(volatile uint32_t ms);

int main(void)
{
    /* === S1-A: GPIO PA0 初始化 === */
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    GPIOA->MODER  &= ~(3U << (0 * 2));
    GPIOA->MODER  |=  (1U << (0 * 2));   /* PA0 = output */
    GPIOA->OTYPER &= ~(1U << 0);          /* push-pull */
    GPIOA->OSPEEDR &= ~(3U << (0 * 2));   /* low speed */
    GPIOA->PUPDR  &= ~(3U << (0 * 2));    /* no pull */

    uart1_puts("[BOOT] LED Blinker v1.0\r\n");
    uart1_puts("[GPIO] PA0 init OK\r\n");

    /* === S1-B: 主循环闪烁 === */
    while (1) {
        GPIOA->BSRR = (1U << 0);          /* set PA0 */
        delay_ms(500);
        GPIOA->BSRR = (1U << (0 + 16));   /* reset PA0 */
        delay_ms(500);
        uart1_puts("[LOOP] toggling...\r\n");
    }
}

static void uart1_puts(const char *s) { (void)s; /* mock */ }
static void delay_ms(volatile uint32_t ms) { while (ms--) for (volatile int i = 0; i < 4000; i++); }
