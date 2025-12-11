"""Launcher shim for the introspection + hero-suite CLI."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC_PATH = REPO_ROOT / "src"
MODULE_PATH = SRC_PATH / "cli.py"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def _load_cli_module():
    spec = importlib.util.spec_from_file_location("introspection_cli", MODULE_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive guard
        raise ImportError(f"Unable to load CLI module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> None:
    module = _load_cli_module()
    module.main(argv)


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
