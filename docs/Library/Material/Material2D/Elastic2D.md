# Elastic2D

2D Elastic Model

## Background

The two-dimensional elasticity models are obtained by reducing the three-dimensional Hooke law under either plane stress or plane strain.
With engineering shear strain $$\gamma_{12}=2\varepsilon_{12}$$, the 3D law is $$\mathbf\sigma=2G\mathbf\varepsilon+\lambda\,\mathrm{tr}(\mathbf\varepsilon)\mathbf I$$ with $$G=E/[2(1+\nu)]$$ and $$\lambda=E\nu/[(1+\nu)(1-2\nu)]$$.

Under plane stress, $$\sigma_{33}=\tau_{23}=\tau_{13}=0$$ and the out-of-plane strain $$\varepsilon_{33}=-\nu(\sigma_{11}+\sigma_{22})/E$$ is eliminated, giving the reduced stiffness
$$
\mathbf D^{(S)}=\dfrac{E}{1-\nu^2}\begin{bmatrix}1&\nu&0\\\nu&1&0\\0&0&(1-\nu)/2\end{bmatrix}.
$$

Under plane strain, $$\varepsilon_{33}=\gamma_{23}=\gamma_{13}=0$$ and the constraint stress $$\sigma_{33}=\nu(\sigma_{11}+\sigma_{22})/(1-\nu)$$ is eliminated, giving
$$
\mathbf D^{(E)}=\dfrac{E(1-\nu)}{(1+\nu)(1-2\nu)}\begin{bmatrix}1&\nu/(1-\nu)&0\\\nu/(1-\nu)&1&0\\0&0&(1-2\nu)/[2(1-\nu)]\end{bmatrix}.
$$
Both cases can be written in the unified form $$\mathbf D=E'/[(1-\nu'^2)]\begin{bmatrix}1&\nu'&0\\\nu'&1&0\\0&0&(1-\nu')/2\end{bmatrix}$$ with $$E'=E$$ and $$\nu'=\nu$$ for plane stress, and $$E'=E/(1-\nu^2)$$ and $$\nu'=\nu/(1-\nu)$$ for plane strain.
The source implements exactly this substitution and then sets the shear entry to $$G=E/[2(1+\nu)]$$, so the material response is linear and path independent.

!!! warning "implementation limitation"
    The out-of-plane component is reconstructed from the in-plane strain for recording and is not used in the stress update.

!!! note "developer note"
    Only the three in-plane components are stored as material state.

## Syntax

```text title="Elastic2D"
material Elastic2D (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# [4] double, density, default: 0.0
# [5] int, material type, plane stress = 0, plane strain = 1, default: 0
```

## Remarks

* The parser reads arguments in the order `E`, $$\nu$$, density and then the type flag, with density defaulting to zero and the flag defaulting to zero for plane stress.
* Any non-zero value of the material type selects plane strain because the constructor tests `material_type == 0 ? PlaneType::S : PlaneType::E`.
* The out-of-plane component is not part of the strain vector, so $$\sigma_{33}$$ in plane strain is reconstructed only for `S` and `MISES` recording as $$\nu E(\varepsilon_{11}+\varepsilon_{22})/[(1+\nu)(1-2\nu)]$$, and $$\varepsilon_{33}$$ in plane stress is never stored.
* Use [CP4](../../Element/Membrane/Plane/CP4.md) or [CP8](../../Element/Membrane/Plane/CP8.md) family elements, where the plane type comes from the material and not from the element token.
* For a three-dimensional constitutive law use the [`PlaneStress`](../Wrapper/PlaneStress.md) or [`PlaneStrain`](../Wrapper/PlaneStrain.md) wrapper instead of a native 2D model, as explained on [Material2D](Material2D.md).
* As $$\nu\to0.5$$ the plane-strain bulk modulus diverges and displacement-only elements lock volumetrically, so reduced-integration or mixed formulations are preferable for nearly incompressible response.
* The constructor does not apply `fabs` to its inputs, so positive $$E$$ and $$0\leq\nu<0.5$$ should be supplied explicitly.

!!! info "deviation from theory"
    The material type flag is interpreted as plane stress only when it is exactly zero, and every other integer silently selects plane strain.
    Unlike [IsotropicElastic3D](../Material3D/Elastic/IsotropicElastic3D.md), no input validation or absolute-value conversion is performed.

## Example

```text
material Elastic2D 1 2E5 .25
material Elastic2D 2 2E5 .25 0. 1
```

Material 1 is plane stress by default and material 2 is plane strain, with density omitted in both cases.
