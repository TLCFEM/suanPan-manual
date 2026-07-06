# Guide

Only general purpose elements for plane strain/stress problems are included.
For other special purpose elements, there are not many options anyway.

Try the following decision tree to find the best membrane element to use.

1. Is the geometry regular or irregular?
   * regular --- use quadrilateral elements that are often more flexible than triangular elements thus provide better results with the same amount of DoFs
   * irregular --- use triangular elements unless a good mesh can be generated to avoid distorted geometry

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
   * no --- [`GQ12`](Drilling/GQ12.md), it does not require local inversion so works even material tangent stiffness is not exact (but global convergence may still be an issue)
3. Used in elastoplastic applications?
   * yes --- normally mixed formulation is better, go to Q4, alternatively displacement based formulation, go to Q5
   * no --- go to Q5
4. Prefer speed or accuracy?
   * speed --- [`PS`](Mixed/PS.md), very cheap to compute, only with a different strain matrix
   * accuracy --- [`QE2`](Mixed/QE2.md), has enhanced strain field, requires more local computation
5. Prefer speed or accuracy?
   * speed --- [`CP4I`](Plane/CP4I.md) or second option [`CP4`](Plane/CP4.md)
   * accuracy --- [`CP8R`](Plane/CP8.md) or second option [`CP8`](Plane/CP8.md)
6. Need faster analysis?
   * yes --- [`SGCMQ`](Drilling/GCMQ.md), GCMQ with no enhanced strain, very cheap to compute, only with a different strain matrix
   * no --- [`GCMQ`](Drilling/GCMQ.md), best coarse mesh accuracy, requires local inversion
