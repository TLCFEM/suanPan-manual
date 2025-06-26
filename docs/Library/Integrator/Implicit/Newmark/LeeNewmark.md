# LeeNewmark

Newmark Algorithm With Lee Damping Model (Type 0 Only)

See this [example](../../../../Example/Structural/Dynamics/response-history-analysis-of-an-elastic-coupled-wall.md).

Please check the references for theory.

1. [10.1016/j.jsv.2020.115312](https://doi.org/10.1016/j.jsv.2020.115312)
2. [10.1016/j.engstruct.2020.110178](https://doi.org/10.1016/j.engstruct.2020.110178)

**For the moment, MPC cannot be considered in all global damping models.**

## Syntax

```
integrator LeeNewmark (1) (2) (3) ((4) (5)...)
# (1) int, unique integrator tag
# (2) double, alpha
# (3) double, beta
# (4) double, damping ratio \zeta_p at the peak of each mode
# (5) double, circular frequency \omega_p at the peak of each mode
```

The converged stiffness from the last substep is used for assembling. If other stiffness matrices are preferred, please
use [`LeeNewmarkFull`](LeeNewmarkFull.md).

## Remarks

1. User shall make sure all active DoFs in the system are displacement DoFs.

2. The `LeeNewmark` integrator uses a standard Newmark algorithm and the damping model proposed by Lee (2020).

3. The static condensation procedure is reversed so that the damping matrix $$\mathbf{C}$$ is a sparse matrix of a
   different size.

4. Currently, the modified equation of motion (of larger size) is stored as a sparse matrix and the `SuperLU` solver is
   used to solve sparse systems by default. To switch to other solver, one can use the following command.

    ```
    set system_solver MUMPS
    ```

   If `MKL` is enabled, it is possible to use `PARDISO` solver by setting the following command.

    ```
    set system_solver PARDISO
    ```

   If `CUDA` is enabled, it is possible to use `CUDA` solver by setting the following command.

    ```
    set system_solver CUDA
    ```

   The matrix storage flags (`sparse_mat`, `band_mat`, `symm_mat`) still have effect on how original matrices are stored
   but do not affect solving stage. Depending on different storage schemes (dense/sparse), the assembly of final
   effective stiffness may have different efficiency. For large systems, it may potentially be faster if original
   matrices adopt sparse scheme as well. To do so, one can use the following command.

    ```
    set sparse_mat true
    ```

5. Experience indicates that different sparse solvers may exhibit different performance. You are suggested to test
   different solvers on your platform.

## Example

The following command adopts three basic functions with peaks located at $$\omega_1=1$$, $$\omega_2=10$$ and
$$\omega_3=100$$. Each basic function has a peak of $$3\%$$ damping.

```
integrator LeeNewmark 1 .25 .5 .03 1 .03 10 .03 100
```

With the above command, we use $$\alpha=0.25$$ and $$\beta=0.5$$ in Newmark method. Note the final overall response will
be something greater than $$3\%$$ at those three frequencies since the contributions of three functions will be summed.
Users need to manually compute $$\zeta_p$$ and $$\omega_p$$ to obtain desired curve.

One can also use [Damping Dolphin](https://github.com/TLCFEM/damping-dolphin) to generate parameter sets.
