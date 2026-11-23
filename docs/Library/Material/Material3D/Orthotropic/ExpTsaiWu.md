# ExpTsaiWu

Exponential Hardening Tsai-Wu Model

## References

1. [Tsai-Wu failure criterion](https://en.wikipedia.org/wiki/Tsai%E2%80%93Wu_failure_criterion)
2. [10.1016/S0045-7825(02)00605-9](https://doi.org/10.1016/S0045-7825(02)00605-9)

3. [10.1177/002199837100500106](https://doi.org/10.1177/002199837100500106)

## Background

This model combines the orthotropic elasticity of [`OrthotropicElastic3D`](../Elastic/OrthotropicElastic3D.md) with associative plasticity based on the Tsai-Wu yield criterion.
The yield function has the same quadratic structure as [`ExpHoffman`](ExpHoffman.md),

$$
F(\mathbf\sigma,\bar\varepsilon_p)=\frac12\mathbf\sigma^\mathrm T\mathbf P\mathbf\sigma+\mathbf q^\mathrm T\mathbf\sigma-K^2(\bar\varepsilon_p),
$$

but the interaction terms are defined by the Tsai-Wu tensor-polynomial theory.
With $$T_1=1/(\sigma_{11}^t\sigma_{11}^c)$$, $$T_2=1/(\sigma_{22}^t\sigma_{22}^c)$$ and $$T_3=1/(\sigma_{33}^t\sigma_{33}^c)$$, the normal cross terms are

$$
P_{12}=P_{21}=-\sqrt{T_1T_2},\quad P_{23}=P_{32}=-\sqrt{T_2T_3},\quad P_{13}=P_{31}=-\sqrt{T_3T_1}.
$$

The diagonal terms are $$P_{11}=2T_1$$, $$P_{22}=2T_2$$, $$P_{33}=2T_3$$ and $$P_{ii}=2/(\sigma_{ij}^0)^2$$ for the shear entries, and the linear terms are $$q_i=(\sigma_{ii}^c-\sigma_{ii}^t)/(\sigma_{ii}^t\sigma_{ii}^c)$$.
The chosen interaction terms keep the yield ellipse closed, but the model does not distinguish individual failure modes.
The plastic flow is associative, the equivalent plastic strain uses $$\sqrt{2/3}\lVert\Delta\mathbf\varepsilon_p\rVert$$, and the history layout matches [`ExpHoffman`](ExpHoffman.md).

!!! info "deviation from theory"
    The implementation uses the Tsai interaction $$F_{ij}=-\tfrac12\sqrt{F_{ii}F_{jj}}$$ rather than requiring an independently measured biaxial strength.
    The interaction strength is therefore not a free parameter.

## Theory

The isotropic hardening rule is defined as

$$
K(\bar\varepsilon_p)=1+a(1-e^{-b\bar\varepsilon_p})
$$

The derivative is $$\mathrm dK/\mathrm d\bar\varepsilon_p=ab\exp(-b\bar\varepsilon_p)$$.
The function starts from $$K(0)=1$$ and saturates at $$1+a$$, so $$b$$ sets the plastic strain scale over which saturation occurs.
The yield surface is scaled by $$K^2$$, hence its size approaches $$(1+a)^2$$ at saturation.

!!! warning "implementation limitation"
    The parameters `a` and `b` are not converted to absolute values, so a negative `a` produces unbounded softening instead of saturation.

## Syntax

```text title="ExpTsaiWu"
material ExpTsaiWu (1) (2...7) (8...10) (11...19) (20) (21) [22]
# (1) int, unique material tag
# (2...7) double, six moduli: E_{xx}, E_{yy}, E_{zz}, G_{xy}, G_{yz}, G_{zx}
# (8...10) double, three Poisson's ratios: v_{xy}, v_{yz}, v_{xz}
# (11...19) double, nine yield stresses
# (20) double, a
# (21) double, b
# [22] double, density, default: 0.0
```

## Remarks

The nine yield stresses are ordered as $$\sigma_{11}^t,\sigma_{11}^c,\sigma_{22}^t,\sigma_{22}^c,\sigma_{33}^t,\sigma_{33}^c,\sigma_{12}^0,\sigma_{23}^0,\sigma_{13}^0$$.
The six moduli are ordered as $$E_1,E_2,E_3,G_{12},G_{23},G_{13}$$ and the three Poisson's ratios as $$\nu_{12},\nu_{23},\nu_{13}$$.
None of the elastic or strength inputs are converted to absolute values, so positive strengths must be supplied explicitly.
The material axes coincide with the global axes by default and can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.
The model is intended for 3D solid elements such as [`C3D8`](../../../Element/Cube/C3D8.md).
Related variants are [`BilinearTsaiWu`](BilinearTsaiWu.md), [`CustomTsaiWu`](CustomTsaiWu.md) and the Hoffman counterpart [`ExpHoffman`](ExpHoffman.md).
