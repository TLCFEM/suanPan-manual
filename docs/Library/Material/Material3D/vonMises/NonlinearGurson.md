# NonlinearGurson

Nonlinear General Gurson Porous Model

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

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

Furthermore, $$q_1$$, $$q_2$$ and $$q_3=q_1^2$$ are model constants, $$f(\varepsilon_m^p)$$ is the volume fraction,
$$\sigma_y(\varepsilon_m^p)$$ is the yield stress, $$\varepsilon_m^p$$ is the equivalent plastic strain.

* $$q_1=q_2=1$$ The original Gurson model is recovered.
* $$q_1=0$$ The von Mises model is recovered.

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

Parameters $$f_N$$, $$s_N$$ and $$\varepsilon_N$$ controls the normal distribution of volume fraction. **If $$f_N=0$$,
the nucleation is disabled. In this case, when $$f_0=0$$, the volume fraction will stay at zero regardless of strain
history.**

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| VF             | volume fraction  |
