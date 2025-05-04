# BFGS

The `BFGS` solver uses the rank two update algorithm BFGS.
Alternatively, the limited memory version can also be switched on.

## Reference

The implementation is based on Algorithm 7.4.

1. [Numerical Optimization](https://doi.org/10.1007/978-0-387-40065-5)

## Syntax

```
solver BFGS (1)
solver LBFGS (1) [2]
# (1) int, unique solver tag
# [2] int, number of steps stored, default: 20
```

## Details and Limitations

The global stiffness matrix is assembled in the very first iteration of each sub-step.
Subsequent iterations use this matrix as the initial Hessian.

Since BFGS possesses a super-linear convergence rate, the overall performance should be better than that of the modified Newton method.

Regardless of whether LBFGS is used, the maximum number of iterations will be limited to the size of the problem.

There is no support for constraints implemented via the Lagrange multiplier method.
