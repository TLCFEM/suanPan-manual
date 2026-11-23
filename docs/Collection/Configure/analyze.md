# analyze

The `analyze` (or `analyse`) command triggers the analysis.
The model is initialized by setting up the elements, the global matrix storage and other components.

All steps are analysed.
Subsequent steps can be defined after performing the analysis.

## Syntax

```text title="analyze"
analyze
analyse
```

Before executing the analysis, the application checks for warnings and errors.
If any are found, the analysis is not performed.

Warnings and errors can be ignored with the `--ignore-warnings` and `--ignore-errors` options.
[available from v3.1]

```text title="analyze with options"
analyze [--ignore-warnings] [--ignore-errors]
analyse [--ignore-warnings] [--ignore-errors]
```

Given that errors generally imply that the model is incorrect, ignoring them is not recommended.
