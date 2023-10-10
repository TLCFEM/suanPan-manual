# Ramm

Arc Length Algorithm Using Ramm's Approach

The Ramm's version of arc length algorithm is implemented. This solver can only be used in solving static problems.

## Syntax

```
solver Ramm (1) [2] [3] [4] [5]
# (1) int, unique solver tag
# [2] double, arc length, default: 0.1
# [3] bool string, fixed arc length switch, default: false
# [4] double, minimum arc length, default: 0.
# [5] double, maximum arc length, default: 0.
```

## Remarks

1. A proper arc length shall be manually input to achieve an efficient analysis.
2. Often the arc length is allowed to change depending on the smoothness of the turning point.
3. The computation of determinant is involved. A proper matrix storage scheme shall be activated. For dense matrix
   storage, please use asymmetric schemes by `set symm_mat false`. For sparse solvers, please use `MUMPS` only.
4. If the arc length is not fixed, a positive minimum/maximum arc length will kick in to prevent the arc length from
   being too small/large.
5. Any non-positive values for the minimum/maximum arc length will be ignored.
