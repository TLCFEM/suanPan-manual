# Static

To define a static analysis, the `Static` step shall be used.

```
step static (1) [2]
# (1) int, unique step tag
# [2] double, step length, default: 1.0
```

## Remarks

1. Unlike `ABAQUS`, all time lengths defined are absolute time.
   There is no so-called "step time", which is related to some normalized time concept in `ABAQUS`.
2. The `Static` step supports all matrix storage schemes.
3. Displacement control solver [`MPDC`](../Solver/MPDC.md) is automatically enabled if a displacement load is active.

## Storage and Solver Compatibility

| storage | commands | `system_solver` &rarr; matrix solver |
|---|---|---|
| full | `set symm_mat false`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gesv`<br>`CUDA` &rarr; `cusolverDnD(S)gesv` |
| symm. banded | `set symm_mat true`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)pbsv` |
| asymm. banded | `set symm_mat false`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gbsv`<br>`SPIKE` &rarr; `d(s)spike_gbtrf` + `d(s)spike_gbtrs`<br>`CUDA` &rarr; GPU SPIKE |
| symm. packed | `set symm_mat true`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)ppsv` |
| sparse | `set sparse_mat true` | `SuperLU` (default) &rarr; `d(s)gssv`<br>`CUDA` &rarr; `cusolverSpD(S)csrlsvqr`<br>`PARDISO` &rarr; `pardiso`<br>`FGMRES` &rarr; `dfgmres`<br>`MAGMA` &rarr; `magma_d(s)_solver` |

- Default solver: `Newton`, or `MPDC` with an active displacement load.
- Unsupported names are replaced by `LAPACK` (dense) or `SuperLU` (sparse); `LIS`/`MUMPS` are MPI-only.
- `CUDA`, `MAGMA`, `PARDISO` and `FGMRES` need build support; shipped binaries lack GPU support.
- Symm. banded/packed need a positive definite matrix.
- MPI: `pdgesv`/`pdpbsv`/`pdgbsv`/`pdposv` (dense), `cluster_sparse_solver`/`lis_solve`/`dmumps_c` (sparse).
