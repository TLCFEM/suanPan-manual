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
