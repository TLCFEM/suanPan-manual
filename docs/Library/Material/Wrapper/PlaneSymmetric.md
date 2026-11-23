# PlaneSymmetric

Plane Symmetric Wrapper

Wraps a 3D host material model into a 2D plane symmetric model that can be used with 2D membrane elements.

## Theory

This wrapper is a specialisation of [PlaneStrain](PlaneStrain.md), which readers should consult for the Voigt ordering and the submatrix extraction.
Plain plane strain sets $\varepsilon_{33}=\gamma_{23}=\gamma_{13}=0$, whereas a plane symmetric state imposes that one out-of-plane normal direction behaves like an in-plane direction and that one out-of-plane shear vanishes or mirrors an in-plane shear.
The two tokens select which normal direction is identified with the thickness direction.

The implementation starts from the three in-plane strains $(\varepsilon_{11},\varepsilon_{22},\gamma_{12})$ and builds a zero six-vector.
For `PlaneSymmetric13` it copies $\varepsilon_{11}$ into $\varepsilon_{33}$ and $\gamma_{12}$ into $\gamma_{13}$.
For `PlaneSymmetric23` it copies $\varepsilon_{22}$ into $\varepsilon_{33}$ and $\gamma_{12}$ into $\gamma_{23}$.
The host is then evaluated with this reconstructed 3D strain, and the wrapper returns the in-plane stresses and the in-plane tangent submatrix exactly as [PlaneStrain](PlaneStrain.md) does.
For an isotropic host these strain constraints produce the corresponding normal-stress symmetry quoted in the Remarks, but for an anisotropic host the result depends on the coupling terms of the host tangent.
No local iteration is performed, since all imposed components are prescribed rather than solved for.

!!! warning "imposed strains versus quoted stress symmetry"
    The Remarks below state the stress equalities $\sigma_{11}=\sigma_{33}$ with $\tau_{12}=\tau_{32}$ and $\sigma_{22}=\sigma_{33}$ with $\tau_{12}=\tau_{31}$.
    The wrapper actually imposes strain constraints, namely $\varepsilon_{33}=\varepsilon_{11}$ and $\gamma_{13}=\gamma_{12}$ for `PlaneSymmetric13`, and $\varepsilon_{33}=\varepsilon_{22}$ and $\gamma_{23}=\gamma_{12}$ for `PlaneSymmetric23`.
    Those stress equalities follow only for an isotropic host with the corresponding elastic symmetry, while an anisotropic host can violate them because of coupling terms in its tangent.

!!! note "developer note"
    The strain constraints are implemented in `PlaneStrain.cpp`.

## Syntax

```text title="PlaneSymmetric"
material PlaneSymmetric13 (1) (2)
material PlaneSymmetric23 (1) (2)
# (1) int, unique material tag
# (2) int, 3D reference material tag
```

## Remarks

1. The token `PlaneSymmetric13` indicates $$\sigma_{11}=\sigma_{33}$$ and $$\tau_{12}=\tau_{32}$$.
2. The token `PlaneSymmetric23` indicates $$\sigma_{22}=\sigma_{33}$$ and $$\tau_{12}=\tau_{31}$$.

The parser maps `PlaneSymmetric13` and `PlaneSymmetric23` to the same class as [PlaneStrain](PlaneStrain.md) with an internal symmetry flag, so all three tokens accept exactly two arguments.
The underlying host must be a 3D material and must not be nonlocal, matching the restriction of [PlaneStrain](PlaneStrain.md).
The wrapper inherits the host density and extracts the $3\times3$ in-plane initial stiffness from the host.
Use [Axisymmetric](Axisymmetric.md) instead when the hoop strain arises from a radial displacement in a true body of revolution, since that element supplies the hoop strain directly.

## References

- [ISBN 978-1-4398-0247-2](https://search.worldcat.org/search?q=bn:9781439802472)
- [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
