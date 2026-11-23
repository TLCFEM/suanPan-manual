# LinearDamage

Linear Damage Degradation With Cut-offs

The `LinearDamage` model wraps a three-dimensional host material and degrades its stress and stiffness by a scalar factor that grows linearly with a strain measure.

## Background

Isotropic damage mechanics introduces a scalar variable that reduces the stiffness of a material while preserving the direction of the response.
In the effective-stress formulation of Kachanov and Rabotnov, the intact stress $\bar{\boldsymbol\sigma}$ acts on the undamaged area, and the Cauchy stress is $\boldsymbol\sigma=(1-\omega)\bar{\boldsymbol\sigma}$ with $\omega$ the damage variable.
This implementation instead works with the survival factor $d=1-\omega$, so that $d=1$ denotes the intact state and a smaller value denotes degradation.
The evolution of damage is driven by an equivalent strain, and irreversibility is enforced by storing the maximum value ever reached as a history variable.
A linear evolution law between a start strain and an end strain is the simplest regularisation of experimental softening curves and needs only three parameters in addition to the host material.

## Syntax

```text title="LinearDamage"
material LinearDamage (1) (2) (3) (4) [5]
# (1) int, unique material tag
# (2) int, associated material tag
# (3) double, start strain
# (4) double, end strain
# [5] double, end damage value, default: 0.0
```

## Theory

In this model, the equivalent total strain is used to characterize the damage development, namely, $$d=f(\varepsilon_{eq})$$.
Then the final response is defined as

$$
\mathbf\sigma=d\mathbf{\bar\sigma},
$$

where $$\mathbf{\bar\sigma}$$ is the intact stress response of the associated material model.

!!! info "deviation from theory"
    The symbol $d$ is a remaining-stiffness factor, not the damage variable $\omega$ of classical continuum damage mechanics.
    The two are related by $d=1-\omega$, and the input called "end damage value" is the residual factor at saturation, not a damage fraction.

The final stiffness can be derived as

$$
\mathbf{K}=\dfrac{\mathrm{d}\mathbf{\sigma}}{\mathrm{d}\mathbf{\varepsilon}}=\dfrac{\mathrm{d}\mathbf{\bar\sigma}}{\mathrm{d}\mathbf{\varepsilon}}d+\mathbf{\bar\sigma}\otimes\dfrac{\mathrm{d}d}{\mathrm{d}\mathbf{\varepsilon}}=\mathbf{\bar{K}}d+\mathbf{\bar\sigma}\otimes\dfrac{\mathrm{d}d}{\mathrm{d}\mathbf{\varepsilon}}.
$$

The source uses the von Mises norm of the deviatoric strain as the damage-driving measure,
$$
\varepsilon_{eq}=\sqrt{\dfrac{2}{3}\,\mathbf e:\mathbf e},\qquad \mathbf e=\operatorname{dev}\boldsymbol\varepsilon,
$$
with engineering shear entries weighted by the usual Voigt factors.
The factor is then
$$
d=\begin{cases}
1,&\varepsilon_{eq}\leq\varepsilon_s,\\
1+\dfrac{1-d_e}{\varepsilon_s-\varepsilon_e}(\varepsilon_{eq}-\varepsilon_s),&\varepsilon_s<\varepsilon_{eq}<\varepsilon_e,\\
d_e,&\varepsilon_{eq}\geq\varepsilon_e,
\end{cases}
$$
where $\varepsilon_s$ and $\varepsilon_e$ are the start and end strains and $d_e$ is the end damage value.
The stored history variable is $\kappa=\max\varepsilon_{eq}$, so the factor is evaluated at the current maximum and never increases back towards one during unloading.
Inside the linear branch the derivative required by the tangent is $\partial d/\partial\boldsymbol\varepsilon=\mathrm{slope}\,\mathbf W\mathbf e/(1.5\,\varepsilon_{eq})$, where $\mathbf W$ contains the Voigt weights and $\mathrm{slope}=(1-d_e)/(\varepsilon_s-\varepsilon_e)$.

!!! warning "implementation limitation"
    The equivalent strain contains only the deviatoric part of the strain, so hydrostatic compression alone cannot initiate damage.
    Many quasi-brittle damage models use a positive-part or energy-based equivalent strain that is sensitive to tensile hydrostatic stress, which is not available here.

!!! warning "implementation limitation"
    The outer product $\bar{\boldsymbol\sigma}\otimes\partial d/\partial\boldsymbol\varepsilon$ makes the consistent tangent non-symmetric.
    The shipped example therefore uses `set symm_mat 0`, and using a symmetric solver assumption can prevent convergence.

## Remarks

* `(2)` is the tag of the three-dimensional host material, `(3)` is the strain at which degradation starts, and `(4)` is the strain at which it saturates.
* `(5)` is the residual stress and stiffness factor at saturation, with a default of zero meaning complete loss of load-carrying capacity.
* All three damage parameters are stored without sign conversion, so $\varepsilon_s<\varepsilon_e$ must be supplied for a decreasing factor.
* The damage factor is stored in `HIST` through the base class history mechanism, which records $\kappa$ rather than the current factor directly.
* Unloading follows the degraded stiffness, so no stiffness recovery due to crack closure is represented.
* Damage is local and unregularised, so computed energy dissipation depends on element size in strain-softening problems.
* Use three-dimensional solid elements such as [C3D8](../../../Element/Cube/C3D8.md) with `PlaneStrain` or `Axisymmetric` wrappers only if the host material is compatible with the wrapper.

## References

1. Kachanov, L. M. (1958), "On the Time to Failure under Creep Conditions", Izvestiya Akad. Nauk SSSR, Otd. Tekh. Nauk, 8, 26--31.
2. Rabotnov, Y. N. (1963), "Creep Problems in Structural Members", North-Holland, Amsterdam.
3. Lemaitre, J. and Chaboche, J.-L. (1990), "Mechanics of Solid Materials", Cambridge University Press.
4. Mazars, J. and Pijaudier-Cabot, G. (1989), "Continuum Damage Theory: Application to Concrete", Journal of Engineering Mechanics, 115(2), 345--365, [10.1061/(ASCE)0733-9399(1989)115:2(345)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:2(345)).
5. Chen, W. F. and Han, D. J. (2007), "Plasticity for Structural Engineers", J. Ross Publishing, ISBN 978-1-932159-75-2.
