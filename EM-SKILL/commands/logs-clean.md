# 命令: /em logs-clean (日志滚动清理)

> S17-A 止血包新增。背景：嵌入式项目 logs/ 长期累积编译/串口日志，无清理机制（problem-log 2026-09-12 痛点 2）。

## 功能
按「保留最新 N 份」滚动清理 `<STATE_DIR>/logs/`（及可选 `cache/`），防止日志无限膨胀。

## 触发
```
/em logs-clean              # 预览 + 确认后清理（默认保留最新 10 份）
/em logs-clean -n 5         # 保留最新 5 份
/em logs-clean --dry-run    # 只预览不删除
/em logs-clean --all        # 连同 cache/（plugin-registry.json 等运行时缓存）一起清
```

## 规则

| 对象 | 规则 | 默认 |
|------|------|------|
| `logs/*.log`（serial_*.log / build_*.log 等） | 按 mtime 排序，保留最新 N 份，其余删除 | N=10 |
| `logs/` 子目录 | 不递归处理，仅提示 | — |
| `cache/`（仅 `--all`） | 整目录删除（plugin-registry.json 会由 loader 自动重建） | 不动 |

**保护约束**：
- ❌ 不删 `logs/` 目录本身
- ❌ 不删非日志文件（只匹配 `*.log` / `*.txt`）；拿不准的列出来问
- ✅ HVR / problem-log 中被引用的日志（grep 到路径）**默认保留**并在预览中标注「被引用」
- ✅ 删除前列出完整清单等用户确认（`--dry-run` 永远只预览）

## 执行流程

1. **【状态目录】** `get_state_dir()` → `<STATE_DIR>`；`logs/` 不存在 → 提示「无日志可清理」并退出
2. **【扫描】** 列出 `logs/*.log` + mtime + 大小，按 mtime 倒序
3. **【引用检查】** 对将删除的文件，在 `checkpoints/` 与 `problem-log.md` 中 grep 文件名；命中的移回保留列表并标注
4. **【预览】** 输出：

   ```
   🧹 logs 清理预览（保留最新 10 份）

   ✅ 保留（10）:
     serial_s16_20260921_141022.log   12 KB  2026-09-21
     ...
   🗑️ 删除（23）:
     serial_s5_20260419_141722.log     45 KB  2026-04-19
     ...
   ⚠️ 被引用已回保（2）:
     serial_s15_...log  ← HVR-S15-002.md 引用

   合计释放: ~1.2 MB
   确认删除？[y/n]
   ```

5. **【执行】** 用户确认后删除；输出实际释放统计
6. **【记录】** 会话日志记一行（清理 N 份 / 释放 X）；不写 problem-log（属例行维护）

## 边界与降级

| 场景 | 行为 |
|------|------|
| 日志总数 ≤ N | 提示「无需清理」退出 |
| 用户全拒绝 | 不做任何删除 |
| 非 EM 项目（无 STATE_DIR） | 报错退出 |
| cache/ 清理后 | 下次任一插件命令自动重建（loader mtime 缓存机制） |

## 相关文件
- `commands/arch.md` — 文件归档（问题日志/规格单走那边）
- `docs/LIFECYCLE.md` — 生命周期总表（S17-D）
- EM-SKILL `.gitignore` — `.em/logs/*.log` / `.emv2/logs/*.log` 已忽略，本命令处理的是磁盘占用
