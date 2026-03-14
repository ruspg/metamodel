"""Shared Wave 1 validation message/result structures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ValidationMessage:
    code: str
    message: str
    path: str


@dataclass(frozen=True)
class ValidationResult:
    errors: Tuple[ValidationMessage, ...]
    warnings: Tuple[ValidationMessage, ...]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def is_valid(self) -> bool:
        return not self.errors
