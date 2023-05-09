# set

The `set` command is used to set some properties of the analysis.

## Linear Elastic Simplification

In a general non-linear context, each substep requires at least two system solving, one for initial guess, one for
convergence test.
There is no general way to detect a linear system automatically,
with which we know the initial guess leads to convergence so that further system solving is not necessary.
To speed up simulation, one can use the following command to indicate the system is linear.

```
set linear_system true
```

With this enabled, only one system solving will be performed in each substep.

## Substepping Control

To use a fixed substep size, users can define

```
set fixed_step_size true
```

Otherwise, the algorithm will automatically substep the current step if convergence is not met. The time step control
strategy cannot be customized.

To define the initial step size, users can use

```
set ini_step_size (1)
# (1) double, substep size
```

To define the maximum/minimum step size, users can use

```
set max_step_size (1)
set min_step_size (1)
# (1) double, target time step size
```

## Solving Related Settings

### Matrix Storage Scheme

#### Asymmetric Banded

By default, an **asymmetric banded** matrix storage scheme is used. For 1D analysis, the global stiffness matrix is
always symmetric. However, when it comes to 2D and 3D analyses, the global stiffness may be structurally symmetric in
terms of its layout, but there may not have the same value on the symmetric entries. In maths language, if $$K(i,j)
\neq0$$ then $$K(j,i)\neq0$$, but $$K(i,j)\neq{}K(j,i)$$. Hence, an asymmetric banded storage is the safest.
The `_gbsv()` LAPACK subroutine is used for matrix solving.

#### Symmetric Banded

It shall be noted that the symmetric scheme can save almost $$50\%$$ of the memory used in the asymmetric scheme.
The `_pbsv()` LAPACK subroutine is used. This subroutine can only deal with **symmetric positive definite band matrix**.
For some problems, in which the matrix is not necessarily positive definite, for example the buckling problems, this
subroutine fails. **Before enabling the symmetric banded storage, the analyst must check if the matrix is SPD.**

#### Full Storage

If the problem scale is small, it does not hurt if a full storage scheme is used. For some particular issues such as
particle collision issues, the full storage scheme is the only option.

#### Full Packed Storage

If the matrix is symmetric, a so-called pack format can be used to store the matrix. Essentially, only the upper or the
lower triangle of the matrix is stored. The spatial cost is half of that of the full storage, but the solving speed is
no better. The `_spsv()` subroutine is used for matrix solving. It is not recommended using this packed scheme.

#### Sparse Storage

The sparse matrix is also supported. Several sparse solvers are implemented.

#### Direct System Solver

Different solvers are implemented for different storage schemes. It is possible to switch from one to another by using
the following command. Details are covered in the summary table.

```
set system_solver (1)
# (1) string, system solver name
```

### Mixed Precision Algorithm

The following command can be used to control if to use mixed precision refinement. This command has no effect if the
target matrix storage scheme has no mixed precision implementation.

```
set precision (1)
# (1) string, "single" ("mixed") or "double" ("full")
```

#### Iterative Refinement

The maximum number of refinements can be bounded by

```text
set iterative_refinement (1)
# (1) integer, maximum number of refinements
```

#### Iterative Refinement Tolerance

If the mixed precision algorithm is used, it is possible to use the following command to control the tolerance.

```text
set tolerance (1)
# (1) double, tolerance of the iterative solver
```

Typically, each refinement reduces the error by a factor of $$10^{-7}$$. Thus two or three refinements should be
sufficient to achieve the working precision.

Thus, the following command set makes sense.

```text
set precision mixed
set iterative_refinement 3
set tolerance 1e-15
```

### Summary

All available settings are summarised in the following table.

| storage       | configuration         | configuration        | system solver | mixed precision | subroutine in external library |
|---------------|-----------------------|----------------------|---------------|-----------------|--------------------------------|
| full          | `set symm_mat false`  | `set band_mat false` | `LAPACK`      | yes             | `d(s)gesv`                     |
|               |                       |                      | `CUDA`        | yes             | `cusolverDnD(S)gesv`           |
| symm. banded  | `set symm_mat true`   | `set band_mat true`  | `LAPACK`      | yes             | `d(s)pbsv`                     |
|               |                       |                      | `SPIKE`       | yes             | `d(s)spike_gbsv`               |
| asymm. banded | `set symm_mat false`  | `set band_mat true`  | `LAPACK`      | yes             | `d(s)gbsv`                     |
|               |                       |                      | `SPIKE`       | yes             | `d(s)spike_gbsv`               |
| symm. packed  | `set symm_mat true`   | `set band_mat false` | `LAPACK`      | yes             | `d(s)ppsv`                     |
| sparse        | `set sparse_mat true` |                      | `SuperLU`     | yes             | `d(s)gssv`                     |
|               |                       |                      | `CUDA`        | yes             | `cusolverSpD(S)csrlsvqr`       |
|               |                       |                      | `MUMPS`       | no              | `dmumps_c`                     |
|               |                       |                      | `PARDISO`     | no              | `pardiso`                      |
|               |                       |                      | `FGMRES`      | no              | `dfgmres`                      |

