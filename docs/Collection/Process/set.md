# set

The `set` command configures properties of the analysis.

## General Settings

The following settings apply globally and can be used before any step is defined.

```text
set num_threads (1)
set screen_output (2)
set verbose_output (2)
# (1) int, number of threads used by OpenMP-based parallelisation
# (2) string, boolean value such as `true` or `false`
```

The output folder can be changed with `set output_folder`, which is described in [OutputFolder](../../Library/Recorder/OutputFolder.md).

`set num_nodes` sets the number of compute nodes reported by `peek num_nodes`.
It defaults to the size of the MPI communicator.

## Linear Elastic Simplification

In a general non-linear context, each substep requires at least two system solving steps: one for the initial guess and one for the convergence test.
There is no general way to detect a linear system automatically.
For a linear system, the initial guess leads to convergence, so further system solving is not necessary.
To speed up the simulation, use the following command to indicate that the system is linear.

```
set linear_system true
```

With this enabled, only one system solve is performed in each substep.

## Substepping Control

To use a fixed substep size, define

```
set fixed_step_size true
```

Otherwise, the algorithm automatically substeps the current step if convergence is not met.
The time step control strategy cannot be customized.

To define the initial step size, use

```
set ini_step_size (1)
# (1) double, substep size
```

To define the maximum or minimum step size, use

```
set max_step_size (1)
set min_step_size (1)
# (1) double, target time step size
```

To define the maximum number of substeps allowed in a step, use

```
set max_iteration (1)
# (1) int, maximum number of substeps
```

## Solving Related Settings

### Matrix Storage Scheme

#### Asymmetric Banded

By default, an **asymmetric banded** matrix storage scheme is used.
For 1D analysis, the global stiffness matrix is always symmetric.
In 2D and 3D analyses, however, the global stiffness matrix may be structurally symmetric in its layout, but the symmetric entries may not have the same value.
In mathematical terms, if $$K(i,j)\neq0$$, then $$K(j,i)\neq0$$, but $$K(i,j)\neq{}K(j,i)$$.
An asymmetric banded storage is therefore the safest choice.
The `_gbsv()` LAPACK subroutine is used for matrix solving.

#### Symmetric Banded

The symmetric scheme can save almost $$50\%$$ of the memory used by the asymmetric scheme.
The `_pbsv()` LAPACK subroutine is used.
This subroutine can only handle a **symmetric positive definite banded matrix**.
For problems in which the matrix is not necessarily positive definite, such as buckling problems, this subroutine fails.
**Before enabling symmetric banded storage, the analyst must check that the matrix is SPD.**

#### Full Storage

For a small problem, using a full storage scheme is acceptable.
For some particular problems, such as particle collision, full storage is the only option.

#### Full Packed Storage

If the matrix is symmetric, a so-called packed format can be used to store it.
Essentially, only the upper or lower triangle of the matrix is stored.
The memory cost is half that of full storage, but the solving speed is no better.
The `_spsv()` subroutine is used for matrix solving.
This packed scheme is not recommended.

#### Sparse Storage

Sparse matrices are also supported.
Several sparse solvers are implemented.

### Direct System Solver

Different solvers are implemented for different storage schemes.
Use the following command to switch between them.
Details are covered in the summary table.

```
set system_solver (1)
# (1) string, system solver name
```

Some integrators solve additional systems alongside the global one.
Use `set sub_system_solver` to select the solver for those auxiliary systems.

```
set sub_system_solver (1)
# (1) string, auxiliary system solver name
```

Accepted values are `LAPACK`, `SPIKE`, `SUPERLU`, `LIS`, `MUMPS`, `CUDA`, `PARDISO` and `FGMRES`, subject to the libraries available in the build.

#### Mixed Precision Algorithm

The following command can be used to control whether to use mixed precision refinement.
This command has no effect if the target matrix storage scheme has no mixed precision implementation.

```
set precision (1)
# (1) string, "single" ("mixed") or "double" ("full")
```

#### Iterative Refinement

The mixed precision algorithm requires iterative refinement.
The maximum number of refinements can be limited with

```text
set iterative_refinement (1)
# (1) integer, maximum number of refinements
```

It **cannot** exceed 256.

#### Iterative Refinement Tolerance

If the mixed precision algorithm is used, use the following command to control the tolerance.

```text
set tolerance (1)
# (1) double, tolerance
```

Typically, each refinement reduces the error by a factor of $$10^{-7}$$.
Two or three refinements should therefore be sufficient to achieve the working precision.

The following settings are reasonable.

```text
set precision mixed
set iterative_refinement 3
set tolerance 1e-15
```

### Iterative System Solver

