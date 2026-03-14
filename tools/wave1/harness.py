"""Wave 1 validation harness orchestrating loader + validators + lint."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

from .lint import LintMessage, LintResult, lint_ontology
from .loader import OntologyLoadError, load_ontology
from .model import NormalizedOntology
from .relation_catalog_validator import validate_relation_catalog
from .validation_types import ValidationMessage, ValidationResult
from .validator import validate_ontology


@dataclass(frozen=True)
class HarnessStageResult:
    name: str
    errors: Tuple[str, ...]
    warnings: Tuple[str, ...]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)


@dataclass(frozen=True)
class Wave1HarnessResult:
    success: bool
    stages: Tuple[HarnessStageResult, ...]

    @property
    def error_count(self) -> int:
        return sum(stage.error_count for stage in self.stages)

    @property
    def warning_count(self) -> int:
        return sum(stage.warning_count for stage in self.stages)


def run_wave1_validation_harness(
    ontology_path: Path | str,
    *,
    relation_catalog_path: Path | str | None = None,
) -> Wave1HarnessResult:
    """Load ontology from paths and run full Wave 1 validation stack."""

    try:
        ontology = load_ontology(ontology_path, relation_catalog_path=relation_catalog_path)
    except OntologyLoadError as exc:
        stage = HarnessStageResult(name="load", errors=(str(exc),), warnings=())
        return Wave1HarnessResult(success=False, stages=(stage,))

    return run_wave1_validation_harness_on_model(ontology)


def run_wave1_validation_harness_on_model(ontology: NormalizedOntology) -> Wave1HarnessResult:
    """Run full Wave 1 validation stack on an already normalized ontology."""

    ontology_result = _sorted_validation_result(validate_ontology(ontology))
    lint_result = _sorted_lint_result(lint_ontology(ontology))
    relation_result = _sorted_validation_result(validate_relation_catalog(ontology))

    stages = (
        _stage_from_validation_result("ontology_validation", ontology_result),
        _stage_from_lint_result("ontology_lint", lint_result),
        _stage_from_validation_result("relation_catalog_validation", relation_result),
    )

    success = all(stage.error_count == 0 for stage in stages)
    return Wave1HarnessResult(success=success, stages=stages)


def format_harness_report(result: Wave1HarnessResult) -> str:
    """Render deterministic multiline report for local review and CI logs."""

    lines = [
        f"success={str(result.success).lower()} errors={result.error_count} warnings={result.warning_count}",
    ]
    for stage in result.stages:
        lines.append(
            f"[{stage.name}] errors={stage.error_count} warnings={stage.warning_count}"
        )
        for error in stage.errors:
            lines.append(f"  ERROR {error}")
        for warning in stage.warnings:
            lines.append(f"  WARN  {warning}")
    return "\n".join(lines)


def _sorted_validation_result(result: ValidationResult) -> ValidationResult:
    return ValidationResult(
        errors=tuple(sorted(result.errors, key=lambda item: (item.path, item.code, item.message))),
        warnings=tuple(sorted(result.warnings, key=lambda item: (item.path, item.code, item.message))),
    )


def _sorted_lint_result(result: LintResult) -> LintResult:
    return LintResult(
        errors=tuple(sorted(result.errors, key=lambda item: (item.path, item.code, item.message))),
        warnings=tuple(sorted(result.warnings, key=lambda item: (item.path, item.code, item.message))),
    )


def _stage_from_validation_result(name: str, result: ValidationResult) -> HarnessStageResult:
    return HarnessStageResult(
        name=name,
        errors=tuple(_format_validation_message(message) for message in result.errors),
        warnings=tuple(_format_validation_message(message) for message in result.warnings),
    )


def _stage_from_lint_result(name: str, result: LintResult) -> HarnessStageResult:
    return HarnessStageResult(
        name=name,
        errors=tuple(_format_lint_message(message) for message in result.errors),
        warnings=tuple(_format_lint_message(message) for message in result.warnings),
    )


def _format_validation_message(message: ValidationMessage) -> str:
    return f"[{message.code}] {message.path}: {message.message}"


def _format_lint_message(message: LintMessage) -> str:
    return f"[{message.severity}/{message.code}] {message.path}: {message.message}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entrypoint for local harness execution."""

    import argparse

    parser = argparse.ArgumentParser(description="Run Wave 1 validation harness")
    parser.add_argument("ontology_path", type=Path)
    parser.add_argument("--relation-catalog-path", type=Path, default=None)
    args = parser.parse_args(argv)

    result = run_wave1_validation_harness(
        args.ontology_path,
        relation_catalog_path=args.relation_catalog_path,
    )
    print(format_harness_report(result))
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
