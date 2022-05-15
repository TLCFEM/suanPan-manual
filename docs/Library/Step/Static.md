# Static

To define a static analysis, the `Static` step shall be used.

```
step static (1) [2]
# (1) int, unique step tag
# [2] double, step length, default: 1.0
```

## Remarks

1. Unlike `ABAQUS`, all time lengths defined are absolute time. There is no so-called "step time", which is related to
   some normalized time concept in `ABAQUS`.
2. The `Static` step supports all matrix storage schemes.
3. Displacement control solver [`MPDC`](../Solver/MPDC.md) is automatically enabled if a displacement load is active.
