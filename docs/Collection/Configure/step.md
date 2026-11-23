# step

The `step` command defines an analysis step.
Please refer to the specific step types for syntax and details.

## Syntax

```text title="step"
step (1) (2) ...
# (1) string, step type
# (2) int, unique step tag
```

For all available steps, a default **asymmetric banded** dense storage is used.
This storage scheme fits most problems.
The LAPACK driver used is `_gbsv()`.
The main reason behind this choice stems from two aspects.

1. For 2D and 3D problems, most material models have asymmetric stiffness moduli.
   The global stiffness matrix is then asymmetric.
2. If the problem shows softening behaviour, the stiffness matrix is not always positive definite.
   The symmetric solver then fails to solve such a matrix.
