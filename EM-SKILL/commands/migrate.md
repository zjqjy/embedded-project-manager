# 命令: /em migrate (迁移 .emv2/ → .em/)

## 功能
将存量项目的 `.emv2/` 状态目录迁移到新的 `.em/` 目录，保留旧目录作为回退。

## 触发
```
/em migrate [项目路径]
```

## 参数
- **项目路径**（可选）：项目根目录路径
  - 不带路径时：使用当前项目目录（`.`）
  - 带路径时：使用指定目录的绝对/相对路径

## 设计动机（S10-C 决策）

- `.emv2/` → `.em/` 目录重命名（S10-B 通用化决策）
- **非强制迁移**：旧项目按需执行，EM 启动时仅提示而不自动执行
- **保留回退语义**：迁移完成后 `.emv2/` 仍存在，作为软链接或独立副本
- **零配置升级**：迁移期间 EM 启动逻辑自动优先读 `.em/`，回退 `.emv2/`

## 执行流程

### 1. 状态目录预检

```python
def migrate_precheck(project_root: str) -> dict:
    """
    迁移前预检：判定是否需要迁移、是否需要覆盖确认。
    """
    em_dir   = os.path.join(project_root, '.em')
    emv2_dir = os.path.join(project_root, '.emv2')

    em_exists   = os.path.isdir(em_dir)
    emv2_exists = os.path.isdir(emv2_dir)

    return {
        'em_exists':   em_exists,
        'emv2_exists': emv2_exists,
        'action': (
            'no-op'      if not emv2_exists else
            'overwrite?' if em_exists and emv2_exists else
            'migrate'    if emv2_exists and not em_exists else
            'error'
        )
    }
```

### 2. 状态机分支

| 预检结果 | 行为 | 用户交互 |
|----------|------|----------|
| `.emv2/` 不存在 | 提示"无需迁移"并退出 | 无 |
| `.emv2/` 存在，`.em/` 不存在 | 直接进入迁移流程 | 打印「开始迁移」 |
| `.emv2/` 和 `.em/` 都存在 | 提示"目标已存在，是否强制覆盖？" | 用户选择 `[y/N]`（默认否） |
| 用户拒绝覆盖 | 退出迁移，保留现状 | 无 |
| `.emv2/` 不存在但 `.em/` 存在 | 提示"已是新格式，无需迁移" | 无 |

### 3. 迁移步骤（核心流程）

