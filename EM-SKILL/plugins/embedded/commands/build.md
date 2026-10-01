# 编译 (build — adapter 路由)

> S17-B：本命令按 `project.json.embedded.build` 从 `tools/registry.json` 路由到具体 adapter。
> 默认 keil；TI 项目为 ccs。新增构建工具只改 registry，本文件不变。

## 第 0 步: 解析 adapter

1. 读 `project.json.embedded.build`（无 → 提示 `/em initem` 锁定组合）
2. adapter 脚本 = `tools/` + `registry.json → adapters.build.<name>.file`

## keil adapter（默认）

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/adapters/build/keil.py \
  --project <工程文件> \
  --target <目标名>
```

### 参数来源

| 参数 | 来源 |
|------|------|
| `--project` | 扫描工作区的 .uvprojx/.uvproj 文件 |
| `--target` | 使用工程中第一个 Target，或由用户指定 |
| UV4 路径 | 自动从 tool_config 读取（由 `/em initem` 注册） |

## ccs adapter（TI 工程，S17-C）

### 调用方式

```bash
python EM-SKILL/plugins/embedded/tools/adapters/build/ccs.py \
  --project <CCS 工程目录> \
  --workspace <临时 workspace> \
  [--configuration Debug]
```

| 参数 | 来源 |
|------|------|
| `--project` | 扫描 `.project` / `.ccsproject` 所在目录 |
| `--workspace` | 默认 `<STATE_DIR>/cache/ccs-workspace`（可复用） |
| eclipsec 路径 | tool_config 的 `ccs` key（initem 注册） |

## 检测工程

AI 自动在工作区中查找工程文件：

```bash
python -c "
from pathlib import Path
for p in Path('.').rglob('*.uvprojx'): print(p)
for p in Path('.').rglob('*.uvproj'):  print(p)
for p in Path('.').rglob('.ccsproject'): print(p.parent)
"
```

## 结果处理

AI 从脚本 stdout 中提取以下字段记录到 HVR：

| 字段 | 作用 |
|------|------|
| 编译状态 | ✅ 成功 / ❌ 失败 |
| 错误数/警告数 | `错误: N  警告: N` |
| 固件大小 | `Flash ≈ N KB  RAM ≈ N KB` |
| 产物路径 | `产物: file.axf/.out (N KB)` |

## 自动决策

**编译成功 → 自动进入烧录流程**（AI 连续执行，用户只需观察物理现象）

```
编译(AI执行) → 烧录(AI执行) → 串口监控(AI抓日志) → 用户口述观察结果
```

**编译失败** → 读取编译日志 → 分析错误 → 请求用户修复

## 常见错误

- ❌ 未找到工程文件 → 确认工程文件路径
- ❌ UV4 / eclipsec 路径配置错误 → 运行 `/em initem` 重新配置
- ❌ 编译错误 → 显示错误行号和内容，分析原因

## 相关文件
- `tools/registry.json` — 能力矩阵（adapter 路由）
- `tools/adapters/build/keil.py` / `ccs.py` — 编译 adapter
- `commands/flash.md` - 烧录说明
- `commands/serial.md` - 串口监控说明
