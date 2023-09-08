# TSection2D

2D T-Section

## Syntax

```
section TSection2D (1) (2...5) (6) [7] [8]
# (1) int, unique tag
# (2...5) double, section dimensions
# (6) int, material tag
# [7] int, number of integration points, default: 6
# [8] double, eccentricity measured from the web centre, default: 0.0
```

## Remarks

1. Section dimensions are:
   * `(2)` top flange height
   * `(3)` top flange thickness
   * `(4)` web width
   * `(5)` web thickness
2. By default, the flange is at the top of the local coordinate system.

The eccentricity is measured from the centre of the web.
The default trivial eccentricity will lead to extra bending moments when the section is subjected to axial force since
the section is not symmetric.
Eccentricity can be manually adjusted.

See [Eccentricity](../Eccentricity.md) for more details.
