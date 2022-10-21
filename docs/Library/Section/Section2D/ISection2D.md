# ISection2D

2D I-Section

## Syntax

```
section ISection2D (1) (2...7) (8) [9] [10]
# (1) int, unique tag
# (2...7) double, section dimensions
# (8) int, material tag
# [9] int, number of integration points, default: 6
# [10] double, eccentricity measured from the centre, default: 0.0
```

## Remarks

1. Section dimensions are:
   * `(2)` top flange height
   * `(3)` top flange thickness
   * `(4)` bottom flange height
   * `(5)` bottom flange thickness
   * `(6)` web width
   * `(7)` web thickness
