# CircularHollow2D

2D Hollow Circular Section

![arrangement](PIC/CircularHollow.svg)

The radius should be the outer radius, which shall be half of the overall diameter.

## Syntax

```
section CircularHollow2D (1) (2) (3) (4) [5] [6]
# (1) int, unique section tag
# (2) double, radius
# (3) double, thickness
# (4) int, material tag
# [5] int, number of integration points for half circle, default: 10
# [6] double, eccentricity/location, default: 0.0
```

## Remarks

The eccentricity is measured from the centre of the section.
