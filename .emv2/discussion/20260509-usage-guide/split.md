# 需求拆分 - 20260509-usage-guide

## 日期
2026-05-09

## 需求描述
为串口工具增加使用说明，并建立触发机制

## 子系统/模块

### 1. 使用说明索引
- 类型：配置/文档
- 简述：在项目 CLAUDE.md 增加使用说明索引章节

### 2. EM-SKILL 命令文件
- 类型：文档/命令
- 简述：在 EM-SKILL/commands/ 下创建 build.md, flash.md, serial.md

### 3. 项目初始化集成
- 类型：流程
- 简述：修改 si.md 和 init.md，在项目初始化时创建 CLAUDE.md

## 涉及的 EM-SKILL 工具
- build-keil - 编译工具
- flash-openocd - 烧录工具
- serial-monitor - 串口监控工具

## 结论
✅ 确认拆分结果