```python
def run_migration(project_root: str, force: bool = False) -> dict:
    """
    执行迁移：.emv2/ → .em/，创建 .emv2 软链接或保留为副本。

    返回迁移报告 dict。
    """
    import shutil
    import os

    em_dir   = os.path.join(project_root, '.em')
    emv2_dir = os.path.join(project_root, '.emv2')
    emv2_lnk = os.path.join(project_root, '.emv2')   # 注意：路径同 emv2_dir，区别是文件还是目录

    report = {
        'copied_files': 0,
        'copied_dirs':  0,
        'symlink_mode':  None,    # 'symlink' | 'copy' | 'kept'
        'emv2_final':    None,    # 'symlink' | 'dir-copy' | 'removed'
        'errors':        [],
    }

    try:
        # Step 1: 创建 .em/ 目录
        if not os.path.isdir(em_dir):
            os.makedirs(em_dir)

        # Step 2: 递归复制 .emv2/ → .em/
        file_count, dir_count = _copy_tree(emv2_dir, em_dir)
        report['copied_files'] = file_count
        report['copied_dirs']  = dir_count

        # Step 3: 处理 .emv2/ 的最终形态
        # 决策矩阵：
        #   3a. 软链接成功（Unix 或 Windows 管理员权限）→ 删目录、建软链
        #   3b. 软链接失败（Windows 无权限）           → 保留原 .emv2/ 目录作为独立副本
        #   3c. 用户显式 --no-symlink                 → 同 3b
        if _try_create_symlink(em_dir, emv2_lnk):
            # 成功建软链：先删旧的 .emv2/ 目录
            if os.path.isdir(emv2_dir) and not os.path.islink(emv2_dir):
                shutil.rmtree(emv2_dir)
            os.symlink('.em', emv2_lnk)
            report['symlink_mode'] = 'symlink'
            report['emv2_final']   = 'symlink'
        else:
            # 软链失败：保留 .emv2/ 作为独立副本
            report['symlink_mode'] = 'copy'
            report['emv2_final']   = 'dir-copy'

    except PermissionError as e:
        report['errors'].append({
            'type': 'permission',
            'msg':  f'权限不足：{e}。请以管理员/root 权限运行后重试。',
        })
        _rollback(em_dir)
    except OSError as e:
        if 'No space left' in str(e) or e.errno == 28:
            report['errors'].append({
                'type': 'disk-full',
                'msg':  f'磁盘空间不足：{e}。已回滚迁移操作。',
            })
            _rollback(em_dir)
        else:
            raise
    else:
        report['success'] = True

    return report


def _copy_tree(src: str, dst: str) -> tuple[int, int]:
    """递归复制 src/ 下所有内容到 dst/，返回 (文件数, 目录数)。"""
    import shutil
    file_count = 0
    dir_count  = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel) if rel != '.' else dst
        os.makedirs(target_dir, exist_ok=True)
        dir_count += 1
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_dir, f)
            shutil.copy2(src_file, dst_file)   # 保留元数据
            file_count += 1
    return file_count, dir_count


def _try_create_symlink(target: str, link_path: str) -> bool:
    """尝试创建软链接，失败返回 False（不抛异常）。"""
    try:
        # Windows 上 os.symlink 需要特权或开发者模式
        if os.path.exists(link_path):
            os.remove(link_path) if not os.path.isdir(link_path) else None
        os.symlink(target, link_path)
        return True
    except (OSError, NotImplementedError):
        return False


def _rollback(em_dir: str) -> None:
    """迁移失败时回滚：删除已部分创建的 .em/。"""
    import shutil
    if os.path.isdir(em_dir):
        shutil.rmtree(em_dir, ignore_errors=True)
```

### 4. 迁移报告

迁移完成后，AI 输出以下报告：

```
═══════════════════════════════════════════════════════════
  EM 迁移报告
═══════════════════════════════════════════════════════════

源目录:  <项目根>/.emv2/
目标目录: <项目根>/.em/

复制统计:
  - 文件数:  42
  - 子目录数: 7
  - 总大小:  128 KB

软链接状态:
  - 模式: symlink    # 或 copy（Windows 无权限时）
  - .emv2 → .em     # 指向关系

保留情况:
  - .emv2/ 保留为: 软链接    # 或「独立副本（Windows 回退模式）」
  - EM 启动仍可读取 .emv2/ 作为回退

═══════════════════════════════════════════════════════════
✅ 迁移成功

后续建议:
  1. 验证项目可正常恢复: /em rec
  2. 1-2 个版本后（v2.1+）可手动删除 .emv2/ 软链接/目录
  3. 详细使用场景见: templates/em-migration.md
═══════════════════════════════════════════════════════════
```

### 5. 错误处理矩阵

| 错误类型 | 检测方式 | 处理策略 |
|----------|----------|----------|
| 权限不足 | `PermissionError` | 提示用管理员/root 权限重试，保留原 `.emv2/` |
| 磁盘空间不足 | `OSError.errno == 28` | 回滚已复制文件（删除 `.em/`），原 `.emv2/` 不动 |
| 软链接创建失败 | `os.symlink` 抛 `OSError` | 回退到「保留 `.emv2/` 独立副本」模式 |
| 软链接创建失败（Windows 常见）| `NotImplementedError` / `OSError: symbolic link privilege` | 同上，回退副本模式 |
| 目标 `.em/` 已存在且用户拒绝覆盖 | 用户输入 `N` | 退出迁移，保留现状 |
| 源 `.emv2/` 不存在 | 预检阶段 | 提示"无需迁移"并退出 |
| 源 `.emv2/` 实际是文件而非目录 | `os.path.isfile(emv2_dir)` | 错误：路径冲突，提示用户检查 |

