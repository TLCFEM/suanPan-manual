# Damper02

Maxwell Model

The `Damper02` is a Maxwell model that uses **displacement** and **velocity** as inputs, that is, element length is not
used to compute strain or strain rate.

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)

## Reference

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Syntax

```
element Damper02 (1) (2) (3) (4) (5) [6] [7] [8]
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
