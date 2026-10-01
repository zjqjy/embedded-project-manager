# 命令: /em learn humanize <topic-slug>

## 功能

对主题的讲解产物执行去 AI 味检查（按 `plugins/learning/HUMANIZE.md` 清单逐节扫描并重写），
是 L5 Surface 出稿前的最后一道工序。也可用于任意已有笔记/文档。

## 触发

```
/em learn humanize <topic-slug>     # 处理指定主题
/em learn humanize                  # 处理当前活跃主题
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| topic-slug | 否 | 缺省时取 `learning/state.md` 中第一个活跃主题 |

## 执行流程

### 步骤 1: 定位产物

处理 `learning/topics/<slug>/` 下的：
- `README.md`（必处理）
- `deep-dive.md` / `cheatsheet.md`（存在则处理）

### 步骤 2: 执行清单

载入 `plugins/learning/HUMANIZE.md`，逐节扫描七类模式：
夸大与宣传 / 肤浅分析尾缀 / 模糊归因 / AI 高频词 / 公式化结构 / 格式痕迹 / 填充与谄媚。

**不改的东西**：技术含义、代码示例、命令、参数表、坑表的结构、STYLE.md 要求的术语白话注释。

### 步骤 3: 重写与报告

- 直接 Edit 重写问题片段（保含义、保语气、代码不动）
- 输出改动清单表：`| 模式 | 位置 | 改法 |`
- 按 HUMANIZE.md 五维评分（直接性/节奏/信任读者/听感/精炼度，≥45/50 通过）
- 未达标 → 再过一轮；通过 → `_index.json` 该主题加 `"humanized": true`

## 验收

- grep 不到触发词表中的高频词（标志性地/彰显/此外/不仅…更…等）
- 出声读一遍不卡壳
- 代码与参数 diff 为零

## 相关文件

- `../HUMANIZE.md` — 模式清单与评分标准
- `../STYLE.md` — 术语与结构硬规则
- `../workflows/learn-lpr.md` — L5 流程挂载点
