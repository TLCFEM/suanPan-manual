# DCP4

Bilinear Quadrilateral With Crack Phase

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Translation, Damage)
* DoF Label: U1, U2, DAMAGE
* Integration Scheme: 2nd Order Gauss
* Zero Mass Entries On Damage DoFs

![encoding](../../PIC/Q4.svg)

## Syntax

```text title="DCP4"
element DCP4 (1) (2...5) (6) (7) (8) [9]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, characteristic length
# (8) double, energy release rate
# [9] double, element thickness, default: 1.0
```

## Remarks

* The third DoF is the damage variable.
  Boundary conditions can be assigned.
* The characteristic length `(7)` can be set to a negative value to automatically determine it based on the element geometry.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| DAMAGE         | damage variable  |

## Variants

`DCP4M` uses the same command `element DCP4M (1) (2...5) (6) (7) (8) [9]` as `DCP4`, but solves displacement and damage monolithically by adding their coupling blocks to the stiffness matrix instead of using a staggered update.
