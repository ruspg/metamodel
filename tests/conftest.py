from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Canonical source paths — used by all test modules
METAMODEL_PATH = ROOT / "model" / "metamodel.yaml"
RELATION_CATALOG_PATH = ROOT / "model" / "relation_catalog.yaml"
