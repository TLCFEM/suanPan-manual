# LeeNewmarkFull

Newmark Algorithm With Lee Damping Model (Full Modes)

Please check the references for theory.

1. [10.1016/j.jsv.2020.115312](https://doi.org/10.1016/j.jsv.2020.115312)
2. [10.1016/j.engstruct.2020.110178](https://doi.org/10.1016/j.engstruct.2020.110178)
3. [10.1016/j.compstruc.2020.106423](https://doi.org/10.1016/j.compstruc.2020.106423)
4. [10.1016/j.compstruc.2021.106663](http://dx.doi.org/10.1016/j.compstruc.2021.106663)

**For the moment, MPC cannot be considered in all global damping models.**

## Syntax

```
integrator LeeNewmarkFull (1) (2) (3) ((4) (5) (6) [7...]...)
# (1) int, unique integrator tag
# (2) double, alpha in Newmark method
# (3) double, beta in Newmark method
# (4) string, type identifier
# (5) double, \zeta_p
# (6) double, \omega_p
# (7...) double/int, parameters associated with the mode
```

By default, the converged stiffness from the last substep is used in assembling damping matrix, this leads to quadratic
convergence rate. For special purposes, one can also use the following commands to explicitly use the certain stiffness
matrix.

```
integrator LeeNewmarkFullInitial (1) (2) (3) ((4) (5) (6) [7...]...)
integrator LeeNewmarkFullCurrent (1) (2) (3) ((4) (5) (6) [7...]...)
integrator LeeNewmarkFullTrial (1) (2) (3) ((4) (5) (6) [7...]...)
```

## Remarks

1. User shall ensure all active DoFs in the system are displacement DoFs.

2. The `LeeNewmarkFull` integrator uses a standard Newmark algorithm and the damping model proposed by Lee (2020).
   Several types of basic functions are defined to control the bandwidth.

3. The static condensation procedure is reversed so that the damping matrix $$\mathbf{C}$$ is a sparse matrix of a
   different size.

4. Currently, the modified equation of motion (of larger size) is stored as a sparse matrix and the `SuperLU` solver is
   used to solve sparse systems. To switch to other solver, one can use the following command.

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

5. The final global matrix is expected to be considerable huge compared to the original matrix. Thus, the sparse storage
   scheme is also used for assembling original stiffness and mass matrices by default. Please **always** add the
   following command in the corresponding step.

   ```
   set sparse_mat true
   ```

6. The following type identifiers are available:

   1. `-type0` --- zeroth order model, need no additional parameter, viz., `[7]` can be empty
   2. `-type1` --- type 1 model, need one integer parameter, viz., `[7]` ($$n_p$$) is a non-negative integer
   3. `-type2` --- type 2 model, need two integer parameters, viz., `[7]` ($$n_{pr}$$) and `[8]` ($$n_{pl}$$) are
      non-negative integers (**zero allowed**)
   4. `-type3` --- type 3 model, need a double parameter, viz., `[7]` ($$\gamma$$) is a double number that is greater 
      than $$\gamma>-1$$
   5. `-type4` --- type 4 model, need five parameters, `[7...10]` are four non-negative integers ($$n_{pr}$$,
      $$n_{pl}$$, $$n_{pk}$$, $$n_{pm}$$), `[11]` is a double parameter greater than $$\gamma>-1$$

7. Multiple types can be mixed in any preferred orders. See examples below.

## Examples

Each of the following commands defines $$5\%$$ peak damping on $$\omega=1$$ via different types with different
parameters.

```
integrator LeeNewmarkFull 1 .25 .5 -type0 .05 1
integrator LeeNewmarkFull 1 .25 .5 -type1 .05 1 2
integrator LeeNewmarkFull 1 .25 .5 -type2 .05 1 2 1
integrator LeeNewmarkFull 1 .25 .5 -type2 .05 1 3 1
integrator LeeNewmarkFull 1 .25 .5 -type2 .05 1 2 3
integrator LeeNewmarkFull 1 .25 .5 -type3 .05 1 -.25
integrator LeeNewmarkFull 1 .25 .5 -type3 .05 1 .5
integrator LeeNewmarkFull 1 .25 .5 -type3 .05 1 1 1 1 1 .5
integrator LeeNewmarkFull 1 .25 .5 -type3 .01 1 .5 -type2 .01 1 2 3 -type2 .01 1 2 1 -type0 .01 1 -type1 .01 1 2
```

With the above commands, we use $$\alpha=0.25$$ and $$\beta=0.5$$ in Newmark method. Users need to manually compute
$$\zeta_p$$, $$\omega_p$$ and other parameters to obtain desired curve.

There is no validation of input parameters. It is users' responsibility to ensure parameters are valid, and the
resulting curve is desired. Please refer to the references for customization of damping curves.

One can also use [Damping Dolphin](https://github.com/TLCFEM/damping-dolphin) to generate parameter sets.