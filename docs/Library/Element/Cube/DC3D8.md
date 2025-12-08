# DC3D8

* Number of Nodes: 8
* Number of DoFs: 4 (Translation, Translation, Translation, Damage)
* DoF Label: U1, U2, U3, DAMAGE

## Syntax

```text
element DC3D8 (1) (2...9) (10) (11) (12)
# (1) int, unique element tag
# (2...9) int, eight corner nodes with conventional order
# (10) int, material tag
# (11) double, characteristic length
# (12) double, energy release rate
```
