# IsotropicDamage

Independent Isotropic Damage Model

The `IsotropicDamage` model interacts with an associated 3D material model and computes the damage factor based on total strain or other related quantities.

## Background

Continuum damage mechanics represents distributed microcracking by an internal variable that reduces the load-carrying capacity of a material.
Kachanov introduced a scalar continuity $\psi$ with $\psi=1$ for the intact state and $\psi=0$ at failure, and Rabotnov introduced the damage variable $\omega=1-\psi$.
The effective stress concept of Lemaitre and Chaboche postulates that the damaged material behaves like the intact material subjected to $\tilde{\mathbf\sigma}=\mathbf\sigma/(1-\omega)$.
For an elastic host with fourth-order stiffness $\mathbf D_0$, the strain equivalence hypothesis gives the damaged response $\mathbf\sigma=(1-\omega)\mathbf D_0:\mathbf\varepsilon$ and the damage energy release rate $Y=-\partial\psi/\partial\omega=\tfrac12\mathbf\varepsilon:\mathbf D_0:\mathbf\varepsilon$.
Irreversibility is enforced by an internal variable $\kappa$ that stores the maximum equivalent strain ever reached, so that $\omega=g(\kappa)$ with $\dot\kappa\geq0$.
For a general nonlinear host the damaged stress can be written as $\mathbf\sigma=\Omega\,\bar{\mathbf\sigma}(\mathbf\varepsilon)$ with the damage factor $\Omega=1-\omega$, and the consistent tangent becomes $\mathbf K=\Omega\bar{\mathbf K}+\bar{\mathbf\sigma}\otimes\partial\Omega/\partial\mathbf\varepsilon$.
Because the damage factor is a scalar, this class of models cannot distinguish cracks with different orientations and assumes that damage affects all directions equally.

!!! warning "implementation limitation"
    The host material is advanced with the total strain, not with an effective strain obtained from the damage variable.
    Damage is applied afterwards to the host stress and stiffness, so the strain equivalence hypothesis is not enforced inside the host constitutive integration.

## Interface

The `update_trial_status(const vec&)` is implemented so that `trial_stress` and `trial_stiffness` store the corresponding response of the associated material model and call the `update_damage()` method.

The `update_damage()` method shall be implemented in all derived classes.

Alternatively, material state update method `update_trial_status(const vec&)` can be thoroughly overridden by the derived classes.

!!! note "developer note"
    The source calls a pure virtual method named `compute_damage()`, not `update_damage()`.
    A derived class must override `compute_damage()` for the base implementation of `update_trial_status` to compile and run.

## Remarks

* The associated material tag must refer to a three-dimensional material, since the source rejects hosts whose material type is not `D3`.
* Density is inherited from the host material and parameter queries are forwarded to it, so the wrapper does not introduce separate elastic constants.
* The host is updated first with the total strain, and its trial stress and trial stiffness are copied before `compute_damage()` is called.
* The class is abstract and has no material parser token, so only concrete subclasses such as [`LinearDamage`](LinearDamage.md) can be created with a `material` command.
* Crack closure under compression is not represented, so the model predicts the same stiffness reduction in tension and compression.
* Damage evolution is local and has no characteristic length, so strain softening localises into one element layer and results depend on mesh size.
* Use three-dimensional solid elements such as [C3D8](../../../Element/Cube/C3D8.md) and set `symm_mat 0` if the derived consistent tangent is non-symmetric.

## References

1. On the Time to Failure under Creep Conditions
2. [ISBN 978-0-7204-2357-0](https://search.worldcat.org/search?q=bn:9780720423570)
3. [ISBN 978-0-521-32853-1](https://search.worldcat.org/search?q=bn:9780521328531)
4. [10.1061/(ASCE)0733-9399(1989)115:2(345)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:2(345))
5. [ISBN 978-1-932159-75-2](https://search.worldcat.org/search?q=bn:9781932159752)
