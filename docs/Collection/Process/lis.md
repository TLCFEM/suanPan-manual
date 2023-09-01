# Iterative Solver

[available from v3.1]

To use iterative solvers, one shall use the following settings:

```text
set sparse_mat true
set system_solver lis [1]
# [1] string, lis solver options
```

The [`Lis`](https://www.ssisc.org/lis/) library is used to provide the functionality.

Please note that although `Lis` provides a wide variety of iterative solvers and preconditioners, not all would yield a
good performance.
Whether it is faster than direct solvers depends on different problems.

All possible options, which are copied directly from `Lis` documentation, are listed below.

For example, if one wants to use the `BiCGSTAB` solver with `ILU(2)` preconditioner, and wants to print statistics, the
settings would be:

```text
set sparse_mat true
set system_solver lis -i bicgstab -p ilu -ilu_fill 2 -print out
```

## Solver Related Options

| Solver       | Option              | Auxiliary Options |                             |
|--------------|---------------------|-------------------|-----------------------------|
| CG           | `-i {cg\|1}`        |                   |                             |
| BiCG         | `-i {bicg\|2}`      |                   |                             |
| CGS          | `-i {cgs\|3}`       |                   |                             |
| BiCGSTAB     | `-i {bicgstab\|4}`  |                   |                             |
| BiCGSTAB(l)  | `-i {bicgstabl\|5}` | `-ell [2]`        | The degree $$l$$            |
| GPBiCG       | `-i {gpbicg\|6}`    |                   |                             |
| TFQMR        | `-i {tfqmr\|7}`     |                   |                             |
| Orthomin(m)  | `-i {orthomin\|8}`  | `-restart [40]`   | The restart value $$m$$     |
| GMRES(m)     | `-i {gmres\|9}`     | `-restart [40]`   | The restart value $$m$$     |
| Jacobi       | `-i {jacobi\|10}`   |                   |                             |
| Gauss-Seidel | `-i {gs\|11}`       |                   |                             |
| SOR          | `-i {sor\|12}`      | `-omega [1.9]`    | The relaxation coefficient  |
|              |                     |                   | $$\omega$$ ($$0<\omega<2$$) |
| BiCGSafe     | `-i {bicgsafe\|13}` |                   |                             |
| CR           | `-i {cr\|14}`       |                   |                             |
| BiCR         | `-i {bicr\|15}`     |                   |                             |
| CRS          | `-i {crs\|16}`      |                   |                             |
| BiCRSTAB     | `-i {bicrstab\|17}` |                   |                             |
| GPBiCR       | `-i {gpbicr\|18}`   |                   |                             |
| BiCRSafe     | `-i {bicrsafe\|19}` |                   |                             |
| FGMRES(m)    | `-i {fgmres\|20}`   | `-restart [40]`   | The restart value $$m$$     |
| IDR(s)       | `-i {idrs\|21}`     | `-irestart [2]`   | The restart value $$s$$     |
| IDR(1)       | `-i {idr1\|22}`     |                   |                             |
| MINRES       | `-i {minres\|23}`   |                   |                             |
| COCG         | `-i {cocg\|24}`     |                   |                             |
| COCR         | `-i {cocr\|25}`     |                   |                             |

## Preconditioner Related Options

| Preconditioner | Option           | Auxiliary Options           |                                                                   | 
|----------------|------------------|-----------------------------|-------------------------------------------------------------------|
| None           | `-p {none\|0}`   |                             |                                                                   |
| Jacobi         | `-p {jacobi\|1}` |                             |                                                                   |
| ILU(k)         | `-p {ilu\|2}`    | `-ilu_fill [0]`             | The fill level $$k$$                                              |
| SSOR           | `-p {ssor\|3}`   | `-ssor_omega [1.0]`         | The relaxation coefficient $$\omega$$ ($$0<\omega<2$$)            |
| Hybrid         | `-p {hybrid\|4}` | `-hybrid_i [sor]`           | The linear solver                                                 |
|                |                  | `-hybrid_maxiter [25]`      | The maximum number of iterations                                  |
|                |                  | `-hybrid_tol [1.0e-3]`      | The convergence tolerance                                         |
|                |                  | `-hybrid_omega [1.5]`       | The relaxation coefficient $$\omega$$ of the SOR ($$0<\omega<2$$) |
|                |                  | `-hybrid_ell [2]`           | The degree $$l$$ of the BiCGSTAB(l)                               |
|                |                  | `-hybrid_restart [40]`      | The restart values of the GMRES and Orthomin                      |
| I+S            | `-p {is\|5}`     | `-is_alpha [1.0]`           | The parameter $$\alpha$$ of $$I+\alpha S^{(m)}$$                  |
|                |                  | `-is_m [3]`                 | The parameter $$m$$ of $$I+\alpha S^{(m)}$$                       |
| SAINV          | `-p {sainv\|6}`  | `-sainv_drop [0.05]`        | The drop criterion                                                |
| SA-AMG         | `-p {saamg\|7}`  | `-saamg_unsym [false]`      | Select the unsymmetric version                                    |
|                |                  |                             | (The matrix structure must be                                     |
|                |                  |                             | symmetric)                                                        |
|                |                  | `-saamg_theta [0.05\|0.12]` | The drop criterion $$a^2_{ij}\le\theta^2\|a_{ii}\|\|a_{jj}\|$$    |
|                |                  |                             | (symmetric or unsymmetric)                                        |
| Crout ILU      | `-p {iluc\|8}`   | `-iluc_drop [0.05]`         | The drop criterion                                                |
|                |                  | `-iluc_rate [5.0]`          | The ratio of the maximum fill-in                                  |
| ILUT           | `-p {ilut\|9}`   |                             |                                                                   |
| Additive       | `-adds true`     | `-adds_iter [1]`            | The number of iterations                                          |
| Schwarz        |                  |                             |                                                                   |

## Other Options

| Option                 |                                                                                                                                                                       | 
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-maxiter [1000]`      | The maximum number of iterations                                                                                                                                      |
| `-tol [1.0e-12]`       | The convergence tolerance $$tol$$                                                                                                                                     |
| `-tol_w [1.0]`         | The convergence tolerance $$tol_w$$                                                                                                                                   |
| `-print [0]`           | The output of the residual history                                                                                                                                    |
|                        | `-print {none\|0}`  None                                                                                                                                              |
|                        | `-print {mem\|1}`  Save the residual history                                                                                                                          |
|                        | `-print {out\|2}`  Output it to the standard output                                                                                                                   |
|                        | `-print {all\|3}`  Save the residual history and output it to the standard output                                                                                     |
| `-scale [0]`           | The scaling                                                                                                                                                           |
|                        | (The result will overwrite the original matrix and vectors)                                                                                                           |
|                        | `-scale {none\|0}`  No scaling                                                                                                                                        |
|                        | `-scale {jacobi\|1}`  The Jacobi scaling $$D^{-1}Ax=D^{-1}b$$ ($$D$$ represents the diagonal of $$A=(a_{ij})$$)                                                       |
|                        | `-scale {symm_diag\|2}`  The diagonal scaling $$D^{-1/2}AD^{-1/2}x=D^{-1/2}b$$ ($$D^{-1/2}$$ represents the diagonal matrix with $$1/\sqrt{a_{ii}}$$ as the diagonal) |
| `-initx_zeros [1]`     | The behavior of the initial vector $$x_{0}$$                                                                                                                          |
|                        | `-initx_zeros {false\|0}`  The components are given by the argument `x` of the function `lis_solve()`                                                                 |
|                        | `-initx_zeros {true\|1}`  All the components are set to $$0$$                                                                                                         |
| `-conv_cond [0]`       | The convergence condition                                                                                                                                             |
|                        | `-conv_cond {nrm2_r\|0}`  $$\|\|b-Ax\|\|_2 \le tol * \|\|b-Ax_0\|\|_2$$                                                                                               |
|                        | `-conv_cond {nrm2_b\|1}`  $$\|\|b-Ax\|\|_2 \le tol * \|\|b\|\|_2$$                                                                                                    |
|                        | `-conv_cond {nrm1_b\|2}`  $$\|\|b-Ax\|\|_1 \le tol_w * \|\|b\|\|_1 + tol$$                                                                                            |
| `-omp_num_threads [t]` | The number of threads (`t` represents the maximum number of threads)                                                                                                  |
| `-storage [0]`         | The matrix storage format                                                                                                                                             |
| `-storage_block [2]`   | The block size of the BSR and BSC formats                                                                                                                             |
| `-f [0]`               | The precision of the linear solver                                                                                                                                    |
|                        | `-f {double\|0}`  Double precision                                                                                                                                    |
|                        | `-f {quad\|1}`  Double-double (quadruple) precision                                                                                                                   |
