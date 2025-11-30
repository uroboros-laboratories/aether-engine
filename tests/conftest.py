"""Test configuration for importing code under src/.

Adds the src directory to sys.path so tests can import pillar modules directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repository root is on sys.path so imports like `import src.umx` work
# regardless of where pytest is invoked from. We also add the `src/` directory
# itself so packages exposed at the module root (e.g., `core`, `config`) can be
# imported without the `src.` prefix.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_ROOT):
    str_path = str(path)
    if str_path not in sys.path:
        sys.path.insert(0, str_path)
