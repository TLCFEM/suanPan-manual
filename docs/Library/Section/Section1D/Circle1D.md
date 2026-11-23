# Circle1D

1D Circle Section

## Background

`Circle1D` is a uniaxial section with a circular shape, defined by a radius and a one-dimensional material tag.
Its area is computed as $$\pi r^2$$ from the given radius, so it behaves as a `TrussSection` of that area with the radius retained only for reporting.
The section carries no bending or torsion terms, use a `Circle2D` or `Circle3D` section for beam elements.

## Syntax

```text title="Circle1D"
section Circle1D (1) (2) (3)
# (1) int, unique section tag
# (2) double, radius
# (3) int, material tag
```

## Remarks

The axial stiffness is the material stiffness times the area and the linear density is the material density times the area.
Prefer `Circle1D` when the bar is naturally specified by radius or diameter and `TrussSection` when the area is already known.
Like all 1D sections it is used by section-aware truss elements such as `T2D2S` and `T3D2S`.
