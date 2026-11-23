# ShellBase

The `ShellBase` class is a base class for all shell elements.
It provides basic methods to convert displacement from global to local, or convert resistance and stiffness from local to global.

## Background

Each shell node has six DoFs: three membrane components and three plate components.
`ShellBase` derives the local direction cosines from the element geometry and assembles the membrane and plate contributions into the full element resistance and stiffness.
In a nonlinear geometry analysis the transformation is recomputed from the trial displaced shape.

A flat shell element is obtained by superposing a two-dimensional membrane model and a plate-bending model on the same planar reference surface.

In the local frame the membrane contributes the in-plane translations $$u,v$$ and the drilling rotation $$\theta_z$$, while the plate contributes the transverse displacement $$w$$ and the bending rotations $$\theta_x,\theta_y$$.

The global ordering of the six nodal DoFs is $$(U_1,U_2,U_3,UR_1,UR_2,UR_3)$$, and the implementation uses the index sets $$m=\{0,1,5\}$$ for the local membrane block and $$p=\{2,3,4\}$$ for the local plate block.

For a node with local membrane vector $$\mathbf d_m$$ and plate vector $$\mathbf d_p$$, the strain at a fibre of thickness coordinate $$z$$ is

$$
\mathbf\varepsilon(z)=\mathbf B_m\mathbf d_m+z\,\mathbf B_p\mathbf d_p ,
$$

with the in-plane strain vector $$(u_{,x},v_{,y},u_{,y}+v_{,x})$$ and the plate curvature used for $$\mathbf B_p$$.

Integrating this strain through the thickness gives the local stiffness in block form

$$
\mathbf K_{\rm loc}=
\begin{bmatrix}
\mathbf K_{mm} & \mathbf K_{mp}\\
\mathbf K_{pm} & \mathbf K_{pp}
\end{bmatrix},
\qquad
\begin{aligned}
\mathbf K_{mm}&=\int\mathbf B_m^{\mathsf T}\mathbf D\mathbf B_m\,dV,\\
\mathbf K_{mp}&=\int z\,\mathbf B_m^{\mathsf T}\mathbf D\mathbf B_p\,dV,\\
\mathbf K_{pp}&=\int z^2\,\mathbf B_p^{\mathsf T}\mathbf D\mathbf B_p\,dV,
\end{aligned}
$$

so the bending stiffness is synthesized from the two-dimensional material matrix $$\mathbf D$$ and the $$z$$ and $$z^2$$ moments.

`ShellBase::reshuffle` inserts these three-by-three blocks into the six-DoF-per-node layout, and the fibre coordinate is evaluated at Gauss points with $$z=\xi t/2$$ and weights proportional to $$t$$.

The local triad is built from the first three nodes, with $$\mathbf e_1$$ along $$\mathbf x_2-\mathbf x_1$$, $$\mathbf e_3$$ normal to the plane spanned by $$\mathbf x_2-\mathbf x_1$$ and $$\mathbf x_3-\mathbf x_1$$, and $$\mathbf e_2=\mathbf e_3\times\mathbf e_1$$.

These three unit vectors are stored as the columns of the rotation matrix $$\mathbf R$$, so nodal vectors and stiffnesses are transformed with $$\mathbf d_{\rm loc}=\mathbf R^{\mathsf T}\mathbf d_{\rm glob}$$ and $$\mathbf K_{\rm glob}=\mathbf T\mathbf K_{\rm loc}\mathbf T^{\mathsf T}$$, where $$\mathbf T={\rm diag}(\mathbf R,\ldots,\mathbf R)$$.

When the nonlinear-geometry switch is active, the triad is recomputed from the trial displaced nodal positions and the derivative of the triad with respect to displacement contributes an additional geometric stiffness through `transform_to_global_geometry`, giving a corotational-style large-displacement formulation with a locally linear response.

!!! info "deviation from theory"
    This is not a fully nonlinear corotational formulation, because the material response is still evaluated in the local frame with small-strain kinematics.
    The geometric stiffness comes only from the derivative of the rigid-body triad, not from finite-strain measures.
    The local triad is taken from the first three nodes, so the local plane is fixed by that choice rather than by a best-fit plane through all nodes.

## Remarks

`ShellBase` is not a user-instantiable element and has no `element ShellBase` command.
Use one of its derived elements instead: [`DKTS3`](DKTS3.md), [`S4`](S4.md) or [`SGCMS`](SGCMS.md).

* Each derived element takes a single two-dimensional material tag, and the same material matrix is used for membrane and bending action through the $$z$$ and $$z^2$$ integrals.

!!! warning "implementation limitation"
    There is no separate membrane material, plate material or section definition in these elements.
    Layered or sandwich shells are only possible through the material's own through-thickness response.
    Strongly warped geometry is not checked.

!!! note "developer note"
    The planarity warning is commented out in the source.

* The drilling rotation `UR3` is supplied only by the membrane part, so an Allman- or GQ12-type membrane can leave a uniform drilling mode without stiffness; see [Allman](../Membrane/Drilling/Allman.md).
* The local coordinates are projections of the global nodal coordinates onto the local plane, and the explicit non-planarity warning is commented out in the source, so a strongly warped element should be used with care.
* With `nlgeom` enabled the element follows the "large displacement, small deformation" assumption because the local material response remains linear.
* The separate `SectionShell` abstraction, for example its `Homogeneous` implementation, performs a similar eccentricity-based thickness integration for section-aware elements, but the flat shells listed here integrate their layers internally.
* [DKTS3](DKTS3.md) uses a three-node drilling membrane plus [DKT3](../Plate/DKT3.md) plate bending, [S4](S4.md) uses [GQ12](../Membrane/Drilling/GQ12.md) plus [Mindlin](../Plate/Mindlin.md), and [SGCMS](SGCMS.md) uses [SGCMQ](../Membrane/Drilling/GCMQ.md) plus [DKT4](../Plate/DKT4.md).

## References

1. [ISBN 978-0-13-301458-7](https://search.worldcat.org/search?q=bn:9780133014587)
2. [ISBN 978-0-7506-5050-2](https://search.worldcat.org/search?q=bn:9780750650502)
3. [ISBN 978-0-471-35605-9](https://search.worldcat.org/search?q=bn:9780471356059)
4. [10.1016/0045-7825(89)90124-2](https://doi.org/10.1016/0045-7825(89)90124-2)
