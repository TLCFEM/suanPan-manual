# Mises1D

Uniaxial General Model Using von Mises Criterion

This is an abstract class that shall be overridden.

The `Mises1D` model is a general model using von Mises yielding criterion and associated flow rule.
The hardening rules can be customized.

## Theory

### Yield Function

A von Mises type yield function is used.

$$
F=|\sigma-\beta|-k
$$

### Flow Rule

The associated plasticity is assumed.

$$
\mathrm{d}\varepsilon^p=\gamma\dfrac{\partial{}F}{\partial\sigma}=\text{sign}(\sigma-\beta)~\gamma
$$

### Hardening

Both isotropic and kinematic hardening rules are employed.

#### Isotropic Hardening

A general function of accumulated plastic strain $$p$$ needs to be defined.

$$
k=k(p),
$$

where $$p=\displaystyle\int|\mathrm{d}\varepsilon^p|~\mathrm{d}t$$ is the accumulated plastic strain.

#### Kinematic Hardening

A general function of accumulated plastic strain $$p$$ needs to be defined.

$$
\beta=h(p).
$$

!!! info "deviation from theory"
    The back stress is not an independent state variable in this family.
    It is a prescribed scalar function of the accumulated plastic strain multiplied by the sign of the trial shifted stress.
    A classical Chaboche or Armstrong--Frederick back stress obeys its own differential equation and must be stored as an independent history variable.
    Use [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md) when that behaviour is required.

### Return Mapping

A plastic corrector is applied when the elastic predictor violates the yield condition.
The trial stress and the trial shifted stress are

$$
\sigma^\text{tr}=\sigma_n+E\Delta\varepsilon,\qquad \xi=\sigma^\text{tr}-\beta_n.
$$

If $$|\xi|\leqslant{}k(p_n)$$, the step is elastic and no history variable changes.
Otherwise, a plastic multiplier $$\gamma\geqslant0$$ is solved from the discrete consistency condition

$$
\left|\sigma^\text{tr}-E\gamma\,\operatorname{sign}\xi-h(p_n+\gamma)\right|-k(p_n+\gamma)=0.
$$

The accumulated plastic strain is incremented by $$p=p_n+\gamma$$ because $$|\mathrm{d}\varepsilon^p|=\mathrm{d}\gamma$$ in one dimension.
The back stress is updated as $$\beta=h(p)$$ with the sign of $$\xi$$.

The Newton correction used by the implementation is

$$
\Delta\gamma=\dfrac{F}{E+\dfrac{\mathrm{d}k}{\mathrm{d}p}+\dfrac{\mathrm{d}h}{\mathrm{d}p}},\qquad\gamma\leftarrow\gamma+\Delta\gamma,
$$

where $$F$$ is the current value of the consistency residual.
The iteration terminates when the correction is below the tolerance or the residual is small after a few iterations, with a hard limit of 20 iterations.
A failure to converge aborts the analysis step with an error message.

The consistent elastoplastic tangent returned by the implementation is

$$
E^{ep}=E\,\dfrac{H}{E+H},\qquad H=\dfrac{\mathrm{d}k}{\mathrm{d}p}+\dfrac{\mathrm{d}h}{\mathrm{d}p}.
$$

!!! warning "implementation limitation"
    A perfectly plastic definition with $$H=0$$ gives a zero algorithmic tangent during plastic loading.
    The yield radius is also clamped to zero, so a hardening function that becomes negative cannot drive the radius below zero.

!!! note "developer note"
    The source multiplies the elastic stiffness by $$H/(E+H)$$ directly.

## Implementation

The function $$k(p)$$ and $$h(p)$$ need to be defined in the derived classes.
In the source tree the abstract base class is `NonlinearMises1D`, which exposes four pure virtual functions.
These are `compute_k(p)`, `compute_dk(p)`, `compute_h(p)` and `compute_dh(p)`, returning $$k$$, $$\mathrm{d}k/\mathrm{d}p$$, $$h$$ and $$\mathrm{d}h/\mathrm{d}p$$, respectively.

The concrete models in this family are [`BilinearMises1D`](BilinearMises1D.md), [`ExpMises1D`](ExpMises1D.md), [`MultilinearMises1D`](Multilinear1D.md) and [`CustomMises1D`](CustomMises1D.md).

## Remarks

`Mises1D` itself is a conceptual base and is not a valid material token in the parser.
Use one of the concrete models listed above, or derive a new class from `NonlinearMises1D`.

!!! warning "implementation limitation"
    The `Mises1D` token is not registered, so a misspelled name fails at material creation instead of selecting this model.

!!! note "developer note"
    The token registry in `MaterialParser.cpp` contains no entry named `Mises1D`, and unknown tokens are passed to the external-module hook rather than falling back to this base class.

The elastic modulus passed to the constructor is converted to its absolute value.
The yield radius is evaluated as $$\max(0,k(p))$$, so a negative isotropic function cannot produce a negative radius.

The stored history consists of the accumulated plastic strain $$p$$ in `initial_history(0)` and the back stress $$\beta$$ in `initial_history(1)`.
A step with a vanishing strain increment returns immediately, leaving the plastic variables untouched.

!!! info "deviation from theory"
    There is no viscous branch in this base class.
    A zero strain increment can never generate creep or stress relaxation, even if the imposed stress would exceed the yield radius.
    Rate dependence requires [`VAFCRP1D`](VAFCRP1D.md) or [`SubloadingViscous1D`](SubloadingViscous1D.md).

This base class supports isotropic hardening, kinematic hardening, or both, but it has no drag stress, damage or rate dependence.
For nonlinear kinematic hardening use [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md), and for rate dependence use [`VAFCRP1D`](VAFCRP1D.md) or [`SubloadingViscous1D`](SubloadingViscous1D.md).

These models are intended for truss, beam and other elements that expect a `Material1D` object.
For general stress states use the three-dimensional counterparts such as [`NonlinearJ2`](../../Material3D/vonMises/NonlinearJ2.md).

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
2. [10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6)
