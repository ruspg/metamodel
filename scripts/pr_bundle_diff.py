#!/usr/bin/env python3
"""Generate a bundle from current working tree and diff against baseline.

Outputs markdown to stdout. Used by CI to post PR comments and locally
via `make diff`.

Exit codes:
  0 — diff computed (identical or changed)
  1 — generation or comparison failed
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.wave1.bundle_diff import compute_bundle_diff, format_bundle_diff_markdown
from tools.wave1.loader import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle


def _find_latest_baseline(candidates_dir: Path) -> Path | None:
    """Find the latest bundle directory by name (lexicographic sort)."""
    if not candidates_dir.is_dir():
        return None
    bundles = sorted(
        [d for d in candidates_dir.iterdir() if d.is_dir() and (d / "artifacts").is_dir()],
        key=lambda p: p.name,
    )
    return bundles[-1] if bundles else None


def main() -> int:
    metamodel_path = ROOT / "model" / "metamodel.yaml"
    relation_catalog_path = ROOT / "model" / "relation_catalog.yaml"
    candidates_dir = ROOT / "generated" / "atlas_candidates"

    # Find baseline
    baseline = _find_latest_baseline(candidates_dir)
    if baseline is None:
        print("## Bundle diff\n\nNo baseline bundle found in `generated/atlas_candidates/`. First run.")
        return 0

    # Generate bundle from current working tree
    try:
        ontology = load_ontology(
            metamodel_path,
            relation_catalog_path=relation_catalog_path,
        )
        projection = build_projection_model(ontology, profile="atlas_mvp")

        with tempfile.TemporaryDirectory(prefix="bundle_diff_") as tmp:
            result = generate_atlas_bundle(projection, Path(tmp))
            head_dir = Path(result.bundle_root)
            diff = compute_bundle_diff(baseline, head_dir)

    except Exception as exc:
        print(f"## Bundle diff\n\nFailed to generate bundle: {exc}", file=sys.stderr)
        return 1

    print(format_bundle_diff_markdown(diff))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
