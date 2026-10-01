# 烧录 (flash — adapter 路由)

> S17-B：本命令按 `project.json.embedded.flash` 从 `tools/registry.json` 路由到具体 adapter。
> 默认 openocd；TI 项目为 dslite。新增烧录工具只改 registry，本文件不变。

## 第 0 步: 解析 adapter

1. 读 `project.json.embedded.flash` + `flash_args`（无 → 提示 `/em initem` 锁定组合）
2. adapter 脚本 = `tools/` + `registry.json → adapters.flash.<name>.file`

## openocd adapter（默认）

### 先探测环境

```bash
python EM-SKILL/plugins/embedded/tools/adapters/flash/openocd.py --detect
```

确认 OpenOCD 可用且调试探针已连接。

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/adapters/flash/openocd.py \
  --artifact <产物路径> \
  --interface stlink \
  --target <flash_args.target_cfg>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--artifact` | 从 build 的产物路径获取（AXF/ELF） |
| `--interface` | 从 `--detect` 探测结果获得（stlink/jlink/cmsis-dap） |
| `--target` | **`project.json.embedded.flash_args.target_cfg`**（registry 默认值，不再人工记芯片↔cfg 对应） |

## dslite adapter（TI XDS100/XDS110，S17-C）

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/adapters/flash/dslite.py \
  --artifact <.out/.hex 产物> \
  --ccxml <flash_args.ccxml> \
  [--reset-after]
```

| 参数 | 来源 |
|------|------|
| `--artifact` | ccs build 的产物（.out） |
| `--ccxml` | `flash_args.ccxml`（目标配置，CCS 导出或工程内 user_files） |
| dslite 路径 | tool_config 的 `dslite` key（initem 注册，通常在 CCS 安装目录 ccs/ccs_base/common/uscif/） |

## 结果处理

| 字段 | 检查要点 |
|------|----------|
| 烧录状态 | success / failure |
| 校验状态 | verified / skipped |
| 失败分类 | connection-failure / target-response-abnormal / project-config-error |

## 自动决策

- 烧录成功 → 提示下一步（串口观察启动日志）
- 烧录失败 → 根据失败分类引导排查

## 常见错误

| 错误类型 | 原因 | 解决方案 |
|----------|------|----------|
| connection-failure | 调试器未连接或驱动问题 | 检查调试器连接、USB驱动 |
| target-response-abnormal | 芯片未进入调试模式 | 检查芯片供电、复位电路 |
| project-config-error | target 配置文件与芯片不匹配 | 检查 --target / --ccxml 参数 |
| Unsupported transport | --interface 参数错误 | 使用正确的接口类型 (stlink/jlink/cmsis-dap) |

## 注意事项

⚠️ **--interface 必须与烧录时使用的接口一致**（openocd）
⚠️ **--target / --ccxml 必须匹配实际芯片型号**（来源：registry + initem 锁定）

## 相关文件
- `tools/registry.json` — 能力矩阵（adapter 路由）
- `tools/adapters/flash/openocd.py` / `dslite.py` — 烧录 adapter
- `commands/build.md` - 编译说明
- `commands/serial.md` - 串口监控说明
