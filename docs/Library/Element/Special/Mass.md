# Mass

Point Mass

* Number of Nodes: 1
* Number of DoFs: varies

## Syntax

```
Mass (1) (2) (3) (4...)
element Mass (1) (2) (3) (4...)
# (1) int, unique element tag
# (2) int, node tag
# (3) double, magnitude
# (4...) int, dof tag
```

Point mass is implemented via element interface that connects only one node. No stiffness is defined within that
element. Thus, a `Mass` object shares the same tag pool with the other elements.
