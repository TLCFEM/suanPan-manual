# CircleHollow3D

3D Hollow Circle Section

![arrangement](PIC/CircularHollow.svg)

The radius should be the outer radius, which shall be half of the overall diameter.

## Syntax

```
section CircularHollow3D (1) (2) (3) (4) [5] [6] [7]
# (1) int, unique section tag
# (2) double, radius
# (3) double, thickness
# (4) int, material tag
# [5] int, number of integration points of half circle, default: 10
# [6] double, eccentricity along y axis, default: 0.0
# [7] double, eccentricity along z axis, default: 0.0
```
