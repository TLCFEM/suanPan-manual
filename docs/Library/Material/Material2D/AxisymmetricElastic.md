# AxisymmetricElastic

Axisymmetric Elastic Model

## Background

Axisymmetric analysis applies when the geometry, loading and material are invariant under rotation about a fixed axis, so that all field quantities depend only on the radial coordinate $r$ and the axial coordinate $z$.
The only non-zero displacement components are $u_r(r,z)$ and $u_z(r,z)$, and the element assembles the engineering strain vector
$$
\boldsymbol\varepsilon=\begin{bmatrix}\varepsilon_{rr}&\varepsilon_{\theta\theta}&\varepsilon_{zz}&\gamma_{rz}\end{bmatrix}^{\mathrm T}=\begin{bmatrix}\partial u_r/\partial r&u_r/r&\partial u_z/\partial z&\partial u_r/\partial z+\partial u_z/\partial r\end{bmatrix}^{\mathrm T}.
$$
The hoop strain $u_r/r$ is the term that distinguishes an axisymmetric solid from a plane-strain solid, and it must be supplied by the element strain-displacement matrix rather than by the material.

!!! warning "implementation limitation"
    The material does not compute the hoop strain $u_r/r$ itself and expects the element to supply it in the strain vector.
    Using it with an element that does not generate $u_r/r$ gives a plane-strain response instead of an axisymmetric one.

!!! note "developer note"
    The fourth strain slot is multiplied directly by the shear modulus.

With the Lamé constants $G=E/[2(1+\nu)]$ and $\lambda=E\nu/[(1+\nu)(1-2\nu)]$, the material returns
$$
\boldsymbol\sigma=\begin{bmatrix}\sigma_{rr}\\\sigma_{\theta\theta}\\\sigma_{zz}\\\tau_{rz}\end{bmatrix}=\begin{bmatrix}\lambda+2G&\lambda&\lambda&0\\\lambda&\lambda+2G&\lambda&0\\\lambda&\lambda&\lambda+2G&0\\0&0&0&G\end{bmatrix}\boldsymbol\varepsilon.
$$
This matrix is the upper-left $4\times4$ block of the six-dimensional isotropic elasticity tensor, which is exactly what `tensor::isotropic_stiffness(elastic_modulus, poissons_ratio)(span(0,3), span(0,3))` extracts in the source.
The shear entry is the engineering shear modulus $G$ because suanPan stores the engineering shear strain $\gamma_{rz}=2\varepsilon_{rz}$ in the fourth slot.

## Syntax

```text title="AxisymmetricElastic"
material AxisymmetricElastic (1) (2) (3) [4]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# [4] double, density, default: 0.0
```

## Remarks

* The strain and stress vectors contain four entries in the order $(\varepsilon_{rr},\varepsilon_{\theta\theta},\varepsilon_{zz},\gamma_{rz})$ and $(\sigma_{rr},\sigma_{\theta\theta},\sigma_{zz},\tau_{rz})$.
* Use [CAX4](../../Element/Membrane/Axisymmetric/CAX4.md) or [CAX8](../../Element/Membrane/Axisymmetric/CAX8.md) elements, which generate the hoop strain $u_r/r$ from the nodal radial displacements.
* To use a three-dimensional constitutive law in an axisymmetric analysis, use the [`Axisymmetric`](../Wrapper/Axisymmetric.md) wrapper, which extracts components $(0,1,2,3)$ of the full 3D response.
* Poisson's ratio must stay below $0.5$ because the bulk modulus scales with $1/(1-2\nu)$, and values approaching $0.5$ lead to near-incompressible volumetric locking in displacement-only elements.
* Unlike [IsotropicElastic3D](../Material3D/Elastic/IsotropicElastic3D.md), the constructor does not take absolute values of the elastic modulus and Poisson's ratio, so the signs supplied by the user are passed through unchanged.
* This model has `PlaneType::A`, so [Material2D](Material2D.md) does not provide `S`, `SP`, `E` or `EP` output for it and only the common history outputs remain available.

!!! info "deviation from theory"
    Standard elasticity requires $E>0$ and $-1<\nu<0.5$, but this class performs no validation or sign correction.
    A negative input therefore produces a negative stiffness rather than the physical modulus.
