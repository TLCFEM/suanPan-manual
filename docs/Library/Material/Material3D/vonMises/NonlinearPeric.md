# NonlinearPeric

Viscoplasticity

## Theory

Similar to the classic rate independent J2 plasticity, the `NonlinearPeric` class defines a J2 plasticity that incorporates viscoplasticity using Peric's model, that is

$$
\dot\gamma(\sigma,\sigma_y)=\left\{\begin{array}{ll}\dfrac{1}{\mu}\left[\dfrac{q(\sigma)}{\sigma_y}-1\right]
^{1/\epsilon},&\Phi\ge0,\\0,&\Phi<0.\end{array}\right.
$$

In which, $$\mu$$ is a viscosity-related parameter, $$\epsilon$$ is the rate sensitivity, and a larger $$\epsilon$$ means the
response is more sensitive to rate, $$q(\sigma)=\sqrt{\dfrac{3}{2}\eta:\eta}$$ as before is the effective von Mises
stress.

!!! info "deviation from theory"
    The equation above is the Perzyna overstress law, while the implementation uses the Peric law with the power applied to the stress ratio before subtracting unity.
    In the implemented form a smaller $$\epsilon$$ gives the stronger rate sensitivity.

This is an abstract base class, and a derived class supplies the isotropic radius $$k(p)$$ and its derivative $$k'(p)$$ as functions of the accumulated plastic strain $$p$$.

!!! warning "implementation limitation"
    A negative radius from the derived class is clamped to zero and its derivative is discarded.

The elastic predictor gives the trial stress and the trial von Mises stress $$q^{tr}=\sqrt{3/2}\lVert\mathrm{dev}\,\boldsymbol\sigma^{tr}\rVert$$.
With the multiplier normalisation $$\mathrm{d}\boldsymbol\varepsilon^p=\sqrt{3/2}\,\gamma\,\boldsymbol n$$ one has $$\mathrm{d}p=\gamma$$ and $$q=q^{tr}-3G\gamma$$ during radial return.
The backward-Euler residual solved by the local Newton iteration is

$$
\left(q^{tr}-3G\gamma\right)\left(\dfrac{\Delta t}{\Delta t+\mu\gamma}\right)^\epsilon-k(p_n+\gamma)=0.
$$

It is the discrete form of the Peric overstress law $$\dot\gamma=(1/\mu)[(q/k)^{1/\epsilon}-1]$$, because it rearranges to $$q=k(1+\mu\gamma/\Delta t)^\epsilon$$.
The consistent tangent is obtained by linearising this residual with respect to strain, and it reduces to the rate-independent J2 tangent when viscosity disappears.
The only history variable is the accumulated plastic strain in `initial_history(0)`.
The concrete subclass [`BilinearPeric`](BilinearPeric.md) supplies a bilinear radius $$k(p)=\sigma_y+Hp$$, and [`VAFCRP`](VAFCRP.md) adds multiple Armstrong-Frederick back stresses.

## Remarks

The overstress law displayed above is the Perzyna form, while the implementation in `NonlinearPeric.cpp` uses the Peric form $$\dot\gamma=(1/\mu)[(q/k)^{1/\epsilon}-1]$$, as explained on the [`VAFCRP`](VAFCRP.md) page.
In the implemented Peric form the exponent is $$1/\epsilon$$, so a smaller $$\epsilon$$ gives a stronger rate sensitivity for a fixed overstress.
The viscosity parameter $$\mu$$ carries time units, so the step time must be interpreted as real time and must be consistent with the calibration.
Either $$\mu=0$$ or $$\epsilon=0$$ removes rate dependence and recovers the rate-independent limit.
A vanishing strain increment leaves the history unchanged.

## References

1. D. Peric, On a class of constitutive equations in viscoplasticity: formulation and computational issues, *International Journal for Numerical Methods in Engineering* 36 (1993) 1365--1393, [doi:10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807).
2. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer, New York, 1998, [doi:10.1007/b98904](https://doi.org/10.1007/b98904).