Iterative solvers are available for sparse storage.
The [`Lis`](https://www.ssisc.org/lis/) library provides a wide range of solvers and preconditioners.
See [here](lis.md) for more details.

A GPU-based iterative solver powered by the [MAGMA](https://icl.utk.edu/magma/) library is also available.
The officially shipped binaries are **not** compiled with GPU support.
Users can compile the library with GPU support themselves.
See [here](magma.md) for more details.

### Summary

#### For Single Node Machine

With `SP_ENABLE_MPI` **disabled**, all available settings are summarised in the following table.

| storage       | configuration         | configuration        | system solver  | mixed precision | subroutine in external library |
|---------------|-----------------------|----------------------|----------------|-----------------|--------------------------------|
| full          | `set symm_mat false`  | `set band_mat false` | `LAPACK`       | yes             | (default) `d(s)gesv`           |
|               |                       |                      | `CUDA`         | yes             | `cusolverDnD(S)gesv`           |
| symm. banded  | `set symm_mat true`   | `set band_mat true`  | `LAPACK`       | yes             | (default) `d(s)pbsv`           |
|               |                       |                      | `SPIKE`        | yes             | `d(s)spike_gbsv`               |
| asymm. banded | `set symm_mat false`  | `set band_mat true`  | (not required) | yes             | `d(s)gbsv`                     |
| symm. packed  | `set symm_mat true`   | `set band_mat false` | (not required) | yes             | `d(s)ppsv`                     |
| sparse        | `set sparse_mat true` |                      | `SuperLU`      | no              | (default) `d(s)gssv`           |
|               |                       |                      | `CUDA`         | yes             | `cusolverSpD(S)csrlsvqr`       |
|               |                       |                      | `PARDISO`      | no              | `pardiso`                      |
|               |                       |                      | `FGMRES`       | no              | `dfgmres`                      |

#### For Multi Node Cluster

With `SP_ENABLE_MPI` **enabled**, all available settings are summarised in the following table.

| storage       | configuration         | configuration        | system solver  | mixed precision | subroutine in external library |
|---------------|-----------------------|----------------------|----------------|-----------------|--------------------------------|
| full          | `set symm_mat false`  | `set band_mat false` | (not required) | no              | `pdgesv`                       |
| symm. banded  | `set symm_mat true`   | `set band_mat true`  | (not required) | no              | `pdpbsv`                       |
| asymm. banded | `set symm_mat false`  | `set band_mat true`  | (not required) | no              | `pdgbsv`                       |
| symm. packed  | `set symm_mat true`   | `set band_mat false` | (not required) | no              | `pdposv`                       |
| sparse        | `set sparse_mat true` |                      | `PARDISO`      | no              | `cluster_sparse_solver`        |
|               |                       |                      | `LIS`          | no              | `lis_solve`                    |
|               |                       |                      | `MUMPS`        | no              | (default) `dmumps_c`           |

Some empirical guidance can be drawn as follows.

1. For most cases, the asymmetric banded storage with a full precision solver is the most general option.
2. The best performance is obtained with symmetric banded storage.
   If the (effective) stiffness matrix is guaranteed to be positive definite, users should use it as the first choice.
3. The mixed precision algorithm often gives the most significant performance boost for full storage with the `CUDA` solver.
   It outperforms the full precision algorithm when the size of the system exceeds several thousands.
4. The `SPIKE` solver is slightly slower than the conventional `LAPACK` implementations.
5. The `PARDISO` direct solver and `FGMRES` iterative solver are provided by `MKL`.

## Parallel Matrix Assembling

For dense matrix storage schemes, the global matrix is stored in a consecutive chunk of memory.
Assembling the global matrix requires writing several values, contributed by different elements, to the same memory location.
Often in-place atomic summation is involved.
Assigning a mutex lock to each memory location is not cost-efficient.
Instead, a $$k$$-coloring concept can be adopted to divide the whole model into several groups.
Each group contains elements that do not share common nodes with others in the same group.
In this way, no atomic operations are required.
Elements in the same group can be updated simultaneously, so matrix assembly is lock-free.

By default, the coloring algorithm is enabled.
To disable it, use the following command.

```
set color_model false
set color_model none
```

Finding the **minimum** chromatic number is an NP-hard problem.
The goal, however, is to find a number small enough to make good use of parallelism.
The [Welsh-Powell](https://doi.org/10.1093/comjnl/10.1.85) algorithm is implemented.
It is a sequential algorithm that may be slow on large problems.
The [maximum independent set](https://en.wikipedia.org/wiki/Maximal_independent_set) algorithm is also available.
It outperforms the Welsh-Powell algorithm on large models because it is parallelised.
To switch, use the following command.

```
# default to MIS algorithm
set color_model MIS
# switch to WP algorithm
set color_model WP
```

Depending on the problem setup, such coloring may or may not improve performance.
If there are not many matrix assembly operations, the time saved may not be significant.
For small problems, users may therefore consider disabling coloring.

This option has no effect if a sparse storage is used.

## Penalty Number

For constraints and loads implemented with the penalty method, the default penalty number can be overridden.

```
set constraint_multiplier (1)
set load_multiplier (1)
# (1) double, new penalty number
```

This command does not overwrite the user-defined penalty number if the specific constraint or load takes the penalty number as an input argument.

## FGMRES Iterative Tolerance

For the `FGMRES` iterative solver, use the following dedicated command to control the algorithm tolerance.

```
set fgmres_tolerance (1)
# (1) double, tolerance
```

If the boundary condition is applied with the penalty method, for example with `set constraint_multiplier 1E8`, there is no need to set a tolerance smaller than `1E-8`.
A slightly larger value is sufficient for an iterative algorithm.
One can then set

```
set fgmres_tolerance 1E-6
```

## Eigen Analysis

For a [`Frequency`](../../Library/Step/Frequency.md) step, the number of requested eigenvalues can be specified with

```
set eigen_number (1)
# (1) int, number of eigenvalues
```

This setting has no effect on other step types.
