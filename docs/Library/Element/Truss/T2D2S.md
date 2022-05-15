# T2D2S

2D Linear Truss Using Section

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)

## Syntax

```
element T2D2S (1) (2) (3) (4) [6] [7] [8]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
# [6] bool string, if to use log strain, default: false
```

## Remarks

1. Compared to `T2D2` , `T2D2S` use section instead of material. Hence, sectional area is handled by the corresponding
   section model.
2. The nonlinearity cannot propagate into the section level. So it is not possible to update area in `T2D2S`.
