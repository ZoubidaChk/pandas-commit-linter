# pandas-commit-linter

A small pandas DataFrame accessor for linting GitHub commit messages.

## Install

```bash
pip install pandas-commit-linter
```

For local development:

```bash
pip install -e .[test]
```

## Usage

Import the package once to register the `commit_lint` accessor:

```python
import pandas as pd
import pandas_commit_linter  # registers DataFrame.commit_lint

commits = pd.DataFrame(
    {
        "sha": ["abc123", "def456"],
        "message": ["feat: add CSV export", "added some stuff"],
    }
)

results = commits.commit_lint.lint()
print(results[["message", "valid"]])
```

Before: commit-message checks usually require repeated string-processing code.

After: call `commits.commit_lint.lint()` for per-row checks, or
`commits.commit_lint.invalid()` to return only failing commit rows.

The first version checks that messages are present, use a supported Conventional
Commit type, and keep the subject at 72 characters or fewer.

## Development

```bash
pip install -e .[test]
pytest
```

## License

MIT
