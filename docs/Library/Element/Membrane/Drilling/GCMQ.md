# (S)GCMQ

Generalised Conforming Mixed Quadrilateral With Drilling DoFs

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Translation, Rotation)
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

## References

1. [10.1002/nme.6066](https://doi.org/10.1002/nme.6066)
2. [10.1016/j.engstruct.2019.109592](https://doi.org/10.1016/j.engstruct.2019.109592)
3. [10.1016/j.engstruct.2020.110760](https://doi.org/10.1016/j.engstruct.2020.110760)

## Syntax

```
element GCMQ (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
# [8] string, integration switch, default: "I"

element GCMQI (1) (2...5) (6) [7] [8]
element GCMQL (1) (2...5) (6) [7] [8]
element GCMQG (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0

element SGCMQI (1) (2...5) (6) [7] [8]
element SGCMQL (1) (2...5) (6) [7] [8]
element SGCMQG (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

* Three integration schemes are available: "I", "L" and "G".
  - "I": Five-Point Irons Scheme
  - "L": 3rd Order Lobatto Scheme
  - "G": 3rd Order Gauss Scheme
* `GCMQ` is the full version described in [1] with enhanced strain, `SGCMQ` is a `PS` like element with no enhanced
  strain, the direct result of which is less computation is required (less than `CP8R`).
