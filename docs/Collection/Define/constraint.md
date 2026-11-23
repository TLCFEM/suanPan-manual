# constraint

The `constraint` command defines a constraint between nodes or between a node and a geometric entity.
Please refer to the specific constraint types for the available syntax.

All constraints are processed in **parallel**.

Most constraints are implemented using both the penalty function and the Lagrange multiplier methods.
A brief discussion of the differences can be found on the [Constraint](../../Library/Constraint/Constraint.md) page.

## Syntax

```text title="constraint"
constraint (1) (2) ...
# (1) string, constraint type
# (2) int, unique constraint tag
```
