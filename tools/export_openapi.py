#!/usr/bin/env python3
import json, sys
from pathlib import Path

# ensure project root is on sys.path so "import backend" works
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.main import app  # noqa: E402

print(json.dumps(app.openapi()))
