# Dynamic

## Syntax

```
step dynamic (1) (2)
# (1) int, unique step tag
# (2) double, step size
```

## Remarks

1. Displacement control solver [`MPDC`](../Solver/MPDC.md) is automatically enabled if a displacement load is active.
2. The [`Newmark`](../Integrator/Newmark/Newmark.md) is automatically enabled if there is no valid integrator defined.