# Guide

Try the following flow chart to find the best membrane element to use.

1. Is the geometry regular or irregular?
   * regular --- use quadrilateral elements
   * irregular --- use triangular elements

## Triangular Elements

1. Is drilling DoF required?
   * yes --- [`Allman`](Drilling/Allman.md)
   * no --- go to Q2
2. Prefer speed or accuracy?
   * speed --- [`CP3`](Plane/CP3.md)
   * accuracy --- [`CP6`](Plane/CP6.md)

Noting that [`CP3`](Plane/CP3.md) element is very rigid and often requires a very dense mesh to get relatively accurate
result, it is not recommended for most applications.

## Quadrilateral Elements

1. Is drilling DoF required?
   * yes --- go to Q2
   * no --- go to Q3
2. Is consistent material stiffness available?
   * yes --- go to Q6
   * no --- [`GQ12`](Drilling/GQ12.md)
3. Used in elastoplastic applications?
   * yes --- normally mixed formulation is better, go to Q4, alternatively displacement based formulation, go to Q5
   * no --- go to Q5
4. Prefer speed or accuracy?
   * speed --- [`PS`](Mixed/PS.md)
   * accuracy --- [`QE2`](Mixed/QE2.md)
5. Prefer speed or accuracy?
   * speed --- [`CP4I`](Plane/CP4I.md) or second option [`CP4`](Plane/CP4.md)
   * accuracy --- [`CP8R`](Plane/CP8.md) or second option [`CP8`](Plane/CP8.md)
6. Need faster analysis?
   * yes --- [`SGCMQ`](Drilling/GCMQ.md)
   * no --- [`GCMQ`](Drilling/GCMQ.md)
