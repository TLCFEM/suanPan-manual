# Fibre1D

1D Fibre Section

## Background

`Fibre1D` aggregates several one-dimensional sections under one section tag so that a single axial member can be made of different materials.
On initialisation it copies each listed section and keeps only those whose section type is also one-dimensional, an incompatible section is skipped with a warning.
The total area, linear density and initial stiffness are the sums of the corresponding quantities of all fibres.
Every fibre receives the same axial deformation and its stiffness and resistance are accumulated to form the response of the whole section.

## Syntax

```text title="Fibre1D"
section Fibre1D (1) [(2)...]
# (1) int, unique section tag
# [(2)...] int, associated section tags
```

## Remarks

Use a single `TrussSection` for a homogeneous bar and `Fibre1D` when several constitutive laws must be tracked separately, for example a steel core sharing axial strain with an FRP jacket.
All listed sections must be one-dimensional, use `Fibre2D` or `Fibre3D` for beam sections.
The parent forwards characteristic length, clear, commit and reset operations to every fibre so that the material history of each constituent is preserved.

## Example

The following is adapted from `Example/Section/Fibre1D.supan`.

```text
node 1 0 0
node 2 4 0
material MPF 1 100 300 .4
section Rectangle1D 1 1 1 1
section Circle1D 2 1 1
section TrussSection 3 1 1
section Fibre1D 4 1 2 3
element T2D2S 1 1 2 4 1 1
fix 1 E 1
```
