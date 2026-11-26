# Frequency

The (generalized) eigenvalue problem is handled in the `Frequency` step.
To define a valid step, please use the following command.

```
step frequency (1) [2] [3]
# (1) int, unique step tag
# [2] int, number of eigen modes to be solved, default: 1
# [3] string, eigenvalue type, default: s
```

To successfully run an eigen analysis, the system shall be symmetric, otherwise complex eigenvalues are computed.
This typically requires the stiffness matrix to be symmetric.
Besides, it must have

1. a positive definite stiffness matrix,
2. a semi-positive definite mass matrix.

## Remarks

1. The symmetric banded storage uses the `_pbsv` solver which only accepts a symmetric positive definite banded matrix.
   If the `Frequency` fails to compute the required eigen modes, please use other storage schemes.
2. The computed eigenvalue is the eigenvalue of the system.
   In the field of structural dynamics, it is $$\omega^2$$.
   The (angular) frequency and period can be computed accordingly.
3. The constrained (generalized) eigenvalue problems cannot be handled when the constraints are implemented via the Lagrange multiplier method.
   If the system contains constraints, users shall make sure they are applied via the penalty function method.

## Modal Properties

The eigenanalysis itself stores the eigenvalues and eigenvectors in the global factory.
To write frequencies, mode shapes, participation factors, effective modal masses and modal elastic forces to an HDF5 file, use the [Modal recorder](../Recorder/ModalRecorder.md).

```
recorder 1 hdf5 Modal U1
step frequency 1 10
analyze
save recorder 1
```

## FEAST Solver

By default, the `ARPACK` solver is used to solve the generalized eigen problem.

The [FEAST Eigenvalue Solver](http://www.feast-solver.org/) can also be used.
To switch, one can use

```
solver FEAST (1) (2) (3) [4]
# (1) int, unique solver tag
# (2) int, number of eigen modes
# (3) double, centre
# [4] double, radius, default: centre
```

`FEAST` solves the linear generalized eigenproblem.

Currently, the `FEAST` solver can be applied to full, banded, symmetric banded and sparse storage.
For asymmetric banded storage, use the `SPIKE` solver.

```
set system_solver SPIKE
```

For the given centre $$c$$ and radius $$r$$, the FEAST solver seeks eigenvalues within the bracket $$[c-r,c+r]$$.
If the radius is not assigned, it defaults to $$c$$, thus the bracket becomes $$[0,2c]$$.

## Example

Consider a massless elastic cantilever beam with lumped end mass.
Assume the length is $$L=2.84$$, the elastic modulus is $$E=94.13$$, the moment of inertia is $$I=1.34$$ and the lumped mass is $$M=5.76$$ so that

$$
\omega^2=\dfrac{3EI}{ML^3}=\dfrac{3\times94.13\times1.34}{5.76\times2.84^3}=2.8680.
$$

```
node 1 0 0
node 2 0 2.84
material Elastic1D 1 94.13
element EB21 1 1 2 1 1.34 1
mass 2 2 5.76 1
fix 1 E 1
recorder 1 hdf5 Eigen
step frequency 1 1
analyze
peek eigenvalue
exit
```

The output is

```
+--------------------------------------------------+
|   __        __        suanPan is an open source  |
|  /  \      |  \          FEM framework (64-bit)  |
|  \__       |__/  __   __          Acrux (0.1.0)  |
|     \ |  | |    |  \ |  |                        |
|  \__/ |__| |    |__X |  |     maintained by tlc  |
|                             all rights reserved  |
+--------------------------------------------------+

Eigenvalues:
   2.8680

Finished in 0.005 seconds.
```

## Storage and Solver Compatibility

| storage | commands | `system_solver` &rarr; matrix solver |
|---|---|---|
| full | `set symm_mat false`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gesv`<br>`CUDA` &rarr; `cusolverDnD(S)gesv` |
| symm. banded | `set symm_mat true`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)pbsv` |
| asymm. banded | `set symm_mat false`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gbsv`<br>`SPIKE` &rarr; `d(s)spike_gbtrf` + `d(s)spike_gbtrs`<br>`CUDA` &rarr; GPU SPIKE |
| symm. packed | `set symm_mat true`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)ppsv` |
| sparse | `set sparse_mat true` | `SuperLU` (default) &rarr; `d(s)gssv`<br>`CUDA` &rarr; `cusolverSpD(S)csrlsvqr`<br>`PARDISO` &rarr; `pardiso`<br>`FGMRES` &rarr; `dfgmres`<br>`MAGMA` &rarr; `magma_d(s)_solver` |

- Default solver: ARPACK. FEAST rejects symm. packed; asymmetric banded needs `SPIKE`; MPI FEAST needs sparse storage.
- Unsupported names are replaced by `LAPACK` (dense) or `SuperLU` (sparse); `LIS`/`MUMPS` are MPI-only.
- `CUDA`, `MAGMA`, `PARDISO` and `FGMRES` need build support; shipped binaries lack GPU support.
- Symm. banded/packed need a positive definite matrix.
- MPI: `pdgesv`/`pdpbsv`/`pdgbsv`/`pdposv` (dense), `cluster_sparse_solver`/`lis_solve`/`dmumps_c` (sparse).
