# pwd

The `pwd` command resembles its counterpart in Unix-like systems.
It can print or set the current working directory.

To load files from another path while saving keystrokes, set the current working directory to the folder containing the model script first.

## Syntax

To check the current working directory, use

```text title="pwd"
pwd
```

To change the current working directory, use

```
pwd (1)
# (1) string, new absolute working path
```

On Windows, `\` must be written as `\\` or `/`.
Relative paths are resolved against the current working directory.
