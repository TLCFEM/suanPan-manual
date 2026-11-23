# solver

The `solver` command creates the nonlinear equation solver used in a step.
If a current step exists, the solver is assigned to it, and it also becomes the current solver.
Please refer to the specific solver pages for syntax and details.

## Syntax

```text title="solver"
solver (1) (2) ...
# (1) string, solver type
# (2) int, unique solver tag
```

## Remarks

1. Available types are `Newton`, `modifiedNewton` (alias `mNewton`), `AICN`, `BFGS`, `LBFGS`, `FEAST`, `QuadraticFEAST`, `DisplacementControl` (alias `MPDC`), and `Ramm`.
2. `AICN` accepts an optional length (default 1.0), and `LBFGS` an optional maximum history (default 20).
3. `FEAST` and `QuadraticFEAST` require a number of frequencies and a centre, with an optional radius that defaults to the centre.
4. See [Newton](../../Library/Solver/Newton.md), [AICN](../../Library/Solver/AICN.md), [BFGS](../../Library/Solver/BFGS.md), [MPDC](../../Library/Solver/MPDC.md), and [Ramm](../../Library/Solver/Ramm.md).
