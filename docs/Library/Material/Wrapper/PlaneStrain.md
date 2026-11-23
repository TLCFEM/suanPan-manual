# PlaneStrain

Plane Strain Wrapper

Wraps a 3D host material model into a 2D plane strain model that can be used with 2D membrane elements.

## Theory

suanPan orders the six 3D Voigt strain entries as $(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$, with engineering shears $\gamma_{ij}=2\varepsilon_{ij}$.
A plane strain state describes a body whose dimension in the $x_3$ direction is large or fully constrained, so that out-of-plane deformation is suppressed.
The kinematic conditions are

$$
\varepsilon_{33}=0,\qquad\gamma_{23}=0,\qquad\gamma_{13}=0,
$$

while the stress components $\sigma_{33}$, $\tau_{23}$ and $\tau_{13}$ are generally nonzero and act as reaction stresses.
This is the opposite of [PlaneStress](PlaneStress.md), where the out-of-plane stresses vanish and the out-of-plane strains are unknown.

Let $\mathbf e^{\mathrm{2D}}=(\varepsilon_{11},\varepsilon_{22},\gamma_{12})$ be the strain vector furnished by a membrane element.
The wrapper embeds it in the 3D vector by selecting indices $F=\{0,1,3\}$ and filling all remaining entries with zero,

$$
\mathbf e^{\mathrm{3D}}=(\varepsilon_{11},\varepsilon_{22},0,\gamma_{12},0,0).
$$

The host is driven with this full strain, and the wrapper extracts the in-plane stress and the in-plane tangent submatrix,

$$
\mathbf s^{\mathrm{2D}}=\mathbf s^{\mathrm{3D}}_{F},
\qquad
\mathbf D^{\mathrm{2D}}=\mathbf D^{\mathrm{3D}}_{F,F}.
$$

No local iteration is necessary because the missing strains are specified rather than solved for.
For a linear isotropic host with modulus $E$ and Poisson ratio $\nu$ this gives

$$
\mathbf D^{\mathrm{2D}}=\dfrac{E}{(1+\nu)(1-2\nu)}
\begin{bmatrix}
1-\nu&\nu&0\\
\nu&1-\nu&0\\
0&0&\dfrac{1-2\nu}{2}
\end{bmatrix}.
$$

The apparent in-plane stiffness grows without bound as $\nu\to0.5$, reflecting the fact that a fully constrained incompressible body cannot change volume.
For this reason a 3D nearly incompressible host requires a formulation that admits $\nu<0.5$, and the wrapper simply propagates the host tangent.

The same class also implements the two symmetry variants `PlaneSymmetric13` and `PlaneSymmetric23`.
They replace two of the zero out-of-plane entries by copies of in-plane entries before the host is evaluated.
The `13` variant sets $\varepsilon_{33}=\varepsilon_{11}$ and $\gamma_{13}=\gamma_{12}$, while the `23` variant sets $\varepsilon_{33}=\varepsilon_{22}$ and $\gamma_{23}=\gamma_{12}$.
Both variants are documented together on [PlaneSymmetric](PlaneSymmetric.md).

## Syntax

```text title="PlaneStrain"
material PlaneStrain (1) (2)
# (1) int, unique tag
# (2) int, 3D material tag
```

The response of attached 3D material model will be output when recorded.

## Remarks

The host material must be a registered 3D model, and nonlocal 3D hosts are explicitly rejected during initialization.
The wrapper copies the host density and uses the in-plane submatrix of the host initial stiffness as its own initial stiffness.
Use this wrapper with 2D membrane elements that possess out-of-plane thickness and represent a long or constrained body.
For a thin plate or shell use [PlaneStress](PlaneStress.md), and for a body of revolution use [Axisymmetric](Axisymmetric.md), whose hoop strain is computed by the element from the radial displacement.
For uniaxial stress states use [Uniaxial](Uniaxial.md), which is based on the same condensation idea as plane stress but keeps only the axial component.
As with all wrappers, `record` forwards to the host, so recorded 3D stresses include the reaction components that the element does not see.

## References

- [ISBN 978-1-4398-0247-2](https://search.worldcat.org/search?q=bn:9781439802472)
- [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
- [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
