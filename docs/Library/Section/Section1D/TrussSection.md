# TrussSection

1D Truss Section

## Background

`TrussSection` is the generic uniaxial section, it takes a cross-sectional area and a one-dimensional material tag without any shape information.
The axial stiffness and resistance are the material stiffness and stress multiplied by the area, and the linear density is the material density multiplied by the area.
It has no eccentricity or bending terms and is intended for axial-only members.

## Syntax

```text title="TrussSection"
section TrussSection (1) (2) (3)
# (1) int, unique section tag
# (2) double, section area
# (3) int, material tag
```

## Remarks

Use `Circle1D` when the area is more conveniently given as a radius, and a code-based or fibre section when sectional bending must be represented.
Several `TrussSection`s with different materials can be combined through `Fibre1D` to model a composite axial member.
1D sections are used by `T2D2S` and `T3D2S` elements.
