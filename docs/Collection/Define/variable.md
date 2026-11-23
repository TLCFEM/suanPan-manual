# variable

Although the parser is not intended to function as a scripting language interpreter, it is sometimes useful to have limited macro-like capabilities.

## Syntax

One can use `var` or `variable` to define variables (macros).

```text title="variable"
variable (1) (2)
# (1) string, name
# (2) any read as string, value
```

To reference a defined variable, use a dollar sign `$` followed by the variable name.
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
    Thus, the order matters in this situation.
    This is because variables and macros are scanned and replaced while the command is being processed.

More advanced scripting functionality should be provided by other tools.
