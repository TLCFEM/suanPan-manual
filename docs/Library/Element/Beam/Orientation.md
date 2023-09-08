# Orientation

An `orientation` is required for 3D beam elements to indicate how the section is oriented. The `orientation` object also
handles transformation between global and local coordinate systems of beam/truss elements.

Similar configurations are also required in other FEM software, see,
for example, Section 26.3.4 `Beam element cross-section orientation` of the Abaqus Analysis User's Manual.

The local $$x$$-axis is along the cord of the beam element.
The local $$z$$-axis is often the strong axis of the section if there is one.
The local $$y$$-axis is defined to be the cross product of the local $$z$$-axis and the local $$x$$-axis.

Depending on the different literature and textbooks, different conventions may be used.
Thus, the term local $$z$$-axis may not be the same axis you may expect.
Please validate the orientation first before using it.

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
3. For brevity, the mass distribution does not follow the corotational formulation, implying that the mass matrix is
   always a constant matrix. This is often sufficient for applications in earthquake engineering. However, it is not
   recommended for other applications. An energy-reserving corotational formulation is required, see Crisfield's work.

One can use the following model to check how the orientation works.

```text
node 1 0 0 0
node 2 1 0 0
orientation B3DL 1 0. 0. 1.
material Elastic1D 1 1
section US3D W10X100 1 1
element B31 1 1 2 1 1
fix2 1 E 1
displacement 1 0 1 1 2
step static 1
analyze
peek node 2
exit
```
