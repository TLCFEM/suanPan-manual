# LeeNewmarkIterative

## Syntax

```
integrator LeeNewmarkIterative (1) (2) (3) ((4) (5) (6) [7...]...)
# (1) int, unique integrator tag
# (2) double, alpha in Newmark method
# (3) double, beta in Newmark method
# (4) string, type identifier
# (5) double, \zeta_p
# (6) double, \omega_p
# (7...) double/int, parameters associated with the mode
```

## Remarks

1. The definition of parameters is **identical** to  [`LeeNewmarkFull`](LeeNewmarkFull.md).
2. Instead of unrolling all modes into a single sparse damping matrix, this integrator uses an iterative procedure to
   solve system. The convergence rate is **linear**.
3. Since the convergence rate is linear even with [`Newton`](../../Solver/Newton.md) method, one may use
   the [`(L)BFGS`](../../Solver/BFGS.md) method to achieve a super-linear convergence rate.