## 完整伪代码（端到端）

```python
def em_migrate(args: list[str]) -> None:
    """
    /em migrate [项目路径]
    """
    project_root = args[0] if args else '.'
    project_root = os.path.abspath(project_root)

    print(f"[EM] 目标项目: {project_root}")

    # 1. 预检
    pre = migrate_precheck(project_root)
    if pre['action'] == 'no-op':
        print("[EM] 未检测到 .emv2/，无需迁移。")
        print("     如需初始化新项目，请使用 /em init <name>")
        return

    if pre['action'] == 'overwrite?':
        print(f"[EM] 检测到 .em/ 已存在，强制迁移将覆盖其内容。")
        ans = input("     是否强制覆盖？[y/N]: ").strip().lower()
        if ans != 'y':
            print("[EM] 已取消迁移。")
            return
        force = True
    else:
        force = False

    # 2. 执行迁移
    print("[EM] 开始迁移 .emv2/ → .em/ ...")
    report = run_migration(project_root, force=force)

    # 3. 输出报告
    if report.get('success'):
        print_migration_report(report)
    else:
        for err in report['errors']:
            print(f"[EM] 错误 ({err['type']}): {err['msg']}")
        sys.exit(1)
```

## 状态机图

```
                    ┌────────────────┐
                    │  /em migrate   │
                    └────────┬───────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ 检查 .emv2/ 是否存在 │
                  └──────┬───────────────┘
                         │
          ┌──────────────┼──────────────┐
          │ 不存在        │ 存在          │
          ▼              ▼              │
   ┌─────────────┐  ┌──────────────┐    │
   │ 提示"无需迁移"│  │ 检查 .em/   │    │
   │ 退出         │  └──────┬───────┘    │
   └─────────────┘         │            │
                  ┌────────┼────────┐   │
                  │ 不存在  │ 存在   │   │
                  ▼        ▼        │   │
           ┌──────────┐ ┌─────────────┐
           │ 直接迁移  │ │ 询问覆盖确认│
           └────┬─────┘ └──────┬──────┘
                │              │
                │         ┌────┴─────┐
                │         │ 用户决定 │
                │         └────┬─────┘
                │       ┌─────┴──────┐
                │       │ 拒绝       │ 确认
                │       ▼            ▼
                │  ┌──────────┐ ┌──────────┐
                │  │ 退出      │ │ 强制覆盖 │
                │  └──────────┘ └────┬─────┘
                │                    │
                ▼                    ▼
           ┌────────────────────────────┐
           │ 1. 创建 .em/              │
           │ 2. 递归复制 .emv2/ → .em/ │
           │ 3. 处理 .emv2/ 最终形态   │
           │    a) 软链接成功 → 删目录建链 │
           │    b) 软链接失败 → 保留副本  │
           └────────┬───────────────────┘
                    │
                    ▼
           ┌────────────────┐
           │ 输出迁移报告    │
           │ 提示后续建议    │
           └────────────────┘
```

## 与其他命令的关系

| 命令 | 关系 |
|------|------|
| `/em rec` | 迁移完成后执行，验证 `.em/` 可正常读取 |
| `/em init` | 迁移不涉及 init；init 用于从零创建项目 |
| `/em si` | 迁移不涉及 si；si 用于存量项目审计并建 `.em/` 或 `.emv2/` |
| `/em stat` | 迁移后可执行，确认新状态目录生效 |

## 相关文件
- commands/init.md - 智能识别 + `get_state_dir()` 函数
- commands/rec.md - 状态目录检测逻辑（含迁移提示）
- templates/em-migration.md - 嵌入式迁移使用场景文档
- SKILL.md - 主入口（含工具索引章节）
