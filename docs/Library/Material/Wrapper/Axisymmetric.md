# Axisymmetric

Axisymmetric Wrapper

Wraps a 3D host material model into a 2D axisymmetric model that can be used with 2D axisymmetric elements such as [CAX4](../../Element/Membrane/Axisymmetric/CAX4.md) and [CAX8](../../Element/Membrane/Axisymmetric/CAX8.md).

## Theory

An axisymmetric body has geometry, loading and material properties independent of the circumferential coordinate $$\theta$$, with vanishing circumferential displacement and radial and axial displacements $$u_r(r,z)$$ and $$u_z(r,z)$$.
The nonzero small-strain components in cylindrical coordinates are

$$
\varepsilon_{rr}=\dfrac{\partial u_r}{\partial r},
\qquad
\varepsilon_{zz}=\dfrac{\partial u_z}{\partial z},
\qquad
\varepsilon_{\theta\theta}=\dfrac{u_r}{r},
\qquad
\gamma_{rz}=\dfrac{\partial u_r}{\partial z}+\dfrac{\partial u_z}{\partial r}.
$$

The hoop strain $$\varepsilon_{\theta\theta}=u_r/r$$ is therefore not zero and is computed by the element from the radial displacement and the current radius.
Axisymmetric elements in suanPan pass a four-component vector $$(\varepsilon_{rr},\varepsilon_{zz},\varepsilon_{\theta\theta},\gamma_{rz})$$ to the material, and the integration weight contains the factor $$2\pi r$$.
This is the essential difference from [PlaneStrain](PlaneStrain.md), which sets the out-of-plane strain to zero and is appropriate for a long prismatic body rather than a body of revolution.

The wrapper selects indices $$F=\{0,1,2,3\}$$ of the 3D Voigt ordering, that is $$(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12})$$ with $$x_1$$ radial, $$x_2$$ axial and $$x_3$$ hoop.
It embeds the four element strains into a six-component host strain with the two out-of-plane shear entries $$\gamma_{23}$$ and $$\gamma_{13}$$ set to zero, and extracts the matching four stresses and the $$4\times4$$ tangent submatrix.
No local iteration is needed because every strain component is supplied by the element, just as for plane strain.
On the symmetry axis the regular solution has $$u_r\to0$$ and $$\varepsilon_{\theta\theta}\to\varepsilon_{rr}$$, so the radial and hoop directions become identical.

!!! warning "implementation limitation"
    The wrapper does not enforce the symmetry-axis condition itself, it simply forwards the four strains supplied by the element.
    The axisymmetric elements compute the hoop strain from $$u_r/r$$ and divide by the radius at the integration point, so a zero-radius integration point is singular and the limiting equality $$\varepsilon_{\theta\theta}=\varepsilon_{rr}$$ is never imposed explicitly.

## Syntax

```text title="Axisymmetric"
material Axisymmetric (1) (2)
# (1) int, unique tag
# (2) int, 3D material tag
```

The response of attached 3D material model will be output when recorded.

## Remarks

The host must be a registered 3D material, and the wrapper inherits its density and uses the corresponding submatrix of the host initial stiffness.
Pair the wrapper only with axisymmetric elements whose reported plane type is `A`, such as [CAX4](../../Element/Membrane/Axisymmetric/CAX4.md) or [CAX8](../../Element/Membrane/Axisymmetric/CAX8.md); other elements report a three-component strain and are incompatible.
The global $$x$$ coordinate of an axisymmetric mesh is the radius and the global $$y$$ coordinate is the axis of revolution, so negative or zero radii are not admissible.
Use [PlaneSymmetric](PlaneSymmetric.md) when the equality of two strain directions must be imposed by the material wrapper rather than derived from the element kinematics.
For a thin shell of revolution use a shell element instead, since a membrane or continuum axisymmetric model cannot represent bending through the wall.
Recorded quantities are forwarded to the 3D host, so the hoop stress appears as the third stress component in the output.

## References

- [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
- [ISBN 978-1-4398-0247-2](https://search.worldcat.org/search?q=bn:9781439802472)
- [Axisymmetric elements](https://search.worldcat.org/search?q=ti:Axisymmetric+elements)
