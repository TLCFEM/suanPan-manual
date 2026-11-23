# MVLEM

Multiple Vertical Line Element Model

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)
* DoF Label: U1, U2, UR3

The `MVLEM` element is often used in modelling walls.
It is in fact a simplified beam element with shear response.

Personally I do not recommend the usage of this element in any case.

## Theory

The multiple-vertical-line-element model idealises a planar wall as two rigid boundary bars connected by a row of uniaxial axial springs and one horizontal shear spring.
It was developed to reproduce the flexural response through axial fibre action and the shear response through a single shear spring with only six degrees of freedom per element.

### Kinematics

The local displacement vector is $$\mathbf a=[u_1,v_1,\theta_1,u_2,v_2,\theta_2]^\mathrm T$$, where $$u$$ and $$v$$ are the horizontal and vertical translations of the bottom and top rigid bars and $$\theta$$ are their rotations.
Let $$h$$ be the wall height, $$c\in[0,1]$$ the normalised height of the shear spring measured from the bottom, and $$x_i$$ the eccentricity of vertical fibre $$i$$ from the centroidal axis.
The deformation of vertical spring $$i$$ and of the shear spring are obtained from the rigid-bar kinematics,
$$
\Delta l_i=\begin{bmatrix}0&-1&-x_i&0&1&x_i\end{bmatrix}\mathbf a,\qquad
\Delta l_H=\begin{bmatrix}1&0&-ch&-1&0&(c-1)h\end{bmatrix}\mathbf a.
$$
With a uniaxial law of stiffness $$k$$ for a spring, its force is $$f=k\,\Delta l$$, where $$k=E A/L$$ for a linear spring and $$L=h$$ for the vertical springs.

### Stiffness matrix

Denote by $$k_i$$ the stiffness of vertical spring $$i$$ and by $$k_H$$ the stiffness of the shear spring, and let sums run over all vertical springs.
The local stiffness matrix is the sum $$\mathbf K=\mathbf K^V+\mathbf K^H$$, where the vertical springs control flexure and the shear spring controls shear:
$$
\mathbf K=\begin{bmatrix}
k_H&0&-chk_H&-k_H&0&(c-1)hk_H\\
0&\sum k_i&\sum k_ix_i&0&-\sum k_i&-\sum k_ix_i\\
-chk_H&\sum k_ix_i&c^2h^2k_H+\sum k_ix_i^2&chk_H&-\sum k_ix_i&c(1-c)h^2k_H-\sum k_ix_i^2\\
-k_H&0&chk_H&k_H&0&(1-c)hk_H\\
0&-\sum k_i&-\sum k_ix_i&0&\sum k_i&\sum k_ix_i\\
(c-1)hk_H&-\sum k_ix_i&c(1-c)h^2k_H-\sum k_ix_i^2&(1-c)hk_H&\sum k_ix_i&(1-c)^2h^2k_H+\sum k_ix_i^2
\end{bmatrix}.
$$
In the implementation $$k_i=(E_{c,i}A_{c,i}+E_{s,i}A_{s,i})/h$$ and $$k_H=A_\mathrm{total}G_H/h$$, where $$A_\mathrm{total}$$ is the sum of all fibre areas and $$G_H$$ is the tangent of the shear material.
The axial forces of the vertical springs and the shear force are computed from the same spring deformations and assembled into the local resistance vector, which is then transformed to the global system.

!!! warning "implementation limitation"
    The element is constructed with `nlgeom = false`, so no corotational update or geometric stiffness is available for walls undergoing large rotations.
    Flexure and shear enter the stiffness as a direct sum of $$\mathbf K^V$$ and $$\mathbf K^H$$, with no interaction surface coupling them.

## Syntax

```text title="MVLEM"
element MVLEM (1) (2) (3) (4) (5) ((6) (7) (8) (9) (10)...)
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag of shear spring
# (5) double, height of shear spring, ranges from 0 to 1
# (6) double, fibre width
# (7) double, fibre thickness
# (8) double, reinforcement ratio of target fibre
# (9) int, concrete material (host) tag
# (10) int, steel material tag
```

## Remarks

1. Parameters `(6)` to `(10)` form a group of parameters that define a single fibre.
   If there are multiple fibres, which is often the case, repeat the five-parameter group for each fibre.
2. Parameter `(5)` is the normalised shear-spring height $$c$$, so the spring is placed at $$ch$$ above the bottom node and $$c$$ should lie between 0 and 1.
3. For each fibre, the steel area is $$A_s=BHR$$ and the concrete area is $$A_c=BH(1-R)$$, where $$R$$ is the reinforcement ratio given by `(8)`.
4. The fibre eccentricities $$x_i$$ are computed automatically by centring the cumulative fibre widths about the wall centroid, so the widths should add up to the wall width.
5. The shear material and all fibre materials must be uniaxial `Material1D` models; a warning is issued if the shear material is not, while fibre material types are not checked.
6. Flexure and shear are uncoupled by construction, so shear-flexure interaction and fixed crack-angle effects are outside the scope of this element.
7. No geometric nonlinearity or corotational formulation is implemented for this element.
8. The parser reads the trailing arguments as repeating groups of five, so the number of material tags must match the number of fibre groups.

!!! warning "implementation limitation"
    Only the shear material is checked for type at initialisation, while the concrete and steel materials are used as one-dimensional materials without validation and will fail later at runtime if incompatible.

## Example

The following defines a wall of three nodes with two fibres of width $$0.2$$, thickness $$1$$ and reinforcement ratio $$0.02$$, using an elastic shear material.

```text
material ConcreteTsai 1 3E4 30. 2. 2. 2. .2 2E-3 1E-4
material MPF 2 2E5 400 .02
material Elastic1D 3 2E6
element MVLEM 1 1 2 3 .4 .2 1 .02 1 2 .2 1 .02 1 2
```

## References

1. Analytical modeling of R/C structural walls
2. [10.1201/9781482296662-15](https://doi.org/10.1201/9781482296662-15)
3. [10.14359/51663105](https://doi.org/10.14359/51663105)
