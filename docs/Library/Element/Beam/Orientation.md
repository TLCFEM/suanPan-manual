# Orientation

An `orientation` is required for 3D beam elements to indicate how the section is oriented. The `orientation` object also
handles transformation between global and local coordinate systems of beam/truss elements.

For 2D beam elements, the local $$z$$-axis is defined to be the global $$z$$-axis.

## Syntax

```
orientation (1) (2) (3) (4) (5)
# (1) int, unique orientation tag
# (2) string, orientation type
# (3) double, x component of local z axis
# (4) double, y component of local z axis
# (5) double, z component of local z axis
```

## Remarks

1. For type `(2)`, currently only `B3DL` (stands for linear 3D beam transformation) and `B3DC` (corotational
   formulation) available.
2. The `B3DC` formulation is based on Crisfield's work with modifications. See de Souza's
   [thesis](https://books.google.co.nz/books/about/Force_based_Finite_Element_for_Large_Dis.html?id=YZ5NAQAAMAAJ).
