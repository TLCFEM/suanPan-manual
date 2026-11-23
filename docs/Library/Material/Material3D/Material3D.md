# Material3D

All 3D material models support the following basic output types.

| variable label | physical meaning                        |
|----------------|-----------------------------------------|
| SP             | all principal stress components         |
| EP             | all principal strain components         |
| EEP            | all principal elastic strain components |
| PEP            | all principal plastic strain components |
| EEQ            | equivalent strain                       |
| EEEQ           | equivalent elastic strain               |
| PEEQ           | equivalent plastic strain               |
| HYDRO          | hydrostatic stress                      |
| MISES          | von Mises stress                        |

Depending on the specific material model, additional output types may be available.

## Background

A three-dimensional material receives the six-component Voigt vector $\boldsymbol\varepsilon=(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{23},\gamma_{13},\gamma_{12})^{\mathrm T}$ and returns $\boldsymbol\sigma=(\sigma_{11},\sigma_{22},\sigma_{33},\tau_{23},\tau_{13},\tau_{12})^{\mathrm T}$.
The last three entries are engineering shear strains and stresses, with $\gamma_{ij}=2\varepsilon_{ij}$ for $i\neq j$, which makes the elasticity matrix symmetric.
For isotropic linear elasticity $\boldsymbol\sigma=2G\boldsymbol\varepsilon+\lambda\,\mathrm{tr}(\boldsymbol\varepsilon)\boldsymbol I$ with $G=E/[2(1+\nu)]$ and $\lambda=E\nu/[(1+\nu)(1-2\nu)]$.
Elastoplastic and damage models split the strain additively, $\boldsymbol\varepsilon=\boldsymbol\varepsilon^e+\boldsymbol\varepsilon^p$, and use a return-mapping algorithm to enforce the yield or damage condition at the end of each step.
The algorithmic tangent returned by `trial_stiffness` must be the derivative of the converged stress update, otherwise the global Newton iteration loses its quadratic convergence.

The derived recorder quantities are defined from the committed stress and strain.
`SP` and `EP` are the eigenvalues of the stress and strain tensors, obtained by reshaping the Voigt vectors into symmetric second-order tensors.
`EE` and `PE` are computed by solving $\boldsymbol\varepsilon^e=\mathbf D_0^{-1}\boldsymbol\sigma$ and $\boldsymbol\varepsilon^p=\boldsymbol\varepsilon-\boldsymbol\varepsilon^e$ with the initial elastic stiffness.
`EEQ`, `EEEQ` and `PEEQ` are the von Mises norms $\sqrt{2/3\,\boldsymbol e:\boldsymbol e}$ of the total, elastic and plastic strain deviators.
`HYDRO` is the mean stress $\sigma_{kk}/3$ and `MISES` is $\sqrt{3/2\,\boldsymbol s:\boldsymbol s}$ with $\boldsymbol s=\operatorname{dev}\boldsymbol\sigma$.

!!! warning "implementation limitation"
    The elastic and plastic strain outputs use the initial stiffness matrix, not the current elastic operator.
    They identify with the true elastic and plastic strains only when elasticity is linear and the strain decomposition is additive, and they are approximate for logarithmic or pressure-dependent elasticity.

!!! info "deviation from theory"
    Stresses are tension-positive, so `HYDRO` is negative in compression and equals $-\sigma'$ for the effective mean stress used in soil mechanics.
    The von Mises norm and the principal values are unaffected by this sign convention, but comparisons with soil-mechanics $p'$ and $q$ must change sign.

A material update is committed with `commit_status()` and restored with `reset_status()`, and the history vector is part of the committed state.
The base class also supports `HIST`, the raw history vector, and `YF`, which is one if any history entry is non-zero.

!!! info "deviation from theory"
    `YF` is not the value of a yield function and does not indicate that the current step was plastic.
    It is a history-activity flag that remains one for the rest of the analysis once any history variable has become non-zero.

Use three-dimensional solid elements such as [C3D8](../../Element/Cube/C3D8.md) or [C3D8I](../../Element/Cube/C3D8I.md), and reduce integration or use mixed elements when $\nu$ approaches $0.5$.
Pressure-dependent and damage models often return a non-symmetric consistent tangent, so `set symm_mat 0` is required in those analyses.
To embed a three-dimensional material in a two-dimensional problem, use the [`PlaneStrain`](../Wrapper/PlaneStrain.md) or [`Axisymmetric`](../Wrapper/Axisymmetric.md) wrapper rather than a native 2D model.

## References

1. [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
2. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
