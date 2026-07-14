# Hardware Alignment — S10: EM-SKILL 学习模式升级 v4.1

## 存储资源

### Git 仓库约束
- GitHub 免费仓库推荐: < 1GB
- 策略: 仓库只存文本 + 小图，大文件存外部

### 文件大小控制
| 类型 | 策略 | 上限 |
|------|------|------|
| Markdown | 正常存储 | 无限制（文本） |
| SVG 图表 | 正常存储 | < 10KB |
| PNG 截图 | 压缩后存储 | < 500KB |
| 视频 | 外部链接 | 不存仓库 |
| PDF | 外部链接 | 不存仓库 |
| HTML 构建产物 | CI 生成 | 不提交 |

## 构建环境

### 本地构建
- Python 3.11+
- 依赖: `pip install markdown pymdown-extensions`

### CI/CD
- GitHub Actions (ubuntu-latest)
- 触发: push to .em/learning/**
- 部署: GitHub Pages

## 运行时依赖

### 必须
- Claude Code CLI (skill 加载)
- Git (版本控制)

### 可选
- QEMU (system-arm) — 实验环境
- OpenOCD — 烧录调试
- Docker — 容器化实验

## 兼容性

### 与现有系统
- .em/learning/ 独立目录，不与 .emv2/ 混
- 与 HVR (项目开发) 平行互补
- 复用 /em new 三档、/em verify、serial-mcp

### 向后兼容
- v3.x 工程管理功能零破坏
- v4.x 学习模式可选启用

---
生成时间: 2026-07-13 23:20
