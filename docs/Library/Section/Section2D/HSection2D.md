# HSection2D

2D H-Section

## Syntax

```
section HSection2D (1) (2...7) (8) [9] [10]
# (1) int, unique tag
# (2...7) double, section dimensions
# (8) int, material tag
# [9] int, number of integration points, default: 6
# [10] double, eccentricity measured from the centre, default: 0.0
```

## Remarks

1. Section dimensions are:
   * `(2)` left flange height
   * `(3)` left flange thickness
   * `(4)` right flange height
   * `(5)` right flange thickness
   * `(6)` web width
   * `(7)` web thickness

The eccentricity is measured from the centre of the web.
If the left and right flanges have different sizes, the default trivial eccentricity will lead to extra bending moments
when the section is subjected to axial force.
Eccentricity can be manually adjusted.

See [Eccentricity](../Eccentricity.md) for more details.
