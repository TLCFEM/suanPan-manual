# sectiontest

This command category tests sections without establishing an FE model.

## Syntax

```text title="sectiontest"
sectionTest1D (1) (2) (3) [4...]
# (1) int, unique tag of the section model to use
# (2) double, size of per deformation increment
# (3) int, number of steps along increment direction
# [4...] int, optional numbers of steps for deformation history

sectionTest2D (1) (2...3) (4) [5...]
# (1) int, unique tag of the section model to use
# (2...3) double, size of per deformation increment
# (4) int, number of steps along increment direction
# [5...] int, optional numbers of steps for deformation history

sectionTest3D (1) (2...4) (5) [6...]
# (1) int, unique tag of the section model to use
# (2...4) double, size of per deformation increment
# (5) int, number of steps along increment direction
# [6...] int, optional numbers of steps for deformation history
```

## Remarks

1. The increment size can be either positive or negative.
2. The loading direction reverses after the given number of steps.
3. The deformation-resistance history is saved to `RESULT.txt`.
   If HDF5 support is enabled, the result is additionally saved to `RESULT.h5`.
4. The deformation vector consists of axial deformation, rotation about the strong axis and rotation about the weak axis.
   1D, 2D and 3D sections have the first, first two and all three components, respectively.

## Example

```text
material Bilinear1D 1 29 0.05 0.01

section US2D W21X68 1 1

sectiontest2d 1 1E-3 0 100
```

In the example above, a W21X68 section is defined with the bilinear hardening model.
It is loaded with 100 increments of $$0.001$$ axial deformation while the rotation is zero.