Some empirical guidance can be concluded as follows.

1. For most cases, the asymmetric banded storage with full precision solver is the most general option.
2. The best performance is obtained by using symmetric banded storage, if the (effective) stiffness matrix is guaranteed
   to be positive definite, users shall use it as a priority.
3. The mixed precision algorithm often gives the most significant performance boost for full storage with `CUDA` solver.
   It outperforms the full precision algorithm when the size of system exceeds several thousands.
4. The `SPIKE` solver is slightly slower than the conventional `LAPACK` implementations.
5. The `SuperLU` solver is slower than the `MUMPS` solver. The multithreaded `SuperLU` performs LU factorization in
   parallel but forward/back substitution in sequence.
6. The `PARDISO` direct solver and `FGMRES` iterative solver are provided by `MKL`.
7. The `MUMPS` solver supports both symmetric and asymmetric algorithms. One can use `set symm_mat true`
   or `set symm_mat false`.

### Iterative System Solver

[available from v2.5]

It is possible to use iterative solvers to solve the linear system of equations. Currently, two solvers are available
by using the following command.

```text
set system_solver BiCGSTAB
set system_solver GMRES
```

As the iterative solvers are relatively independent of the matrix storage scheme, thus, all different storage
schemes can be used along with different iterative solvers. One should beware that different storage schemes may
affect the performance of iterative solvers as they largely depend on matrix--vector multiplication.

Mixed precision solving is not supported by the iterative solvers.

[available from v3.0]

It is also possible to use GPU-based iterative solver powered by the [MAGMA](https://icl.utk.edu/magma/) library. The
binaries shipped officially are not compiled with GPU support. Users can compile the library with GPU support by
themselves. See [here](magma.md) for more details.

#### Preconditioner

Three preconditioners are available for the iterative solvers.

```text
set preconditioner None
set preconditioner Jacobi
set preconditioner ILU
```

The `None` preconditioner uses identify matrix as the preconditioner.

The `Jacobi` preconditioner uses the diagonal of the matrix as the preconditioner. This is the default one but may
not perform well for certain problems.

The `ILU` preconditioner uses the incomplete LU factorization of the matrix as the preconditioner. This `ILU`
preconditioner
is provided by the `SuperLU` library.

If the iterative solver is used, then it is possible to set the tolerance of the iterative solver. In this case,
tolerance assigned will not be used by mixed precision algorithm as it is not activated due to an iterative solver
is defined.

```text
set tolerance (1)
# (1) double, tolerance of the iterative solver
```

## Parallel Matrix Assembling

For dense matrix storage schemes, the global matrix is stored in a consecutive chunk of memory. Assembling global matrix
needs to fill in the corresponding memory location with potentially several values contributed by different elements.
Often in-place atomic summation is involved. To assign each memory location a mutex lock is not cost-efficient. Instead,
a $$k$$-coloring concept can be adopted to divide the whole model into several groups. Each group contains elements that
do not share common nodes with others in the same group. By such, no atomic operations are required. Elements in the
same group can be updated simultaneously so the matrix assembling is lock free.

By default, the coloring algorithm is enabled. To disable it, users can use the following command.

```
set color_model false
set color_model none
```

As a NP hard problem, there is no optimal algorithm to find the minimum chromatic number. The Welsh-Powell algorithm is
implemented in `suanPan`. The maximum independent set algorithm is also available, it may outperform the
Welsh-Powell algorithm on large models. To switch, users can use the following command.

```
# default to WP algorithm
set color_model WP
# switch to MIS algorithm
set color_model MIS
```

Also, depending on the problem setup, such a coloring may or may not help to improve the performance. If there are not a
large number of matrix assembling, the time saved may not be significant. Thus, for problems of small sizes, users may
consider disabling coloring.

This option has no effect if a sparse storage is used.

## Penalty Number

For some constraints and loads that are implemented by using the penalty method, the default penalty number can be
overridden.

```
set constraint_multiplier (1)
set load_multiplier (1)
# (1) double, new penalty number
```

This command does not overwrite user defined penalty number if the specific constraint or load takes the penalty number
than input arguments.

## FGMRES Iterative Tolerance

For `FGMRES` iterative solver, one can use the following dedicated command to control the tolerance of the algorithm.

```
set fgmres_tolerance (1)
# (1) double, tolerance
```

If the boundary condition is applied via the penalty method, say for example one previously
uses `set constraint_multiplier 1E8`, then there is no need to set a tolerance smaller than `1E-8`. A slightly larger
value is sufficient for an iterative algorithm, one can then set

```
set fgmres_tolerance 1E-6
```
