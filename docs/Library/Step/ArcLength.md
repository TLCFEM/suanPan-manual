# ArcLength

## Background

Arc-length control follows a nonlinear equilibrium path by treating the load level as an additional unknown.
It can trace post-peak and snap-back responses that ordinary force control cannot pass.
A [`Criterion`](../Criterion/Criterion.md) governs the path by issuing an exit flag when a target response is reached.

## Syntax

### Prior to v3.2.0

For versions prior to v3.2.0, the syntax is as follows.
Only one single DoF is permitted to be controlled.
It is directly defined in the step command.

```text title="ArcLength"
step ArcLength (1) (2) (3) (4)
# (1) int, unique step tag
# (2) int, reference node tag
# (3) int, reference dof tag
# (4) double, reference magnitude of applied load
```

### v3.2.0 and later

For versions v3.2.0 and later, the syntax is as follows.
The reference load is no longer defined in the step command.
Instead, it is defined by the [`RefForce`](../../Collection/Define/load.md) command.

```text
step ArcLength (1)
# (1) int, unique step tag
```

## Arc-length Control

The step size in an arc-length analysis is now the arc length.
One can use the following to control stepping strategy.

```
set ini_step_size (1)
set min_step_size (1)
set max_step_size (1)
# (1) double, step size (arc length)

set fixed_step_size (1)
# (1) bool, flag to indicate whether to fix the arc length
```

## Remarks

1. A [`Ramm`](../Solver/Ramm.md) solver with default parameters is automatically enabled if no valid `Ramm` solver is defined.
   Not all storage schemes are supported; please check `Ramm` documentation.
2. Distributed computation is not supported.

## Storage and Solver Compatibility

| storage | commands | `system_solver` &rarr; matrix solver |
|---|---|---|
| full | `set symm_mat false`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)gesv` |
| symm. banded | `set symm_mat true`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)pbsv` |
| asymm. banded | `set symm_mat false`<br>`set band_mat true`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)gbsv`<br>`SPIKE` &rarr; `d(s)spike_gbtrf` + `d(s)spike_gbtrs`<br>`CUDA` &rarr; GPU SPIKE |
| symm. packed | `set symm_mat true`<br>`set band_mat false`<br>`set sparse_mat false` | `LAPACK` &rarr; `d(s)ppsv` |
| sparse | `set sparse_mat true` | `SuperLU` &rarr; `d(s)gssv` |

- `Ramm` is forced; it needs `sign_det()`.
- `sign_det()` is implemented by dense LAPACK containers and banded SPIKE/CUDA containers, not by `SparseMatSuperLU`.
- `CUDA` is reset to `LAPACK` outside banded storage; any sparse solver name is reset to `SuperLU`.
- Symm. storage reports a positive determinant sign and needs a positive definite tangent.
- Distributed builds are rejected by `ArcLength::initialize()`.
