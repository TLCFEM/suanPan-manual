# FixedLength

The Lagrange multiplier method can be used to define constraints. Extra storage is required for the so-called auxiliary
border stiffness matrix. The constraint is satisfied exactly.

The `FixedLength2D` and `FixedLength3D` constraints behave similar to the `Tie` element, the nonlinear constraint is
implemented via Lagrange multiplier method.

It shall not be used with global damping models in dynamic analysis since it alters the frequency distribution, leading
to an unintended damping response.
Only damping models that do not depend on system properties can be used.

## Syntax

```
fixedlength2d (1) (2) (3)
fixedlength3d (1) (2) (3)
constraint fixedlength2d (1) (2) (3)
constraint fixedlength3d (1) (2) (3)
# (1) int, unique constraint tag
# (2) int, node tag
# (3) int, node tag
```

## Example

![two cantilever beams](FixedLength.gif)

A vertical load is applied to the free end of the top beam.
The free ends of the two beams are connected by a `FixedLength2D` constraint.

```text
node 1 0 0
node 2 1 0
node 11 .2 0
node 12 .4 0
node 13 .6 0
node 14 .8 0

node 3 1 -.2
node 4 2 -.2
node 21 1.2 -.2
node 22 1.4 -.2
node 23 1.6 -.2
node 24 1.8 -.2

material Elastic1D 1 10

element EB21 1 1 11 12 1 1 1
element EB21 2 11 12 12 1 1 1
element EB21 3 12 13 12 1 1 1
element EB21 4 13 14 12 1 1 1
element EB21 5 14 2 12 1 1 1

element EB21 6 3 21 12 1 1 1
element EB21 7 21 22 12 1 1 1
element EB21 8 22 23 12 1 1 1
element EB21 9 23 24 12 1 1 1
element EB21 10 24 4 12 1 1 1

fix2 1 P 1 4

constraint FixedLength2D 2 2 3

cload 1 0 10 2 2

step static 1 1
set ini_step_size 1E-2
set fixed_step_size true
set symm_mat false

converger RelIncreDisp 1 1E-10 10 1

analyze

exit
```
