# MaxDisplacement

The `MaxDisplacement` criterion tests the displacement of the specified node, if it is **greater** the given value, the
analysis is terminated.

## Syntax

```
criterion MaxDisplacement (1) (2) (3) (4)
# (1) int, unique criterion tag
# (2) int, node
# (3) int, dof
# (4) double, limit
```