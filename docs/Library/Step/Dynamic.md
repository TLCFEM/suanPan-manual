# Dynamic

## Implicit Dynamics System

The implicit dynamics system uses displacement as the primary variable.

### Syntax

```
step dynamic (1) (2)
step implicitdynamic (1) (2)
# (1) int, unique step tag
# (2) double, step size
```

### Remarks

1. Displacement control solver [`MPDC`](../Solver/MPDC.md) is automatically enabled if a displacement load is active.
2. The [`Newmark`](../Integrator/Implicit/Newmark/Newmark.md) is automatically enabled if there is no valid integrator defined.

## Explicit Dynamics System

The explicit dynamics system uses acceleration as the primary variable.

All displacement based loads/constraints cannot be not applied.

### Syntax

```
step explicitdynamic (1) (2)
# (1) int, unique step tag
# (2) double, step size
```

### Remarks

1. The [`Tchamwa`](../Integrator/Explicit/Tchamwa.md) with spectral radius of $$0.8$$ is automatically enabled if there is no
   valid integrator defined.
