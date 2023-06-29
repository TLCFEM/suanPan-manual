# analyze

The `analyze` or `analyse` command will trigger the analysis. The model will be initialized by initializing for example
elements and global storage of matrices.

All steps will be analysed. It is possible to define subsequent steps after performing the analysis.

## Syntax

```
analyze
analyse
```

[available from v3.1]

Before executing the analysis, the application checks if there are any warnings or errors.
If any, the analysis will not be performed.

It is possible to ignore warnings and errors by using the `--ignore-warnings` or `--ignore-errors` option.
Given that errors generally imply that the model is incorrect, it is not recommended to ignore errors.

Use the following syntax to ignore warnings and errors.

## Syntax

```
analyze [--ignore-warnings] [--ignore-errors]
analyse [--ignore-warnings] [--ignore-errors]
```
