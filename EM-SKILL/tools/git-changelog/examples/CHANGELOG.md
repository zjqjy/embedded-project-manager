# Changelog

> 项目变更日志 | 由 `tools/git-changelog/changelog_gen.py` 自动生成
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
> commit 遵循 EM 自定义规范 `[Sx] type: message`。

## [Unreleased]

### Added
- [S11] 计划：嵌入式项目智能识别优化

## [2026-06 (S10-D)] - 2026-06-02

### Added
- [S10-D] git workflow integration with propose-commit UX
- [S10-D] changelog_gen.py tool (zero external dependencies)
- [S10-D] auto tag on main-step archive (v0.10.0 / em-s10-final)

### Changed
- [S10-D] update initem.md with git permissions section
- [S10-D] integrate changelog generation into arch flow

### Documentation
- [S10-D] add git-changelog tool README and examples
- [S10-D] document propose-commit UX in verify.md

### Fixed
- [S10-D] deny `git push` in permissions.deny to enforce manual push

## [2026-05 (S10-C)] - 2026-05-28

### Added
- [S10-C] `em migrate` command for `.emv2/` → `.em/` migration
- [S10-C] tool index in SKILL.md embedded section

### Changed
- [S10-C] keep `.emv2/` symlink during coexistence period

## [2026-05 (S10-B)] - 2026-05-20

### Added
- [S10-B] dual-track state directory (`.em/` preferred, `.emv2/` fallback)
- [S10-B] `get_state_dir()` helper for dynamic path resolution

### Changed
- [S10-B] replace hardcoded `.emv2` references with `<STATE_DIR>` placeholder

## [2026-05 (S10-A)] - 2026-05-12

### Added
- [S10-A] YAML frontmatter in SKILL.md (name / description / version)
- [S10-A] tool index section pointing to `EM-SKILL/tools/`

### Documentation
- [S10-A] reorganize SKILL.md: 快速开始 → 通用命令 → 项目类型 → 嵌入式场景 → 详细命令
