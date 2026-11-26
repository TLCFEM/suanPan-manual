# Dynamic

## Implicit Dynamics System

The implicit dynamics system uses displacement as the primary variable.

### Syntax

```text title="Dynamic"
step dynamic (1) [2]
step implicitdynamic (1) [2]
# (1) int, unique step tag
# [2] double, time period, default: 1.0
```

### Remarks

1. Displacement control solver [`MPDC`](../Solver/MPDC.md) is automatically enabled if a displacement load is active.
2. The [`Newmark`](../Integrator/Implicit/Newmark/Newmark.md) is automatically enabled if there is no valid integrator defined.

## Explicit Dynamics System

The explicit dynamics system uses acceleration as the primary variable.

All displacement based loads/constraints cannot be applied.

### Syntax

```text title="Dynamic"
step explicitdynamic (1) [2]
# (1) int, unique step tag
# [2] double, time period, default: 1.0
```

### Remarks

1. The [`Tchamwa`](../Integrator/Explicit/Tchamwa.md) with spectral radius of $$0.8$$ is automatically enabled if there is no valid integrator defined.

## Storage and Solver Compatibility

| storage | commands | `system_solver` &rarr; matrix solver |
|---|---|---|
| full | `set symm_mat false`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gesv`<br>`CUDA` &rarr; `cusolverDnD(S)gesv` |
| symm. banded | `set symm_mat true`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)pbsv` |
| asymm. banded | `set symm_mat false`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` (default) &rarr; `d(s)gbsv`<br>`SPIKE` &rarr; `d(s)spike_gbtrf` + `d(s)spike_gbtrs`<br>`CUDA` &rarr; GPU SPIKE |
| symm. packed | `set symm_mat true`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)ppsv` |
| sparse | `set sparse_mat true` | `SuperLU` (default) &rarr; `d(s)gssv`<br>`CUDA` &rarr; `cusolverSpD(S)csrlsvqr`<br>`PARDISO` &rarr; `pardiso`<br>`FGMRES` &rarr; `dfgmres`<br>`MAGMA` &rarr; `magma_d(s)_solver` |

- Defaults: `Newmark` (implicit) or `Tchamwa` (explicit); solver `Newton`, or `MPDC` with a displacement load.
- `Ramm` is discarded; `BFGS` fails with Lee damping. Explicit steps warn on displacement loads.
- Auxiliary systems use `set sub_system_solver`.
- Unsupported names are replaced by `LAPACK` (dense) or `SuperLU` (sparse); `LIS`/`MUMPS` are MPI-only.
- `CUDA`, `MAGMA`, `PARDISO` and `FGMRES` need build support; shipped binaries lack GPU support.
- Symm. banded/packed need a positive definite matrix.
- MPI: `pdgesv`/`pdpbsv`/`pdgbsv`/`pdposv` (dense), `cluster_sparse_solver`/`lis_solve`/`dmumps_c` (sparse).
