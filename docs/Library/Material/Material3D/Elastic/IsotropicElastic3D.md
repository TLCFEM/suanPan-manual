# IsotropicElastic3D

Isotropic Elastic Material

The `IsotropicElastic3D` model implements three-dimensional linear isotropic elasticity, i.e., Hooke's law.
Only two independent constants are needed: the elastic modulus and Poisson's ratio.

## Syntax

```text title="IsotropicElastic3D"
material IsotropicElastic3D (1) (2) (3) [4]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# [4] double, density, default: 0.0
```

## Background

Stress and strain are related by

$$
\boldsymbol\sigma=2G\boldsymbol\varepsilon+\lambda\,\mathrm{tr}(\boldsymbol\varepsilon)\boldsymbol I,\qquad
G=\dfrac{E}{2(1+\nu)},\qquad
\lambda=\dfrac{E\nu}{(1+\nu)(1-2\nu)}.
$$

## Remarks

The first two arguments are `(2)` the elastic modulus $$E$$ and `(3)` Poisson's ratio $$\nu$$, in that order.
Both are converted to absolute values.
The implementation evaluates $$\lambda=G\nu/(0.5-\nu)$$, so Poisson's ratio must stay below 0.5 for a bounded bulk modulus.
For direction-dependent stiffness use [`OrthotropicElastic3D`](OrthotropicElastic3D.md); the material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.

`Elastic3D` is accepted as a short alias for `IsotropicElastic3D` and takes the same arguments.
