# ExpHoffman

Exponential Hardening Hoffman Model

## Background

This model combines the orthotropic elasticity of [`OrthotropicElastic3D`](../Elastic/OrthotropicElastic3D.md) with associative plasticity based on the Hoffman yield criterion.
The nine elastic constants are $E_1,E_2,E_3,G_{12},G_{23},G_{13}$ and $\nu_{12},\nu_{23},\nu_{13}$.
The nine strength parameters are $\sigma_{11}^t,\sigma_{11}^c,\sigma_{22}^t,\sigma_{22}^c,\sigma_{33}^t,\sigma_{33}^c,\sigma_{12}^0,\sigma_{23}^0,\sigma_{13}^0$.
The yield function is written in quadratic form as

$$
F(\boldsymbol\sigma,\bar\varepsilon_p)=\frac12\boldsymbol\sigma^\mathrm T\mathbf P\boldsymbol\sigma+\boldsymbol q^\mathrm T\boldsymbol\sigma-K^2(\bar\varepsilon_p),
$$

where $\boldsymbol\sigma=(\sigma_{11},\sigma_{22},\sigma_{33},\sigma_{12},\sigma_{23},\sigma_{13})^\mathrm T$.
The matrix and vector are assembled directly from the nine strengths:

$$
P_{11}=\frac{2}{\sigma_{11}^t\sigma_{11}^c},\quad P_{22}=\frac{2}{\sigma_{22}^t\sigma_{22}^c},\quad P_{33}=\frac{2}{\sigma_{33}^t\sigma_{33}^c},
$$

$$
P_{44}=\frac{2}{(\sigma_{12}^0)^2},\quad P_{55}=\frac{2}{(\sigma_{23}^0)^2},\quad P_{66}=\frac{2}{(\sigma_{13}^0)^2},
$$

$$
P_{12}=P_{21}=\frac{1}{\sigma_{33}^t\sigma_{33}^c}-\frac{1}{\sigma_{11}^t\sigma_{11}^c}-\frac{1}{\sigma_{22}^t\sigma_{22}^c},
$$

with the other normal cross terms obtained by cyclic permutation, and

$$
q_1=\frac{\sigma_{11}^c-\sigma_{11}^t}{\sigma_{11}^t\sigma_{11}^c},\quad q_2=\frac{\sigma_{22}^c-\sigma_{22}^t}{\sigma_{22}^t\sigma_{22}^c},\quad q_3=\frac{\sigma_{33}^c-\sigma_{33}^t}{\sigma_{33}^t\sigma_{33}^c}.
$$

The linear terms $q_i$ are what allow different tensile and compressive strengths.
The plastic flow is associative with $\Delta\boldsymbol\varepsilon_p=\Delta\gamma(\mathbf P\boldsymbol\sigma+\boldsymbol q)$.
The equivalent plastic strain is accumulated as $\Delta\bar\varepsilon_p=\sqrt{2/3}\lVert\Delta\boldsymbol\varepsilon_p\rVert$.
The elastic predictor uses the orthotropic stiffness and the consistency condition is solved by Newton iteration with a bisection fallback.
The history stores the equivalent plastic strain at location 0 and the six plastic strain components at locations 1 to 6.
The same framework with a Tsai-Wu quadratic form is documented in [`ExpTsaiWu`](ExpTsaiWu.md).

## Theory

The isotropic hardening rule is defined as

$$
K(\bar\varepsilon_p)=1+a(1-e^{-b\bar\varepsilon_p})
$$

The derivative is $\mathrm dK/\mathrm d\bar\varepsilon_p=ab\exp(-b\bar\varepsilon_p)$.
The function starts from $K(0)=1$ and saturates at $1+a$, so $b$ sets the plastic strain scale over which saturation occurs.
The yield surface is scaled by $K^2$, hence its size approaches $(1+a)^2$ at saturation.

!!! warning "implementation limitation"
    The parameters `a` and `b` are not converted to absolute values, so a negative `a` produces unbounded softening instead of saturation.

## Syntax

```text title="ExpHoffman"
material ExpHoffman (1) (2...7) (8...10) (11...19) (20) (21) [22]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three Poisson's ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stresses
# (20) double, a
# (21) double, b
# [22] double, density, default: 0.0
```

## Remarks

The nine yield stresses are ordered as $\sigma_{11}^t,\sigma_{11}^c,\sigma_{22}^t,\sigma_{22}^c,\sigma_{33}^t,\sigma_{33}^c,\sigma_{12}^0,\sigma_{23}^0,\sigma_{13}^0$.
The six moduli are ordered as $E_1,E_2,E_3,G_{12},G_{23},G_{13}$ and the three Poisson's ratios as $\nu_{12},\nu_{23},\nu_{13}$.
None of the elastic or strength inputs are converted to absolute values, so positive strengths must be supplied explicitly.
The material axes coincide with the global axes by default and can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.
The model is intended for 3D solid elements such as [`C3D8`](../../../Element/Cube/C3D8.md).
Related variants are [`BilinearHoffman`](BilinearHoffman.md), [`CustomHoffman`](CustomHoffman.md) and the Hill reduction [`NonlinearHill`](NonlinearHill.md).

## References

1. [10.1177/002199836700100210](https://doi.org/10.1177/002199836700100210)
2. [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf)
