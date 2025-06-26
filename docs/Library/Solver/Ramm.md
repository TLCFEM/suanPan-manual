# Ramm

Arc Length Algorithm Using Ramm's Approach

The Ramm's version of arc length algorithm is implemented.
This solver can only be used in solving static problems.

## Syntax

```
solver Ramm (1)
# (1) int, unique solver tag
```

The step size in an arc-length analysis is now the arc length.
One can use the following to control stepping strategy.

```
set ini_step_size (1)
set min_step_size (1)
set max_step_size (1)
# (1) double, step size (arc length)

set fixed_step_size (1)
# (1) bool, flag to indicate if to fix the arc length
```

## Remarks

1. A proper arc length shall be manually input to achieve an efficient analysis.
2. Often the arc length is allowed to change depending on the smoothness of the turning point.
3. If the arc length is not fixed, a positive minimum/maximum arc length (step size) will kick in to prevent the
   arc length from being too small/large.
4. Any non-positive values for the minimum/maximum arc length will be ignored.

A good overview of the method and its implementation detail can be found in Crisfield's book (ISBN: 9780471929567), see Chapter 9.

Solvers for symmetric storage often require the target matrix to be positive definite.
This is **not** the case in arc-length related applications, although it can still be used for problems in which the tangent stiffness is positive definite.
Thus, as a rule of thumb, one may need to switch off `symm_mat`.

```text
set symm_mat 0
```

If positive definiteness is known to be guaranteed, symmetric storage can also be used.

For general cases, the (sign of) determinant of the tangent stiffness is required to identify turning points.
**Not all solvers support the computation of determinant.**

### Without MPI

Only `LAPACK` based solvers can be used.
Thus, one need to use the following settings.
Note they are all default settings thus do not need to be explicitly set.
The point is **do not choose something else**.

```text
set symm_mat 0
set band_mat 1
set sparse_mat 0
set system_solver LAPACK
```

### With MPI

Only the `MUMPS` solver is able to compute the determinant.
`ScaLAPACK` based solvers do not support inspection of factorization thus cannot provide an efficient way of computing determinant.
Thus, one need to enable sparse storage and choose the `MUMPS` solver.

```text
set sparse_mat 1
set system_solver MUMPS
```
