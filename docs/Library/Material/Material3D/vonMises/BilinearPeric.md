# BilinearPeric

Bilinear Peric Viscous Plasticity Model

## Theory

The rate of plasticity multiplier is defined as

$$
\dot{\gamma}=\dfrac{1}{\mu}\left(\dfrac{q}{\sigma_y}-1\right)^{\dfrac{1}{\epsilon}}
$$

where $$\epsilon$$ and $$\mu$$ are two material constants, $$\sigma_y$$ is the initial yield stress, $$q=\sqrt{\dfrac{3}{2}s:s}=\sqrt{3J_2}$$ is the von Mises stress.

!!! info "deviation from theory"
    This displayed equation is the Perzyna overstress law with the power applied to the overstress ratio minus unity.
    The implemented model instead uses the Peric law with the power applied to the ratio before subtracting unity.

The yielding surface is identical to that of the von Mises model.

This model derives from the abstract [`NonlinearPeric`](NonlinearPeric.md) framework and supplies a bilinear isotropic radius,

$$
k(p)=\sigma_y+H p,
$$

where $$p=\int\sqrt{\dfrac{2}{3}\mathrm{d}\boldsymbol\varepsilon^p:\mathrm{d}\boldsymbol\varepsilon^p}$$ is the accumulated plastic strain and $$H$$ is the input hardening modulus.
A negative modulus gives linear softening and the radius is clamped to zero once it would become negative.
The accumulated plastic strain is the only history variable.

!!! warning "implementation limitation"
    The derivative of the radius is also set to zero when the radius is clamped.
    Softening therefore terminates abruptly instead of continuing with a negative yield radius.

The elastic predictor is $$\boldsymbol\sigma^{tr}=\boldsymbol\sigma_n+\boldsymbol C^e:(\boldsymbol\varepsilon-\boldsymbol\varepsilon_n)$$ and the trial von Mises stress is $$q^{tr}=\sqrt{3/2}\,\lVert\mathrm{dev}\,\boldsymbol\sigma^{tr}\rVert$$.
If $$q^{tr}\leqslant k(p_n)$$ the step is elastic.
Otherwise the multiplier $$\gamma$$ is found from the implicit residual

$$
\left(q^{tr}-3G\gamma\right)\left(\dfrac{\Delta t}{\Delta t+\mu\gamma}\right)^\epsilon-k(p_n+\gamma)=0,
$$

which is the discrete form of the rate law shown above when the Peric overstress definition is used.
The stress is returned by radial return, $$\boldsymbol\sigma=\boldsymbol\sigma^{tr}-3G\gamma\,\mathrm{dev}\,\boldsymbol\sigma^{tr}/\lVert\mathrm{dev}\,\boldsymbol\sigma^{tr}\rVert$$.
The consistent tangent follows from linearisation of the same residual, and the analysis step time enters the viscosity through $$\Delta t$$.

## Syntax

```text title="BilinearPeric"
material BilinearPeric (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, yield stress
# (5) double, hardening modulus
# (6) double, mu
# (7) double, epsilon
# [8] double, density, default: 0.0
```

## Remarks

The fourth input is a hardening modulus with stress units, not a dimensionless hardening ratio as in [`BilinearJ2`](BilinearJ2.md).
The formula displayed at the top of this page is the Perzyna overstress form, whereas the implementation in `NonlinearPeric.cpp` uses the Peric form $$\dot\gamma=(1/\mu)[(q/k)^{1/\epsilon}-1]$$ described on the [`VAFCRP`](VAFCRP.md) page.
Either $$\mu=0$$ or $$\epsilon=0$$ removes the rate dependence and gives the rate-independent bilinear J2 limit.
The viscosity parameter $$\mu$$ carries time units, so the step time used by the analysis must represent real time and must be consistent with the calibration.
This model has no kinematic hardening, so use [`VAFCRP`](VAFCRP.md) when a Bauschinger effect is needed.
The uniaxial counterpart is [`VAFCRP1D`](../../Material1D/vonMises/VAFCRP1D.md) with the appropriate hardening inputs.
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. [10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807)
2. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
