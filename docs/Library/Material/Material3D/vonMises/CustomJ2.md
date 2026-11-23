# CustomJ2

J2 Plasticity Model With Custom Hardening

## Theory

This model is an implementation of the [`NonlinearJ2`](NonlinearJ2.md) abstract model.
The framework uses the von Mises yield criterion with an associated flow rule and a mixed isotropic-kinematic hardening rule.

Let $$\mathbf s=\mathrm{dev}\,\mathbf\sigma$$ be the stress deviator and let $$\mathbf\beta$$ be the back stress.
The yield function is

$$
F(\mathbf\sigma,p)=\sqrt{\dfrac{3}{2}(\mathbf s-\mathbf\beta):(\mathbf s-\mathbf\beta)}-k(p)=q-k(p),
$$

where $$q=\sqrt{3J_2}$$ is the von Mises equivalent stress measured from the centre of the yield surface.
The accumulated equivalent plastic strain is

$$
p=\int\sqrt{\dfrac{2}{3}\mathrm{d}\mathbf\varepsilon^p:\mathrm{d}\mathbf\varepsilon^p}.
$$

The isotropic expression supplies the yield radius $$k(p)$$.
The kinematic expression supplies the magnitude $$h(p)=\lVert\mathbf\beta\rVert$$ of the back stress, which is always parallel to the cumulative deviatoric plastic strain.

!!! warning "implementation limitation"
    A negative value returned by the isotropic expression is clamped to zero and its derivative is discarded.
    A custom expression that becomes negative therefore loses its slope information instead of being accepted.
    The kinematic rule is restricted to one back stress whose direction follows the cumulative deviatoric plastic strain.
    A decomposition into several independently evolving back stresses is not available in this framework.
    Use ArmstrongFrederick when several Armstrong-Frederick back stresses are needed.

The associated flow rule gives

$$
\mathrm{d}\mathbf\varepsilon^p=\Delta\gamma\,\mathbf n,\qquad \mathbf n=\dfrac{\mathbf s-\mathbf\beta}{\lVert\mathbf s-\mathbf\beta\rVert},
$$

so that $$\mathrm{d}p=\sqrt{2/3}\,\Delta\gamma$$ with the multiplier normalisation used by this implementation.

!!! info "deviation from theory"
    The common textbook convention writes the plastic strain increment as the thermodynamic multiplier times $$\sqrt{3/2}$$ times the unit normal, so that the accumulated plastic strain equals that multiplier.
    This implementation absorbs the factor $$\sqrt{2/3}$$ into the multiplier, giving $$\mathrm{d}\mathbf\varepsilon^p=\Delta\gamma\mathbf n$$ and $$\mathrm{d}p=\sqrt{2/3}\Delta\gamma$$.
    The multiplier in this family must therefore not be compared directly with the multiplier used by ArmstrongFrederick or VAFCRP.

The elastic predictor is $$\mathbf\sigma^{tr}=\mathbf\sigma_n+\mathbf C^e:(\mathbf\varepsilon-\mathbf\varepsilon_n)$$ with $$\mathbf C^e$$ the isotropic elasticity tensor.
The trial shifted stress is $$\mathbf\xi=\mathrm{dev}\,\mathbf\sigma^{tr}-\mathbf\beta_n$$.
The step is elastic when $$\lVert\mathbf\xi\rVert\leqslant\sqrt{2/3}\,k(p_n)$$.

Otherwise the discrete consistency condition is solved for the plastic multiplier $$\Delta\gamma\geqslant0$$,

$$
\Psi(\Delta\gamma)=\lVert\mathbf\xi\rVert-2G\Delta\gamma-\sqrt{\dfrac{2}{3}}\left[k\left(p_n+\sqrt{\dfrac{2}{3}}\Delta\gamma\right)+h\left(p_n+\sqrt{\dfrac{2}{3}}\Delta\gamma\right)-h(p_n)\right]=0,
$$

where $$G=E/[2(1+\nu)]$$ is the shear modulus.
The Newton correction used in the source is

$$
\delta\Delta\gamma=\dfrac{\Psi}{2G+\dfrac{2}{3}\left[k'(p)+h'(p)\right]}.
$$

The stresses and the history are updated by radial return,

$$
\mathbf\sigma=\mathbf\sigma^{tr}-2G\Delta\gamma\,\mathbf n,\qquad \mathbf\beta=\mathbf\beta_n+\sqrt{\dfrac{2}{3}}\left[h(p)-h(p_n)\right]\mathbf n,\qquad p=p_n+\sqrt{\dfrac{2}{3}}\Delta\gamma.
$$

The consistent tangent is obtained by exact linearisation of the same residual.
Writing $$D=2G+\dfrac{2}{3}[k'(p)+h'(p)]$$ and $$r=\lVert\mathbf\xi\rVert$$, the deviatoric part returned by the implementation is

$$
\mathbf C^{ep}=\mathbf C^e+\dfrac{4G^2}{r^2}\left(\dfrac{\Delta\gamma}{r}-\dfrac{1}{D}\right)\mathbf\xi\otimes\mathbf\xi-\dfrac{4G^2\Delta\gamma}{r}\mathbf I_\text{dev},
$$

in which $$\mathbf I_\text{dev}$$ is the fourth-order deviatoric projector.
The iteration has a hard limit of twenty steps and an unsuccessful return mapping aborts the analysis.
The stored history consists of the accumulated plastic strain in `initial_history(0)` and the six back-stress components in `initial_history(1-6)`.

## Syntax

```text title="CustomJ2"
material CustomJ2 (1) (2) (3) (4) (5) [6]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) int, isotropic hardening expression tag
# (5) int, kinematic hardening expression tag
# [6] double, density, default: 0.0
```

## Remarks

Both hardening functions shall be defined in terms of the equivalent plastic strain.

The isotropic hardening function evaluates to the yield stress for trivial equivalent plastic strain.

The kinematic hardening function evaluates to zero for trivial equivalent plastic strain.

The usage is similar to that of [`CustomMises1D`](../../Material1D/vonMises/CustomMises1D.md).

***The expressions shall be able to compute derivatives.***

Both expressions must take exactly one input and produce exactly one output, as checked during initialisation.
The kinematic expression is additionally checked to vanish at zero plastic strain, whereas the initial yield stress from the isotropic expression is not checked and must be supplied correctly by the user.
The expressions are looked up by tag during initialisation, so they must be defined before the material is first used.
The local Newton iteration requires $$E+h'(p)+k'(p)\geqslant0$$ for all reachable plastic strain, otherwise the corrector may fail to converge.
Smooth analytic functions are preferred because kinks in either hardening curve slow down or break the local iteration.
For a hardening curve given by control points use [`MultilinearJ2`](MultilinearJ2.md), and for a polynomial curve use [`PolyJ2`](PolyJ2.md).
For a built-in exponential curve use [`ExpJ2`](ExpJ2.md), and for a Voce plus Armstrong-Frederick law use [`ArmstrongFrederick`](ArmstrongFrederick.md).
This model has no rate dependence, so use [`VAFCRP`](VAFCRP.md) when viscosity is required.
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
2. [10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6)
