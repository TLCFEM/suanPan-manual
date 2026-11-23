# NonlinearGurson

Nonlinear General Gurson Porous Model

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

## Theory

This abstract model implements Gurson-Tvergaard-Needleman porous plasticity for a von Mises matrix.
Damage is represented by the void volume fraction $$f$$, so the yield condition depends on the hydrostatic stress $$p$$ as well as the equivalent stress $$q$$.
The model assumes isotropic hardening of the matrix, an associated flow rule and approximately spherical voids.
The parameters $$q_1$$ and $$q_2$$ calibrate the original Gurson upper-bound criterion against unit-cell calculations for interacting voids, with the original model recovered at $$q_1=q_2=1$$.
The heat-like cohesive term makes the response sensitive to stress triaxiality, which is the ratio $$p/q$$.
The current implementation includes void growth and strain-controlled nucleation but no void coalescence or loss of load-carrying capacity.

!!! warning "implementation limitation"
    The Tvergaard-Needleman coalescence stage and the critical void fraction for final failure are not implemented.
    The response softens through void growth alone and does not drop to zero stress at a fully damaged state.

The return mapping treats the plastic multiplier, the hydrostatic stress, the equivalent plastic strain and the void fraction as unknowns of one coupled Newton system.
The consistent tangent is obtained from the same Jacobian by premultiplying with the elastic stiffness, which makes the overall tangent generally non-symmetric.
A derived class supplies the matrix yield stress $$\sigma_y(\varepsilon_m^p)$$ and its derivative through the virtual `compute_hardening` method.
The concrete variants are [`ExpGurson`](ExpGurson.md), [`CustomGurson`](CustomGurson.md) and [`TableGurson`](TableGurson.md).

## Yield Function

An extended yield function is used,

$$
F=q^2+2q_1f\sigma_y^2\cosh\left(\dfrac{3}{2}\dfrac{q_2p}{\sigma_y}\right)-\sigma_y^2\left(q_1^2f^2+1\right),
$$

where

$$
s=\mathrm{dev}~\sigma,\qquad{}p=\dfrac{\mathrm{tr}~
\sigma}{3}=\dfrac{I_1}{3},\qquad{}q=\sqrt{3J_2}=\sqrt{\dfrac{3}{2}s:s}=\sqrt{\dfrac{3}{2}}|s|.
$$

Furthermore, $$q_1$$, $$q_2$$ and $$q_3=q_1^2$$ are model constants, $$f(\varepsilon_m^p)$$ is the volume fraction, $$\sigma_y(\varepsilon_m^p)$$ is the yield stress, $$\varepsilon_m^p$$ is the equivalent plastic strain.

* $$q_1=q_2=1$$ The original Gurson model is recovered.
* $$q_1=0$$ The von Mises model is recovered.

The following is a visualization of the yield surface in the $$p-q$$ plane.

<iframe src="https://www.desmos.com/calculator/e3b2fbea70?embed" width="800" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

## Evolution of Equivalent Plastic Strain

The evolution of $$\varepsilon_m^p$$ is assumed to be governed by the equivalent plastic work expression,

$$
\left(1-f\right)\sigma_y\Delta\varepsilon^p_m=\sigma:\Delta\varepsilon^p=2\Delta\gamma\left(
\dfrac{q^{tr}}{1+6G\Delta\gamma}\right)^2+3q_1q_2p\Delta\gamma{}f\sigma_y\sinh\left(
\dfrac{3}{2}\dfrac{q_2p}{\sigma_y}\right).
$$

## Evolution of Volume Fraction

The evolution of volume fraction consists of two parts.

$$
\Delta{}f=\Delta{}f_g+\Delta{}f_n,
$$

where

$$
\Delta{}f_g=(1-f)\Delta\varepsilon_v,\qquad\Delta{}f_n=A\Delta\varepsilon_m^p
$$

with

$$
A=\dfrac{f_N}{s_N\sqrt{2\pi}}\exp\left(-\dfrac{1}{2}\left(\dfrac{\varepsilon_m^p-\varepsilon_N}{s_N}\right)^2\right).
$$

Parameters $$f_N$$, $$s_N$$ and $$\varepsilon_N$$ control the normal distribution of volume fraction.
**If $$f_N=0$$, the nucleation is disabled.**
**In this case, when $$f_0=0$$, the volume fraction will stay at zero regardless of strain history.**

There is no consideration of coalescence in the current implementation.

!!! warning "implementation limitation"
    The void volume fraction is clamped into the interval from zero to one after every Newton update.
    A trial increment that would exceed these bounds is truncated rather than rejected.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| VF             | volume fraction  |

## Remarks

This is an abstract class and cannot be selected directly by a material token.
The history has two entries, the equivalent plastic strain in `initial_history(0)` and the void volume fraction in `initial_history(1)`.
There is no initial void fraction material parameter, so a nonzero initial value must be set with the `initial material history` command.

!!! warning "implementation limitation"
    The initial void fraction defaults to zero when no history is supplied.
    Omitting the history definition silently gives a fully dense material even when nucleation is activated.

With $$f_N=0$$ and a zero initial void fraction the void fraction stays zero and the model reduces to ordinary von Mises plasticity.
Void nucleation uses a normal distribution in plastic strain with mean $$\varepsilon_N$$ and standard deviation $$s_N$$, and the total nucleated fraction is $$f_N$$.
Because the yield function contains $$q^2$$ and $$\sigma_y^2$$, choose a stress unit that avoids overflow when the input numbers are squared.
Small strain increments are recommended near the peak load, where the softening due to void growth is rapid.
Use a three-dimensional solid element such as `C3D8`, and consider `set symm_mat 0` if the non-symmetric tangent affects convergence.
Record `VF` with a recorder to visualise the evolution of porosity.

## References

1. A. L. Gurson, Continuum theory of ductile rupture by void nucleation and growth, Part I: yield criteria and flow rules for porous ductile media, *Journal of Engineering Materials and Technology* 99 (1977) 2--15, [doi:10.1115/1.3443401](https://doi.org/10.1115/1.3443401).
2. V. Tvergaard and A. Needleman, Analysis of the cup-cone fracture in a round tensile bar, *Acta Metallurgica* 32 (1984) 157--169, [doi:10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X).