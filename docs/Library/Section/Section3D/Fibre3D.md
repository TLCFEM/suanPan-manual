# Fibre3D

3D Fibre Section

## Background

`Fibre3D` aggregates several three-dimensional beam sections into one section so that a composite or reinforced cross-section can be modelled with a single element.
On initialisation it copies each listed section, discards any whose section type is not three-dimensional with a warning, and sums their area, linear density and initial stiffness.
All fibres undergo the same section deformation, and their stiffness and resistance are accumulated to give the response of the assembly.
This is the natural way to combine a concrete cell such as `Rectangle3D` with reinforcing `Bar3D` sections placed at their eccentricities instead of adopting a single code-based section such as `US3D`.

## Syntax

```text title="Fibre3D"
section Fibre3D (1) [(2)...]
# (1) int, unique section tag
# [(2)...] int, associated section tags
```

## Remarks

Prefer a code-based section for standard rolled shapes with tabulated properties and `Fibre3D` for arbitrary composite sections or when each material needs its own nonlinear constitutive law.
`Fibre3DOS` is the OS counterpart used by `B31OS` elements, it is built with the OS3D section type and additionally sums the recorded section forces of its fibres.
`Fibre3D` is used with conventional 3D beam elements such as `F31`.

## Example

The fibre assembly of `Example/Element/F31.supan` combines a `Rectangle3D` cell with a `Bar3D` reinforcement.

```text
material MPF 1 1E2 2E-1 .05
section Rectangle3D 2 12 1 1
section Bar3D 3 100 1
section Fibre3D 1 2 3
element F31 1 1 2 1 1
```
