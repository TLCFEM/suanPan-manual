# sectiontest

This command category can be used to test sections without establishing a FE model.

## Syntax

```text
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

1.  The increment size could be either positive or negative.
2.  The loading direction reverses after given numbers of steps.
3.  The strain-stress history would be saved to `RESULT.txt`. If `HDF5` is used, the result would be additionally saved
    to `RESULT.h5`.
4.  The deformation vector consists of axial deformation, rotation about strong axis, rotation about weak axis. 1D, 2D
    and 3D sections have the first, first two and all three components respectively.

## Example

```text
material Bilinear1D 1 29 0.05 0.01

section US2D W21X68 1 1

sectiontest2d 1 1E-3 0 100
```

For the above example, a W21X68 section is defined with the bilinear hardening model. It is loaded with 100 increments
of $$0.001$$ axial deformation while the rotation is zero.
