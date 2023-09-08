# ISection3D

3D I-Section

## Syntax

```
section ISection3D (1) (2) (3) (4) (5) (6) (7) (8) [9] [10] [11]
# (1) int, unique section tag
# (2) double, top flange width
# (3) double, top flange thickness
# (4) double, bottom flange width
# (5) double, bottom flange thickness
# (6) double, web height
# (7) double, web thickness
# (8) int, material tag
# [9] int, number of integration points, default: 3
# [10] double, eccentricity along y axis, default: 0.0
# [11] double, eccentricity along z axis, default: 0.0
```

## Remarks

1. The flange/web is assumed to be slender. Thus, only one integration point is assigned across the thickness. The web,
   top flange and bottom flange share the same number of integration points over the height/width no matter how
   wide/tall the section is.

See [Eccentricity](../Eccentricity.md) for more details.
