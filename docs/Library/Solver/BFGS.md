# BFGS

The `BGFS` solver uses the rank two update algorithm BGFS. Alternatively, the limited memory version can also be
switched on.

## Syntax

```
solver BFGS (1)
solver LBFGS (1) [2]
# (1) int, unique solver tag
# [2] int, number of steps stored, default: 20
```
