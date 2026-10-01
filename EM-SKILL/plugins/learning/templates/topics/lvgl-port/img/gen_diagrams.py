#!/usr/bin/env python3
"""gen_diagrams.py — 生成 LVGL 移植讲解文档的图解 PNG (.em/learning/lvgl-port/img/)
风格沿用 .em/docs/img/gen_diagrams.py (Pillow + 微软雅黑, 扁平配色)。仅 Pillow 依赖。
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__))
FONT = "C:/Windows/Fonts/msyh.ttc"

def F(size, bold=False):
    idx = 1 if bold else 0
    return ImageFont.truetype(FONT, size, index=idx)

INK    = (55, 60, 70)
SUB    = (120, 126, 138)
BLUE   = (66, 133, 244)
BLUE_L = (232, 241, 255)
ORANGE = (240, 138, 30)
OR_L   = (255, 240, 220)
GREEN  = (52, 148, 90)
GR_L   = (226, 245, 233)
RED    = (222, 84, 74)
RD_L   = (253, 231, 229)
GRAY_L = (243, 244, 246)
YEL_L  = (255, 249, 219)
YEL_BD = (225, 200, 90)

def canvas(w, h):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    return im, ImageDraw.Draw(im)

def box(d, xy, fill, r=10, outline=None, width=2):
    d.rounded_rectangle(xy, radius=r, fill=fill,
                        outline=outline or (200, 205, 212), width=width)

def text(d, xy, s, size=20, color=INK, bold=False, anchor="la"):
    d.text(xy, s, font=F(size, bold), fill=color, anchor=anchor)

def arrow(d, p1, p2, color=INK, width=3, head=12):
    d.line([p1, p2], fill=color, width=width)
    import math
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    for da in (2.6, -2.6):
        d.line([p2, (p2[0]+head*math.cos(ang+da), p2[1]+head*math.sin(ang+da))],
               fill=color, width=width)

# ================================================================ 00 对比: 加了 LVGL 多了什么
def d00_before_after():
    im, d = canvas(960, 660)
    text(d, (30, 22), "加 LVGL 前后对比：驱动通路不变，只是渲染交给 LVGL", 27, INK, True)

    def row(y, tag, tagc, tagbg, boxes, note):
        box(d, (30, y, 930, y+180), tagbg, r=12, outline=tagc, width=2)
        text(d, (50, y+14), tag, 20, tagc, True)
        bx = 55
        for i, (title, lines, c, cbg) in enumerate(boxes):
            box(d, (bx, y+50, bx+250, y+166), (255,255,255), outline=c, width=2)
            text(d, (bx+125, y+62), title, 18, c, True, "ma")
            for j, ln in enumerate(lines):
                text(d, (bx+125, y+96+j*24), ln, 14, SUB, False, "ma")
            if i < len(boxes)-1:
                arrow(d, (bx+250, y+108), (bx+300, y+108), tagc)
            bx += 300
        text(d, (50, y+196), note, 16, SUB)

    row(64, "现在（S3 猫播放器）：计算、渲染、送显全在手写代码里", ORANGE, OR_L,
        [("cat_player.c", ["你算: 猫在哪/怎么动", "你填: 每个像素颜色"], INK, GRAY_L),
         ("S2-A 驱动", ["LCD_SetWindow(y+20)", "LCD_SendPixels DMA"], GREEN, GR_L),
         ("屏 ST7789", ["240×280 显存", "收像素就点亮"], BLUE, BLUE_L)],
        "你已经踩通的两个坑都在中栏: y+20 偏移、大端字节序")

    row(330, "加 LVGL 后：渲染交给 LVGL，驱动通路原样保留", BLUE, BLUE_L,
        [("LVGL（新增）", ["声明控件和属性", "它计算坐标并渲染进缓冲"], INK, GRAY_L),
         ("flush_cb（你写）", ["lv_draw_sw_rgb565_swap", "SetWindow(+20)+DMA"], GREEN, GR_L),
         ("屏 ST7789", ["240×280 显存", "和上面完全同一块"], BLUE, BLUE_L)],
        "LVGL 只输出『渲染好的像素块 + 目标坐标』，从不直接操作屏幕 —— 送显路线和你 S3 写的一模一样")

    box(d, (55, 580, 905, 640), YEL_L, outline=YEL_BD)
    text(d, (480, 594), "结论：移植 LVGL = 新增一个渲染库；屏、驱动、两个已踩过的坑全部复用", 18, INK, True, "ma")
    im.save(os.path.join(OUT, "00_before_after.png"))

# ================================================================ 01 角色全景
def d01_roles():
    im, d = canvas(1000, 700)
    text(d, (30, 22), "组件与数据流全景（①~⑥ 为一轮循环）", 27, INK, True)

    # ESP32 大框
    box(d, (30, 70, 700, 560), GRAY_L, r=14, outline=INK, width=2)
    text(d, (60, 84), "ESP32-S3", 20, INK, True)

    # LVGL 大框
    box(d, (55, 120, 400, 420), BLUE_L, r=12, outline=BLUE, width=2)
    text(d, (227, 134), "LVGL 渲染库", 19, BLUE, True, "ma")
    box(d, (75, 175, 380, 225), (255,255,255), outline=BLUE)
    text(d, (227, 183), "控件树: 按钮/表情/文字", 16, INK, False, "ma")
    arrow(d, (227, 225), (227, 255), BLUE)
    box(d, (75, 255, 380, 305), (255,255,255), outline=BLUE)
    text(d, (227, 263), "渲染器：只重绘变化的区域（脏区）", 16, INK, False, "ma")
    arrow(d, (227, 305), (227, 335), BLUE)
    box(d, (90, 335, 205, 400), (255,255,180), outline=YEL_BD, width=2)
    text(d, (147, 350), "缓冲 buf1", 16, INK, True, "ma")
    text(d, (147, 375), "240×40 行", 13, SUB, False, "ma")
    box(d, (245, 335, 360, 400), (255,255,180), outline=YEL_BD, width=2)
    text(d, (302, 350), "缓冲 buf2", 16, INK, True, "ma")
    text(d, (302, 375), "双缓冲轮换", 13, SUB, False, "ma")

    # flush_cb 框
    box(d, (430, 120, 680, 420), GR_L, r=12, outline=GREEN, width=2)
    text(d, (555, 134), "② flush_cb（移植代码）", 19, GREEN, True, "ma")
    code = ["lv_draw_sw_rgb565_swap", "  ← 换大端 (坑1)", "",
            "LCD_SetWindow(x1, y1+20,", "            x2, y2+20)",
            "  ← 偏移 20 (坑2)", "",
            "LCD_SendPixels (DMA)"]
    for i, ln in enumerate(code):
        c = RED if "坑" in ln else (INK if ln.strip() else SUB)
        text(d, (450, 172+i*28), ln, 15, c, ln.startswith("LCD") or "swap" in ln)
    text(d, (555, 396), "= S2-A 已写过的三件事", 14, GREEN, True, "ma")

    # 屏
    box(d, (760, 140, 960, 400), BLUE_L, r=12, outline=BLUE, width=3)
    text(d, (860, 160), "屏 ST7789", 19, BLUE, True, "ma")
    d.rectangle((790, 200, 930, 370), fill=(255,255,255), outline=INK)
    d.rectangle((800, 230, 890, 290), fill=(255, 210, 100), outline=ORANGE, width=2)
    text(d, (845, 245), "刚点亮", 14, ORANGE, True, "ma")
    text(d, (845, 260), "的那块", 14, ORANGE, True, "ma")
    text(d, (860, 440), "④ flush_ready() = 传输完成通知", 13, SUB, True, "ma")

    # 流程箭头
    arrow(d, (400, 250), (430, 250), ORANGE, 4)          # ② 画好 -> flush_cb
    arrow(d, (680, 250), (760, 250), GREEN, 4)           # ③ 发屏
    text(d, (720, 222), "③ DMA 发屏", 13, GREEN, True, "ma")
    arrow(d, (760, 340), (690, 340), INK, 2)             # ④ 回执
    arrow(d, (147, 335), (147, 312), INK, 2)             # ① 渲染进缓冲
    text(d, (58, 312), "①渲染进缓冲", 12, SUB)

    # 底部: ui_task + tick
    box(d, (55, 470, 400, 545), (255,255,255), outline=INK)
    text(d, (227, 482), "ui_task (核1, 优先级8)", 16, INK, True, "ma")
    text(d, (227, 508), "while(1){ lv_timer_handler(); delay(5ms) }", 15, SUB, False, "ma")
    box(d, (430, 470, 680, 545), (255,255,255), outline=INK)
    text(d, (555, 482), "lv_tick_set_cb（毫秒时基）", 16, INK, True, "ma")
    text(d, (555, 508), "LVGL 读取当前毫秒数 ← esp_timer", 15, SUB, False, "ma")
    arrow(d, (227, 470), (227, 430), INK, 2)
    text(d, (105, 440), "⑤ 每 5ms 调一轮渲染", 14, SUB)
    arrow(d, (500, 470), (360, 428), INK, 2)
    text(d, (480, 450), "⑥ 提供时基", 14, SUB)

    text(d, (30, 585), "②③④ 是 flush 回调内部三步；⑤⑥ 是任务与时基。移植代码合计约 40 行。", 18, INK, True)
    text(d, (30, 620), "esp_lcd（显示驱动框架）/ esp_lvgl_port（适配组件）是把②③④⑤⑥封装好的现成方案，见路线图。", 16, SUB)
    im.save(os.path.join(OUT, "01_roles.png"))

# ================================================================ 02 一帧的旅程
def d02_one_frame():
    im, d = canvas(1000, 680)
    text(d, (30, 22), "一次刷新的完整流程：手指按下按钮之后", 27, INK, True)

    steps = [
        ("1", "手指按下按钮", "触摸 INT → LVGL 记录新状态", BLUE),
        ("2", "5ms 周期到", "ui_task 调 lv_timer_handler()", INK),
        ("3", "计算脏区", "只有按钮那块变了 → 脏区 80×40", BLUE),
        ("4", "渲染进缓冲", "80×40×2 = 6.4KB, buf1 装得下", BLUE),
        ("5", "调用 flush_cb", "传入目标区域 + 缓冲区指针", ORANGE),
        ("6", "你写的那三行", "换大端 → SetWindow(+20) → DMA", GREEN),
        ("7", "屏上那块亮了", "只送 6.4KB, 不是全屏 134KB!", GREEN),
        ("8", "flush_ready 完成", "回到③继续渲染下一块, 循环", INK),
    ]
    y = 78
    for n, t, sub, c in steps:
        d.ellipse((60, y, 104, y+44), fill=c)
        text(d, (82, y+8), n, 20, (255,255,255), True, "ma")
        text(d, (120, y+2), t, 19, c, True)
        text(d, (370, y+6), sub, 16, SUB)
        if n != "8":
            arrow(d, (82, y+44), (82, y+62), (200,205,212), 2)
        y += 66

    # 右侧: 屏幕对比
    sx, sy, sw, sh = 700, 90, 240, 280
    box(d, (sx-20, sy-30, sx+sw+20, sy+sh+90), GRAY_L, outline=INK, width=2)
    text(d, (sx+sw//2, sy-22), "屏 240×280", 16, SUB, True, "ma")
    d.rectangle((sx, sy, sx+sw, sy+sh), fill=(255,255,255), outline=INK)
    text(d, (sx+30, sy+30), "表情", 18, INK); text(d, (sx+30, sy+70), "没变,不重画", 13, SUB)
    d.rectangle((sx+60, sy+130, sx+140, sy+170), fill=(255,210,100), outline=ORANGE, width=3)
    text(d, (sx+100, sy+138), "按钮", 15, ORANGE, True, "ma")
    d.line((sx+70, sy+162, sx+130, sy+162), fill=RED, width=3)
    text(d, (sx+100, sy+182), "只有这块重画", 13, RED, True, "ma")
    text(d, (sx+sw//2, sy+sh+30), "脏区 80×40 = 全屏的 4.8%", 15, INK, True, "ma")
    text(d, (sx+sw//2, sy+sh+58), "这就是 PARTIAL 模式", 14, SUB)

    box(d, (40, 610, 960, 664), YEL_L, outline=YEL_BD)
    text(d, (500, 622), "没有 UI 变化时第③步直接跳过，几乎零开销；有变化也只重绘小块", 17, INK, True, "ma")
    im.save(os.path.join(OUT, "02_one_frame.png"))

# ================================================================ 03 路线图
def d03_routes():
    im, d = canvas(1000, 630)
    text(d, (30, 22), "两条移植路线: 终点相同, 上层 UI 代码一行不改", 27, INK, True)

    # 顶部: UI 代码
    box(d, (200, 70, 800, 130), BLUE_L, outline=BLUE, width=2)
    text(d, (500, 82), "你的 UI 代码: 表情页 / 状态页 / 按钮 (表情=lv_image, 交互=lv_btn)", 18, BLUE, True, "ma")
    text(d, (500, 140), "↑ 无论下面走哪条路线, 这层写的代码完全一样 —— 这就是分层的意义", 15, SUB)

    # 路线 A
    box(d, (40, 190, 960, 380), GR_L, r=14, outline=GREEN, width=2)
    text(d, (60, 204), "路线 A · 手动移植 (现在就能做, 配合教学)", 20, GREEN, True)
    box(d, (80, 250, 300, 350), (255,255,255), outline=BLUE, width=2)
    text(d, (190, 262), "LVGL 9", 17, BLUE, True, "ma")
    text(d, (190, 290), "idf.py add-dependency", 13, SUB, False, "ma")
    text(d, (190, 312), "\"lvgl/lvgl^9\"", 13, SUB, False, "ma")
    box(d, (360, 250, 640, 350), (255,255,255), outline=GREEN, width=2)
    text(d, (500, 262), "你的 bsp_lvgl.c ≈40 行", 17, GREEN, True, "ma")
    text(d, (500, 292), "flush_cb / tick / 5ms 任务", 14, SUB, False, "ma")
    text(d, (500, 316), "三个回调自己写，每一步都看得见", 14, SUB, False, "ma")
    box(d, (700, 250, 920, 350), (255,255,255), outline=INK, width=2)
    text(d, (810, 262), "现有裸驱动", 17, INK, True, "ma")
    text(d, (810, 290), "lcd_init.c 原样复用", 13, SUB, False, "ma")
    text(d, (810, 312), "(S2-A 成果 100% 复用)", 13, GREEN, True, "ma")
    arrow(d, (300, 300), (360, 300), GREEN)
    arrow(d, (640, 300), (700, 300), GREEN)

    # 路线 B
    box(d, (40, 420, 960, 560), GRAY_L, r=14, outline=(160,168,178), width=2)
    text(d, (60, 434), "路线 B · 官方组件（S2-D 收编后）", 20, SUB, True)
    box(d, (80, 480, 280, 545), (255,255,255), outline=BLUE)
    text(d, (180, 492), "LVGL 9", 16, BLUE, True, "ma")
    box(d, (330, 480, 540, 545), (255,255,255), outline=ORANGE, width=2)
    text(d, (435, 492), "esp_lvgl_port 适配组件", 16, ORANGE, True, "ma")
    text(d, (435, 518), "自动处理: tick + 任务 + 互斥锁", 13, SUB, False, "ma")
    box(d, (590, 480, 780, 545), (255,255,255), outline=RED, width=2)
    text(d, (685, 487), "esp_lcd 显示驱动框架", 16, RED, True, "ma")
    text(d, (685, 509), "draw_bitmap 一条龙", 13, SUB, False, "ma")
    text(d, (685, 527), "需先替换裸驱动", 12, RED, True, "ma")
    arrow(d, (280, 512), (330, 512), SUB); arrow(d, (540, 512), (590, 512), SUB)
    text(d, (80, 566), "卡点：esp_lvgl_port 只认 esp_lcd 句柄 → 先替换裸驱动才能升级路线 B（顺带消灭字节序坑）", 14, SUB)

    box(d, (40, 588, 960, 618), YEL_L, outline=YEL_BD)
    text(d, (500, 593), "顺序: 先 A 后 B; A 期写的 UI 代码到 B 期原封不动", 16, INK, True, "ma")
    im.save(os.path.join(OUT, "03_routes.png"))

d00_before_after(); d01_roles(); d02_one_frame(); d03_routes()
print("4 图已生成 →", OUT)
