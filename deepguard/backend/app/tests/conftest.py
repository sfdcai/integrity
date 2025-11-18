"""Test configuration for DeepGuard backend tests."""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is available for `import app` style imports during tests
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
