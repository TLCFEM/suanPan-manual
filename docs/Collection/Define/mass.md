# mass

The `mass` command creates a point mass element attached to a single node for dynamic analysis.
It contributes only to the mass matrix, with no stiffness, and shares the element tag pool with other elements.

## Syntax

```text title="mass"
mass (1) (2) (3) (4...)
# (1) int, unique mass tag
# (2) int, node tag
# (3) double, magnitude
# (4...) int, dof tags, at least one and at most six
```

## Remarks

1. At least one DoF tag is required, and DoF tags greater than six are rejected.
2. For example, `mass 3 2 10 1 2 3` assigns a magnitude of 10 to DoFs 1, 2, and 3 of node 2.
3. See the [Mass](../../Library/Element/Special/Mass.md) element page for details.
