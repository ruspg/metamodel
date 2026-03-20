"""Semantic diff between two atlas bundles.

Compares type_catalog.json and relation_catalog.json from two bundle
directories and produces a structured delta with markdown formatting.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BundleDiff:
    added_kinds: tuple[str, ...]
    removed_kinds: tuple[str, ...]
    added_relations: tuple[str, ...]
    removed_relations: tuple[str, ...]
    artifact_sizes: dict[str, tuple[int, int]]  # {name: (base_bytes, head_bytes)}
    base_kind_count: int
    head_kind_count: int
    base_relation_count: int
    head_relation_count: int

    @property
    def is_identical(self) -> bool:
        return (
            not self.added_kinds
            and not self.removed_kinds
            and not self.added_relations
            and not self.removed_relations
        )


def _load_ids(catalog_path: Path, key: str) -> set[str]:
    if not catalog_path.exists():
        return set()
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    return {item["id"] for item in data.get(key, [])}


def _count_items(catalog_path: Path, key: str) -> int:
    if not catalog_path.exists():
        return 0
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    return len(data.get(key, []))


def _artifact_sizes(artifacts_dir: Path) -> dict[str, int]:
    sizes: dict[str, int] = {}
    if artifacts_dir.is_dir():
        for f in sorted(artifacts_dir.iterdir()):
            if f.is_file():
                sizes[f.name] = f.stat().st_size
    return sizes


def compute_bundle_diff(base_dir: Path, head_dir: Path) -> BundleDiff:
    """Compare two bundle directories and return semantic diff."""
    base_artifacts = base_dir / "artifacts"
    head_artifacts = head_dir / "artifacts"

    base_kinds = _load_ids(base_artifacts / "type_catalog.json", "kinds")
    head_kinds = _load_ids(head_artifacts / "type_catalog.json", "kinds")

    base_rels = _load_ids(base_artifacts / "relation_catalog.json", "relations")
    head_rels = _load_ids(head_artifacts / "relation_catalog.json", "relations")

    base_sizes = _artifact_sizes(base_artifacts)
    head_sizes = _artifact_sizes(head_artifacts)
    all_names = sorted(set(base_sizes) | set(head_sizes))
    artifact_sizes = {
        name: (base_sizes.get(name, 0), head_sizes.get(name, 0))
        for name in all_names
    }

    return BundleDiff(
        added_kinds=tuple(sorted(head_kinds - base_kinds)),
        removed_kinds=tuple(sorted(base_kinds - head_kinds)),
        added_relations=tuple(sorted(head_rels - base_rels)),
        removed_relations=tuple(sorted(base_rels - head_rels)),
        artifact_sizes=artifact_sizes,
        base_kind_count=_count_items(base_artifacts / "type_catalog.json", "kinds"),
        head_kind_count=_count_items(head_artifacts / "type_catalog.json", "kinds"),
        base_relation_count=_count_items(base_artifacts / "relation_catalog.json", "relations"),
        head_relation_count=_count_items(head_artifacts / "relation_catalog.json", "relations"),
    )


def _delta(base: int, head: int) -> str:
    d = head - base
    if d == 0:
        return ""
    return f" ({'+' if d > 0 else ''}{d})"


def format_bundle_diff_markdown(diff: BundleDiff) -> str:
    """Format BundleDiff as a markdown summary for PR comments."""
    lines: list[str] = []
    lines.append("## Bundle diff")
    lines.append("")

    if diff.is_identical:
        lines.append("No metamodel changes detected. Bundle is identical to baseline.")
        return "\n".join(lines)

    # Kinds
    lines.append(
        f"### Entity kinds: {diff.base_kind_count} -> "
        f"{diff.head_kind_count}{_delta(diff.base_kind_count, diff.head_kind_count)}"
    )
    lines.append("")
    if diff.added_kinds:
        for k in diff.added_kinds:
            lines.append(f"- + `{k}`")
    if diff.removed_kinds:
        for k in diff.removed_kinds:
            lines.append(f"- - `{k}`")
    if not diff.added_kinds and not diff.removed_kinds:
        lines.append("No changes.")
    lines.append("")

    # Relations
    lines.append(
        f"### Relations: {diff.base_relation_count} -> "
        f"{diff.head_relation_count}{_delta(diff.base_relation_count, diff.head_relation_count)}"
    )
    lines.append("")
    if diff.added_relations:
        for r in diff.added_relations:
            lines.append(f"- + `{r}`")
    if diff.removed_relations:
        for r in diff.removed_relations:
            lines.append(f"- - `{r}`")
    if not diff.added_relations and not diff.removed_relations:
        lines.append("No changes.")
    lines.append("")

    # Artifact sizes
    lines.append("### Artifact sizes")
    lines.append("")
    lines.append("| Artifact | Base | Head | Delta |")
    lines.append("|----------|------|------|-------|")
    for name, (base_sz, head_sz) in diff.artifact_sizes.items():
        delta = head_sz - base_sz
        delta_str = f"{'+' if delta > 0 else ''}{delta}" if delta != 0 else "="
        lines.append(f"| `{name}` | {base_sz:,} | {head_sz:,} | {delta_str} |")
    lines.append("")

    return "\n".join(lines)
