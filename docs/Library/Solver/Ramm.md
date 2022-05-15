# Ramm

Arc Length Algorithm Using Ramm's Approach

The Ramm's version of arc length algorithm is implemented. This solver can only be used in solving static problems.

## Syntax

```
solver Ramm (1) [2] [3]
# (1) int, unique solver tag
# [2] double, arc length, default: 0.1
# [3] bool string, fixed arc length switch, default: false
```

## Remarks

1. A proper arc length shall be manually input to achieve an efficient analysis.
2. Often the arc length is allowed to change depending on the smoothness of the turning point. It is not recommended
   fixing arc length.
3. The computation of determinant is involved. A proper matrix storage scheme shall be activated. For dense matrix
   storage, please use asymmetric schemes by `set symm_mat false`. For sparse solvers, please use `MUMPS` only.
