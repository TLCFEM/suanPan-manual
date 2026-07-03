# variable

Although the parser is not intended to function as a scripting language interpreter, it is sometimes useful to have limited macro-like capabilities available.

## Syntax

One can use `var` or `variable` to define variables (macros).

```text
variable (1) (2)
# (1) string, name
# (2) any read as string, value
```

To reference a defined variable, use dollar sign `$` with the variable name.
For example,

```text
variable ele_t GCMQG

element $ele_t 1 1 2 8 7 1 1
```

This is equivalent to the following.

```text
element GCMQG 1 1 2 8 7 1 1
```

!!! warning "variable must exist"
    The variable must exist (have been defined) when referenced.
    Thus the order matters in this situation.
    This is because the scan and replacement of variables/macros happen during the processing/parsing of the command.

More advanced scripting functionality shall be fulfilled by other tools.
