import pandas as pd
import pytest

import pandas_commit_linter  # noqa: F401 - registers the accessor


def test_lint_marks_valid_conventional_commit():
    frame = pd.DataFrame({"message": ["feat: add export"]})

    result = frame.commit_lint.lint()

    assert result.loc[0, "valid"]


def test_lint_marks_bad_type_invalid():
    frame = pd.DataFrame({"message": ["feature: add export"]})

    result = frame.commit_lint.lint()

    assert not result.loc[0, "allowed_type"]
    assert not result.loc[0, "valid"]


def test_invalid_returns_original_rows():
    frame = pd.DataFrame({"sha": ["a", "b"], "message": ["fix: close issue", "oops"]})

    invalid = frame.commit_lint.invalid()

    assert invalid["sha"].tolist() == ["b"]


def test_missing_message_column_is_rejected():
    with pytest.raises(AttributeError, match="message"):
        pd.DataFrame({"subject": ["feat: nope"]}).commit_lint


def test_subject_length_can_be_configured():
    frame = pd.DataFrame({"message": ["feat: a long subject"]})

    result = frame.commit_lint.lint(max_subject_length=5)

    assert not result.loc[0, "subject_within_limit"]
    assert not result.loc[0, "valid"]
