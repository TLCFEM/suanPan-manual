# Newton

The `Newton` solver defines a classic (modified) Newton-Raphson solver.

## Syntax

```
solver Newton (1)
solver modifiedNewton (1)
solver mNewton (1)
# (1) int, unique solver tag
```

## Remarks

1. The modified Newton method only assembles tangent stiffness at the beginning of each sub-step. Automatic stepping can
   be enabled to obtain optimised computational workload.
2. The Aitken acceleration is automatically enabled in the modified Newton method.
