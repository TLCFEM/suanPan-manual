# Mass

Point Mass

* Number of Nodes: 1
* Number of DoFs: varies

## Syntax

```text title="Mass"
Mass (1) (2) (3) (4...)
element Mass (1) (2) (3) (4...)
# (1) int, unique element tag
# (2) int, node tag
# (3) double, magnitude
# (4...) int, dof tag
```

Point mass is implemented via an element interface that connects only one node.
No stiffness is defined within that element.
Thus, a `Mass` object shares the same tag pool with the other elements.

## Variants

`Mass2D` creates a planar point mass: `Mass2D (1) (2) (3) (4...)` accepts at most three DoF tags, which map to U1, U2 and UR3, and no element is created if a tag larger than three is given.
`Mass3D` creates a spatial point mass with at most six DoF tags, which map to U1, U2, U3, UR1, UR2 and UR3; plain `Mass` is an alias for `Mass3D`.
