"""CLI shim for running ``python -m dpi_quantum`` without PYTHONPATH tweaks.

This keeps the developer workflow simple by importing the CLI implementation
from ``src/dpi_quantum.py`` and executing its ``main`` function. It also
ensures the ``src`` directory is on ``sys.path`` so the underlying module can
resolve its dependencies.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC_PATH = REPO_ROOT / "src"
MODULE_PATH = SRC_PATH / "dpi_quantum.py"

# Ensure src/ is available for downstream imports (config, operator_service, etc.).
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def _load_cli_module():
    spec = importlib.util.spec_from_file_location("dpi_quantum_cli", MODULE_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive guard
        raise ImportError(f"unable to load cli module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> None:
    module = _load_cli_module()
    module.main(argv)


if __name__ == "__main__":  # pragma: no cover - CLI execution
    main()
