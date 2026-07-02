# variable

Although the parser is not intended to function as a scripting language interpreter, it is sometimes useful to have limited macro-like capabilities available.

## Syntax

One can use `var` or `variable` to define variables (macros).

```text
variable ${1:(1)} ${2:(2)}
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

More advanced scripting functionality shall be fulfilled by other tools.
