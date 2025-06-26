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

1. The definition of parameters is **identical** to that of [`LeeNewmarkFull`](LeeNewmarkFull.md).
2. Instead of unrolling all modes into a single sparse damping matrix, this integrator uses an iterative procedure to
   solve system. The convergence rate is **linear**.
3. Since the convergence rate is linear even with [`Newton`](../../../Solver/Newton.md) method, one may use
   the [`(L)BFGS`](../../../Solver/BFGS.md) method to achieve a super-linear convergence rate.

The damping force is obtained via matrix operations, which include matrix inversion. In this phase, some sparse matrices
will be formed, to control what solver to be used to solve sparse matrix, one can set the subsystem solver via the
following commands.

```text
set sub_system_solver MUMPS
set sub_system_solver SuperLU
set sub_system_solver PARDISO ! if MKL is available
set sub_system_solver FGMRES ! if MKL is available
set sub_system_solver CUDA ! if CUDA is available
# currently no iterative solver is available
```

It is recommended to use a dense matrix storage for the system with a [`(L)BFGS`](../../../Solver/BFGS.md) solver. This
configuration can maximize the performance.
For example,

```text
step dynamic 1 10
solver LBFGS 1 50
# the following are the default
set banded_mat true
set symm_mat false
set sparse_mat false
set system_solver SPIKE
set sub_system_solver SuperLU

integrator LeeNewmarkIterative 1 .25 .5 ...
```

The above configuration uses a dense banded asymmetric matrix to store the system matrix. The equation of motion will be solved via the SPIKE solver.
For damping force computation, the relevant sparse matrices will be solved by the SuperLU solver.
