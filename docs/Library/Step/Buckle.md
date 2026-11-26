# Buckle

The `Buckle` step defines a linear buckling analysis.

## Background

A `Buckle` step first runs a single-increment static analysis to obtain the stressed state.
It then solves a generalised eigenproblem formed by the current stiffness matrix and the negative geometric (initial-stress) matrix.
The reported buckling load multiplier scales the applied load to the critical state.

## Syntax

```text title="Buckle"
step Buckle (1)
step Buckling (1)
# (1) int, unique step tag
```

## Remarks

The analysis requires an active nonlinear geometry (`nlgeom`) model, otherwise it fails with an error.
By default it uses an [`AbsIncreDisp`](../Converger/Absolute/AbsIncreDisp.md) converger, the plain integrator and a [`Newton`](../Solver/Newton.md) solver.
Not every buckling solver supports distributed computation; some run the analysis independently on each node.

## Example

```text
element B21 1 1 2 1 6 1
# ... other elements, supports and load ...
cload 1 0 -1E-2 1 6

step Buckle 1
set symm_mat 0
analyze
```

See `Example/Solver/Buckle2.supan` in the source tree for a complete model.

## Storage and Solver Compatibility

| storage | commands | `system_solver` &rarr; matrix solver |
|---|---|---|
| full | `set symm_mat false`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gesv`<br>`CUDA` &rarr; `cusolverDnD(S)gesv` |
| symm. banded | `set symm_mat true`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)pbsv` |
| asymm. banded | `set symm_mat false`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gbsv`<br>`SPIKE` &rarr; `d(s)spike_gbtrf` + `d(s)spike_gbtrs`<br>`CUDA` &rarr; GPU SPIKE |
| symm. packed | `set symm_mat true`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)ppsv` |
| sparse | `set sparse_mat true` | `SuperLU` (default) &rarr; `d(s)gssv`<br>`CUDA` &rarr; `cusolverSpD(S)csrlsvqr`<br>`PARDISO` &rarr; `pardiso`<br>`FGMRES` &rarr; `dfgmres`<br>`MAGMA` &rarr; `magma_d(s)_solver` |

- Requires `nlgeom`. ARPACK solves the `K - G` system in shift-and-invert mode with the matrix solver above.
- Use `set symm_mat 0` for the indefinite tangent.
- Unsupported names are replaced by `LAPACK` (dense) or `SuperLU` (sparse); `LIS`/`MUMPS` are MPI-only.
- `CUDA`, `MAGMA`, `PARDISO` and `FGMRES` need build support; shipped binaries lack GPU support.
- Symm. banded/packed need a positive definite matrix.
- MPI: `pdgesv`/`pdpbsv`/`pdgbsv`/`pdposv` (dense), `cluster_sparse_solver`/`lis_solve`/`dmumps_c` (sparse).
