# CST/CSM

Couple Stress Triangle/Membrane

* Number of Nodes: 3, 4, 5, 6, 7, 8
* Number of DoFs: 3 (Translation, Translation, Rotation)

## Reference

1. [arXiv:2207.02544](https://arxiv.org/abs/2207.02544)

## Syntax

```text
element CST3 (1) (2...*) (3) [4] [5]
element CST6 (1) (2...*) (3) [4] [5]
element CSM4 (1) (2...*) (3) [4] [5]
element CSM5 (1) (2...*) (3) [4] [5]
element CSM6 (1) (2...*) (3) [4] [5]
element CSM7 (1) (2...*) (3) [4] [5]
element CSM8 (1) (2...*) (3) [4] [5]
# (1) int, unique element tag
# (2...*) int, corresponding number of node tags
# (3) int, material tag
# [4] double, thickness, default: 1.0
# [5] double, characteristic length, default: -1.0
```

## Remarks

1. The geometry definitions of CS elements resemble those of CP elements (e.g., CP3, CP4, CP5, CP6, CP7, CP8).
2. The characteristic length `[5]` can be left as default value (negative) to automatically determine the value 
   based on geometry (square root of area), or set to a positive value to manually specify the fixed length.
3. Currently, only supports [`Elastic2D`](../../Material/Material2D/Elastic2D.md) and [`Bilinear2D`](../../Material/Material2D/Bilinear2D.md) 
   materials.
