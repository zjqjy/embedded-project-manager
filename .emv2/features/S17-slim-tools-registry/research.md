# research: S17 — GitHub 工具调研（已裁决：默认不集成）

> 2026-10-01 调研，同日用户裁决：**「好像都没什么用」——全部不进当前集成计划。**
> 原因复盘：清单按「生态里有什么」拼装，未按「verify 循环缺什么」筛选。现有闭环（编译→烧录→串口→人观察）已被 Keil/OpenOCD/serial-mcp 覆盖，TI 格子缺的 CCS/DSLite 无现成可抄、只能自写。本文件降级为**后备清单**：出现具体痛点再按需引入单项。

## 裁决记录

| 候选 | 裁决 | 触发重评的条件（如果哪天出现） |
|------|------|------|
| embedded-debugger-mcp | ❌ 不集成 | 出现「AI 需要主动打断点/读内存定位问题」的高频场景（现模式：人开 Keil/CCS 图形调试器） |
| Renode | ❌ 不集成 | 需要无硬件 CI 回归，且愿意为自研板建模外设 |
| Bloaty | ❌ 不集成 | 项目逼近 Flash 容量，需要逐 commit 体积回归跟踪 |
| cppcheck / clang-tidy | ❌ 不集成 | 代码质量事故驱动，而非预防性引入 |
| probe-rs / pyOCD | ❌ 不集成 | OpenOCD 覆盖不了的新探针/新芯片时再看 |
| J-Link MCP | ❌ 不集成 | 买到 J-Link 且 OpenOCD 不够用时 |
| PlatformIO / puncover / Wokwi | ❌ 不集成 | 新项目放弃 Keil 工作流时（可能性低） |

## S17 真正要做的（工具部分）

组织现有的，不引入新的：

1. `adapters/{build,flash,observe}/` 收编现有 keil_builder / openocd_flasher / serial_monitor（S17-B）
2. `registry.json` 能力矩阵：st / gd 先行（S17-B）
3. **唯一新增 adapter：ccs.py + dslite.py**——slack_app（TMS320F280033）等着用，无现成可抄（S17-C）

## 原始调研记录（存档备查）

- [embedded-debugger-mcp](https://github.com/adancurusul/embedded-debugger-mcp)：Rust MCP server，probe-rs/OpenOCD 后端，flash/断点/读写内存，ARM Cortex-M + RISC-V
- [probe-rs](https://probe.rs) / [pyOCD](https://pyocd.io)：统一调试器，target YAML / CMSIS-Pack 驱动
- [Bloaty](https://github.com/google/bloaty)：二进制体积剖析 + build 间 diff
- [Renode](https://interrupt.memfault.com/blog/test-automation-renode)：确定性仿真 + [renode-test-action](https://github.com/antmicro/renode-test-action)
- [cppcheck](https://www.cppcheck.com/)：C/C++ 静态分析
- [spec-kit](https://github.com/github/spec-kit) / [superpowers](https://github.com/obra/superpowers) / [claude-task-master](https://github.com/eyaltoledano/claude-task-master)：状态组织借鉴（这条**有效**，已用于 brainstorm 的结构收敛设计）
