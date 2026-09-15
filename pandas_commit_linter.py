"""pandas-commit-linter: a DataFrame accessor for commit messages."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

__version__ = "0.1.0"
_DEFAULT_TYPES = ("feat", "fix", "docs", "refactor", "test", "chore", "build", "ci", "perf", "revert")


@pd.api.extensions.register_dataframe_accessor("commit_lint")
class CommitLintAccessor:
    """Lint commit messages stored in a DataFrame."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        if "message" not in pandas_obj.columns:
            raise AttributeError("DataFrame must contain a 'message' column")
        self._obj = pandas_obj

    def lint(
        self,
        *,
        max_subject_length: int = 72,
        require_conventional_type: bool = True,
        allowed_types: Iterable[str] = _DEFAULT_TYPES,
    ) -> pd.DataFrame:
        """Return per-row lint results without modifying the source DataFrame."""
        if max_subject_length < 1:
            raise ValueError("max_subject_length must be positive")
        messages = self._obj["message"].fillna("").astype(str)
        allowed = set(allowed_types)
        pattern = re.compile(r"^(?P<type>[a-z]+)(?:\([^\n()]+\))?!?:\s+\S.+$")
        parsed = messages.str.extract(pattern, expand=False)
        result = pd.DataFrame(index=self._obj.index)
        result["message_present"] = messages.str.strip().ne("")
        result["subject_within_limit"] = messages.str.split("\n", n=1).str[0].str.len().le(max_subject_length)
        result["conventional_format"] = parsed.notna()
        result["allowed_type"] = parsed.isin(allowed)
        if not require_conventional_type:
            result["allowed_type"] = True
        result["valid"] = result.all(axis=1)
        return result

    def invalid(self, **kwargs: object) -> pd.DataFrame:
        """Return source rows whose messages fail one or more lint rules."""
        results = self.lint(**kwargs)
        return self._obj.loc[~results["valid"]].copy()
