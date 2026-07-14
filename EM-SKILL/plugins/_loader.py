"""
EM-SKILL Plugin Loader  —  S15-A
================================

Lazy-load plugin commands via manifest + cache.

设计目标（S15 milestones.md）：
1. 启动时一次性读所有 PLUGIN.md → 构建 {prefix → cmd → file} 映射
2. mtime 校验的缓存（<STATE_DIR>/cache/plugin-registry.json）
3. 命令执行时按缓存路由（O(1) 查表）
4. 支持两种 `provides.commands` 格式：
   - 对象形式（PLUGIN-SPEC v1.0）：{name, file, summary}
   - 简单列表形式（learning v0）："learn-new  # comment"

CLI:
    python _loader.py --build               # 强制重建 + 缓存
    python _loader.py --query learn new     # → plugins/learning/commands/learn-new.md
    python _loader.py --list                # 列出所有命令
    python _loader.py --list embedded       # 列出嵌入式插件命令

退出码：
    0  成功
    1  --query 找不到
    2  参数错误
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Force UTF-8 on Windows consoles (avoid GBK encoding errors for CJK output)
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


CACHE_VERSION = 1
CACHE_FILENAME = "plugin-registry.json"


# ============================================================================
# Path resolution
# ============================================================================

def find_state_dir(start: Path) -> Optional[Path]:
    """Locate `.em/` (preferred) or `.emv2/` (fallback) from `start` upward."""
    current = start.resolve()
    for p in [current] + list(current.parents):
        for d in (".em", ".emv2"):
            candidate = p / d
            if candidate.is_dir():
                return candidate
    return None


def default_cache_dir() -> Path:
    """Default cache directory: <STATE_DIR>/cache/ or fallback to skill/.cache/."""
    state_dir = find_state_dir(Path.cwd())
    if state_dir:
        return state_dir / "cache"
    # Fallback: alongside the skill (so the loader works even outside a project)
    return Path(__file__).resolve().parent.parent / ".cache"


# ============================================================================
# Loader
# ============================================================================

class PluginLoader:
    """Build, cache, and query plugin command registry."""

    def __init__(self, plugins_dir: Path, cache_dir: Path):
        self.plugins_dir = Path(plugins_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / CACHE_FILENAME

    # -------- public API --------

    def build_registry(self, force: bool = False) -> dict:
        """Return registry dict. Use cache unless invalid or `force=True`."""
        if not force and self._cache_is_valid():
            return self._load_cache()
        registry = self._scan_plugins()
        self._write_cache(registry)
        return registry

    def query(self, prefix: str, command: str) -> Optional[str]:
        """Return absolute file path for /em <prefix> <command>, or None.

        Backward-compat: treats `prefix` as plugin name (registry key).
        For user-style invocation ("learn new"), use :meth:`resolve`.
        """
        reg = self.build_registry()
        info = reg.get("registry", {}).get(prefix, {})
        if isinstance(info, dict):
            return info.get("commands", {}).get(command)
        return info.get(command)  # legacy fallback

    def resolve(self, invocation: str) -> Optional[str]:
        """Resolve a user-facing invocation (e.g. ``"learn new"`` or ``"initem"``).

        Resolution rules (in order):
        1. Direct match: ``invocation`` matches a registered command name in any plugin.
        2. Prefix split: first whitespace-separated token equals a plugin's ``prefix``,
           and ``<prefix>-<rest>`` exists as a command in that plugin.
        """
        reg = self.build_registry()
        plugins = reg.get("registry", {})
        tokens = invocation.strip().split()
        if not tokens:
            return None

        # Rule 1: direct command name match across all plugins
        if len(tokens) == 1:
            for _plugin, info in plugins.items():
                cmds = info.get("commands", {}) if isinstance(info, dict) else {}
                if tokens[0] in cmds:
                    return cmds[tokens[0]]

        # Rule 2: prefix + suffix (e.g. "learn new" → "learn-new")
        if len(tokens) >= 2:
            prefix = tokens[0]
            suffix = "-".join(tokens[1:])
            for _plugin, info in plugins.items():
                if not isinstance(info, dict) or "prefix" not in info:
                    continue
                if info["prefix"] != prefix:
                    continue
                cmds = info.get("commands", {})
                candidate = f"{prefix}-{suffix}"
                if candidate in cmds:
                    return cmds[candidate]
                # also try bare suffix if declared with no prefix in name
                if suffix in cmds:
                    return cmds[suffix]
        return None

    def list_commands(self, prefix: Optional[str] = None) -> list[dict]:
        """Return list of {plugin, command, file} dicts; optionally filtered.

        ``prefix`` here means *plugin name* (e.g. ``embedded`` / ``learning``),
        not the user-facing invocation prefix.
        """
        reg = self.build_registry()
        result: list[dict] = []
        for plugin_name, info in reg.get("registry", {}).items():
            if prefix and plugin_name != prefix:
                continue
            cmds = info.get("commands", {}) if isinstance(info, dict) else {}
            for cmd_name, file_path in sorted(cmds.items()):
                result.append({
                    "plugin": plugin_name,
                    "command": cmd_name,
                    "file": file_path,
                })
        return result

    # -------- internals --------

    def _cache_is_valid(self) -> bool:
        """True iff cache exists, version matches, and every PLUGIN.md mtime matches."""
        if not self.cache_file.exists():
            return False
        try:
            cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False
        if cache.get("version") != CACHE_VERSION:
            return False
        for plugin in cache.get("plugins", []):
            manifest_path = self.plugins_dir / plugin["name"] / "PLUGIN.md"
            if not manifest_path.exists():
                return False
            current_mtime = manifest_path.stat().st_mtime
            cached_mtime = plugin.get("mtime", 0.0)
            # mtime precision can vary by FS; allow tiny epsilon
            if abs(current_mtime - cached_mtime) > 0.01:
                return False
        return True

    def _scan_plugins(self) -> dict:
        """Scan plugins/*/PLUGIN.md, return fresh registry dict."""
        registry: dict = {
            "version": CACHE_VERSION,
            "built_at": datetime.now().isoformat(),
            "plugins_dir": str(self.plugins_dir),
            "plugins": [],          # [{name, version, description, mtime, manifest}]
            "registry": {},         # {plugin_name: {cmd_name: file_path}}
        }
        if not self.plugins_dir.is_dir():
            return registry
        for plugin_dir in sorted(self.plugins_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            manifest = plugin_dir / "PLUGIN.md"
            if not manifest.is_file():
                continue
            entry = self._parse_manifest(plugin_dir, manifest)
            if entry is None:
                continue
            registry["plugins"].append(entry["meta"])
            registry["registry"][entry["meta"]["name"]] = entry["info"]
        return registry

    def _parse_manifest(self, plugin_dir: Path, manifest: Path) -> Optional[dict]:
        """Parse one PLUGIN.md frontmatter. Return {meta, commands} or None on failure."""
        try:
            text = manifest.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"WARN: cannot read {manifest}: {exc}", file=sys.stderr)
            return None

        # Extract frontmatter between first pair of `---`
        if not text.startswith("---\n"):
            print(f"WARN: {manifest} missing YAML frontmatter", file=sys.stderr)
            return None
        end = text.find("\n---\n", 4)
        if end == -1:
            print(f"WARN: {manifest} frontmatter not closed", file=sys.stderr)
            return None
        try:
            fm = yaml.safe_load(text[4:end])
        except yaml.YAMLError as exc:
            print(f"WARN: {manifest} YAML parse error: {exc}", file=sys.stderr)
            return None
        if not isinstance(fm, dict):
            return None

        plugin_name = fm.get("plugin") or plugin_dir.name
        prefix = fm.get("prefix", "")  # S15-A: user-facing namespace prefix
        commands_list = (fm.get("provides") or {}).get("commands") or []
        commands_map: dict[str, str] = {}
        for cmd in commands_list:
            if isinstance(cmd, str):
                # Simple form: "learn-new  # comment" → name = "learn-new"
                name = cmd.split("#", 1)[0].strip()
                if not name:
                    continue
                file_path = plugin_dir / "commands" / f"{name}.md"
                if not file_path.exists():
                    print(f"WARN: {manifest}: command '{name}' declared but "
                          f"{file_path.name} missing", file=sys.stderr)
                    continue
                commands_map[name] = str(file_path.resolve())
            elif isinstance(cmd, dict):
                # Object form: {name, file, summary, ...}
                name = cmd.get("name")
                file_rel = cmd.get("file")
                if not name or not file_rel:
                    continue
                file_path = plugin_dir / file_rel
                if not file_path.exists():
                    print(f"WARN: {manifest}: command '{name}' declared but "
                          f"{file_path} missing", file=sys.stderr)
                    continue
                commands_map[name] = str(file_path.resolve())
            else:
                print(f"WARN: {manifest}: unknown command entry type {type(cmd).__name__}",
                      file=sys.stderr)

        return {
            "meta": {
                "name": plugin_name,
                "version": str(fm.get("version", "")),
                "description": str(fm.get("description", "")),
                "mtime": manifest.stat().st_mtime,
                "manifest": str(manifest),
            },
            "info": {
                "prefix": prefix,
                "commands": commands_map,
            },
        }

    def _write_cache(self, registry: dict) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load_cache(self) -> dict:
        return json.loads(self.cache_file.read_text(encoding="utf-8"))


# ============================================================================
# CLI
# ============================================================================

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="em-plugin-loader",
        description="EM-SKILL plugin registry builder & query tool (S15-A).",
    )
    p.add_argument("--build", action="store_true",
                   help="Force rebuild registry (ignore cache).")
    p.add_argument("--query", nargs=2, metavar=("PREFIX", "COMMAND"),
                   help="Return file path for plugin/<PREFIX> command <COMMAND>.")
    p.add_argument("--resolve", metavar="INVOCATION",
                   help="Resolve user-style invocation, e.g. 'learn new' or 'initem'.")
    p.add_argument("--list", nargs="?", const="*", metavar="PREFIX",
                   help="List commands (optionally filtered by plugin name).")
    p.add_argument("--plugins-dir", type=Path, default=None,
                   help="Override plugins directory (default: <skill>/plugins).")
    p.add_argument("--cache-dir", type=Path, default=None,
                   help="Override cache directory (default: <STATE_DIR>/cache).")
    p.add_argument("--json", action="store_true",
                   help="Output as JSON (for --list and --query).")
    p.add_argument("--show-cache-path", action="store_true",
                   help="Print cache file path and exit.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    skill_root = Path(__file__).resolve().parent.parent
    plugins_dir = args.plugins_dir or (skill_root / "plugins")
    cache_dir = args.cache_dir or default_cache_dir()
    loader = PluginLoader(plugins_dir, cache_dir)

    if args.show_cache_path:
        print(loader.cache_file)
        return 0

    if args.query:
        prefix, command = args.query
        result = loader.query(prefix, command)
        if args.json:
            print(json.dumps({"found": result is not None, "file": result},
                             ensure_ascii=False))
        elif result:
            print(result)
        else:
            print(f"ERROR: command not found: /em {prefix} {command}", file=sys.stderr)
            return 1
        return 0

    if args.resolve:
        result = loader.resolve(args.resolve)
        if args.json:
            print(json.dumps({"found": result is not None, "invocation": args.resolve, "file": result},
                             ensure_ascii=False))
        elif result:
            print(result)
        else:
            print(f"ERROR: cannot resolve: /em {args.resolve}", file=sys.stderr)
            return 1
        return 0

    if args.list is not None:
        prefix = None if args.list == "*" else args.list
        items = loader.list_commands(prefix)
        if args.json:
            print(json.dumps(items, ensure_ascii=False, indent=2))
        else:
            if not items:
                print(f"(no commands found for prefix={prefix!r})")
            for item in items:
                print(f"{item['plugin']}.{item['command']}\t{item['file']}")
        return 0

    # Default: build registry + print summary
    reg = loader.build_registry(force=args.build)
    plugin_count = len(reg["plugins"])
    cmd_total = sum(
        len(info.get("commands", {}))
        for info in reg["registry"].values()
        if isinstance(info, dict)
    )
    if args.json:
        print(json.dumps({
            "version": reg["version"],
            "built_at": reg["built_at"],
            "plugin_count": plugin_count,
            "command_total": cmd_total,
            "plugins": reg["plugins"],
            "cache_file": str(loader.cache_file),
        }, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] Registry built: {plugin_count} plugin(s), {cmd_total} command(s)")
        for plugin in reg["plugins"]:
            info = reg["registry"].get(plugin["name"], {})
            cmd_count = len(info.get("commands", {})) if isinstance(info, dict) else 0
            user_prefix = info.get("prefix", "") if isinstance(info, dict) else ""
            prefix_str = f"/em {user_prefix} ..." if user_prefix else "/em <cmd>"
            print(f"  - {plugin['name']} v{plugin['version'] or '?'}  "
                  f"({cmd_count} commands, prefix={prefix_str})  — {plugin['description']}")
        print(f"  cache: {loader.cache_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())