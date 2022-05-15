# Syntax

## Command

All commands are case **insensitive**. Each command by default shall be written in one line.

It is not allowed to write two commands in one line.

To split one command into several lines, use the backslash (`\`) to concatenate. Only **one** backslash can serve as
concatenation symbol in one line. Other backslashes (if any) will be kept and combined with other lines and may lead to
wrongly interpreted command.

The leading and trailing whitespaces would be omitted by default.

## Separator/Delimiter

Either whitespace (`_`), including tab (`\t`), or comma (`,`) can be used as separator/delimiter.

## Comment

Comment lines start with the hash symbol (`#`) or the exclamation symbol (`!`).

Inline comments shall be denoted with the exclamation symbol (`!`) only. All contents after the first `!` will be
treated as comments.

Comments can be mixed with concatenation. There can only be white spaces between `\` and `!`.

```
# this is a comment
! this is another comment
node 1 2 3 4 5 6 ! this is an inline comment
# split one command into multiple lines
node 2 9 7 5 1 3 \
3 4 5 \ ! comments can be put after backslash \
9 8 2
```

## Input

Inputs are mostly integers, doubles and strings. The model input file is a plain text file, scripting of any sorts is
not supported. Math expressions are not available.

When the required input argument is an integer, it is not allowed to have a double in place. The decimal point cannot be
read by the integer parser so may cause failure of command parsing.

However, a double input can be replaced by an integer (if desired value matches), type conversion is automatically done.

Some commands take Boolean values in form of string. For `true` value, following inputs are equivalent: `true`, `yes`
, `1`, `on`, `t`, `y`. For `false` value, following inputs are equivalent: `false`, `no`, `0`, `off`, `f`, `n`. Again,
commands, including inputs, are case-insensitive.

For all commands, compulsory arguments are denoted by rounded brackets `(n)`, optional arguments are denoted by square
brackets `[n]`. Input arguments shall be defined in sequence. To change the default value of any optional arguments, all
leading optional arguments (if any) shall be explicitly defined. For group arguments, `(n n+1...)` means arguments `n`
and `n+1` appear as a group and must be defined due to rounded brackets, while `( ...)` means this group can be repeated
to define a set of arguments. For square case, `[ ...]` means this group is optional.
