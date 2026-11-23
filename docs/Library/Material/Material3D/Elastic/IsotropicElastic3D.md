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

Here $E$ is the Young's modulus, $\nu$ is Poisson's ratio, $G$ is the shear modulus, and $\lambda$ is the first Lamé constant.
The second Lamé constant is $\mu=G$.
Splitting the strain into a volumetric part and a deviatoric part, $\boldsymbol\varepsilon=\tfrac13\varepsilon_v\boldsymbol I+\boldsymbol\varepsilon_d$ with $\varepsilon_v=\mathrm{tr}(\boldsymbol\varepsilon)$ and $\mathrm{tr}(\boldsymbol\varepsilon_d)=0$, gives the equivalent form

$$
\boldsymbol\sigma=K\varepsilon_v\boldsymbol I+2G\boldsymbol\varepsilon_d,\qquad
K=\lambda+\dfrac23G=\dfrac{E}{3(1-2\nu)}.
$$

The strain energy density is

$$
W=\dfrac12K\varepsilon_v^2+G\boldsymbol\varepsilon_d:\boldsymbol\varepsilon_d.
$$

Positive definiteness requires $G>0$ and $K>0$, which gives the thermodynamic bounds $-1<\nu<\tfrac12$.
As $\nu\to\tfrac12$ the bulk modulus diverges and the response becomes incompressible, so nearly incompressible values produce volumetric locking in displacement-only low-order elements.
Negative Poisson's ratios are admissible in theory but cannot be entered through the command line because the constructor replaces both moduli by their absolute values.
In the Voigt convention $(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$ used by the 3D elements, $\gamma_{ij}=2\varepsilon_{ij}$ is the engineering shear strain and the shear entries of the stiffness matrix equal $G$.

!!! warning "implementation limitation"
    The constructor applies `fabs` to both `E` and `nu`, so auxetic materials with negative Poisson's ratio cannot be represented.
    A value of `nu` at or above `0.5` is not rejected by the parser and yields a singular or negative bulk modulus.

## Remarks

The first two arguments are `(2)` the elastic modulus $$E$$ and `(3)` Poisson's ratio $$\nu$$, in that order.
Both are converted to absolute values.
The implementation evaluates $$\lambda=G\nu/(0.5-\nu)$$, so Poisson's ratio must stay below 0.5 for a bounded bulk modulus.
For direction-dependent stiffness use [`OrthotropicElastic3D`](OrthotropicElastic3D.md); the material axes can be reoriented with the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.

`Elastic3D` is accepted as a short alias for `IsotropicElastic3D` and takes the same arguments.

The implementation evaluates $\lambda=G\nu/(0.5-\nu)$ in `tensor::isotropic_stiffness`, which is algebraically identical to the expression given above.
A value of $\nu$ at or above $0.5$ makes the denominator vanish or change sign and must be avoided.
The response is path independent and the tangent matrix is constant, so no history variables are stored.
Use [`OrthotropicElastic3D`](OrthotropicElastic3D.md) when the stiffness differs along material axes.
Use [`NonlocalIsotropicElastic3D`](NonlocalIsotropicElastic3D.md) when a gradient-regularised softening response is required.
For finite-strain rubber-like behaviour use [`MooneyRivlin`](MooneyRivlin.md), [`Yeoh`](Yeoh.md) or [`BlatzKo`](BlatzKo.md) with nonlinear geometry enabled in the element.
Any consistent unit system may be used, but $E$, $\lambda$ and $K$ must share the stress units of the model and the optional density must match the mass units.

## Example

```text
material IsotropicElastic3D 1 2E5 0.3 7.85E-9
```

## References

1. L. D. Landau and E. M. Lifshitz, *Theory of Elasticity*, 3rd ed., Butterworth-Heinemann, 1986, Chapter 2.
2. G. A. Holzapfel, *Nonlinear Solid Mechanics*, Wiley, 2000, Section 3.3.
