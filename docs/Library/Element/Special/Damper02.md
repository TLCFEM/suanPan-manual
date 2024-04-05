# Damper02/Damper04

Maxwell Model

The `Damper02` and `Damper04` are Maxwell models that use **displacement** and **velocity** as inputs, that is, 
element length is not used to compute strain or strain rate.

## References

The Maxwell model allows combinations of nonlinear springs and dampers. The algorithm implemented is documented in the
following paper.

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Damper02

The `Damper02` is the 2D version.

* Number of Nodes: 2
* Number of DoFs: 2 (Translation: UX, Translation: UY)

## Damper04

The `Damper04` is the 3D version.

* Number of Nodes: 2
* Number of DoFs: 3 (Translation: UX, Translation: UY, Translation: UZ)

## Syntax

```
element Damper02 (1) (2) (3) (4) (5) [6] [7] [8]
element Damper04 (1) (2) (3) (4) (5) [6] [7] [8]
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, damper tag
# (5) int, spring tag
# [6] bool string, if to use matrix in iteration, default: true
# [7] int, the maximum delay number, default: 0
# [8] double, beta, default: 0.5
```

## Remarks

1. Parameter `[7]` indicates if to stack diverged increments into next iteration. If $$0$$ is assigned, the material
   returns a failure flag as long as local iteration fails to converge. If $$n>0$$, a maximum $$n$$ increments are
   allowed to be stacked before exit due to divergence.
2. The `[8]` parameter controls the local time integration, $$\beta\in[0,1]$$ shall be defined. The default value
   $$0.5$$ implies a constant acceleration rule for the spring component in the Maxwell model.
