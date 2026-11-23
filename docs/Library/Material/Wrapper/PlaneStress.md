# PlaneStress

Plane Stress Wrapper

Wraps a 3D host material model into a 2D plane stress model that can be used with 2D membrane elements.

## Theory

suanPan stores a symmetric second-order tensor in Voigt form, using $\mathbf e=(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$ for strain and $\mathbf s=(\sigma_{11},\sigma_{22},\sigma_{33},\tau_{12},\tau_{23},\tau_{13})$ for stress.
The shear entries are engineering shears, $\gamma_{ij}=2\varepsilon_{ij}$ for $i\ne j$, so that the inner product $\mathbf s\cdot\mathbf e$ equals the tensor contraction $\boldsymbol\sigma:\boldsymbol\varepsilon$.
A plane stress state models a thin body loaded in its own plane whose faces are traction free, so that $\sigma_{33}=\tau_{23}=\tau_{13}=0$.
The out-of-plane strains $\varepsilon_{33}$, $\gamma_{23}$ and $\gamma_{13}$ are not prescribed by the kinematics, since they arise from Poisson coupling and from the constitutive law.

Partition the tensors into in-plane components $I=(11,22,12)$ and out-of-plane components $O=(33,23,13)$.
The host material defines $\mathbf s=\mathbf s(\mathbf e)$ and its consistent tangent $\mathbf D=\partial\mathbf s/\partial\mathbf e$, which can be partitioned as

$$
\begin{bmatrix}\mathbf s_I\\\mathbf s_O\end{bmatrix}=
\begin{bmatrix}\mathbf D_{II}&\mathbf D_{IO}\\\mathbf D_{OI}&\mathbf D_{OO}\end{bmatrix}
\begin{bmatrix}\mathbf e_I\\\mathbf e_O\end{bmatrix}.
$$

Given the in-plane strain supplied by the element, the wrapper solves the three local equations $\mathbf s_O(\mathbf e_I,\mathbf e_O)=\mathbf 0$ for the three unknown out-of-plane strains.
Linearising these equations at the current trial state gives the correction

$$
\Delta\mathbf e_O=-\mathbf D_{OO}^{-1}\left(\mathbf s_O+\mathbf D_{OI}\Delta\mathbf e_I\right),
$$

where $\Delta\mathbf e_I$ is the in-plane strain increment.
The plane stress stress and tangent are then obtained by static condensation,

$$
\mathbf s_I^{\mathrm{2D}}=\mathbf s_I-\mathbf D_{IO}\mathbf D_{OO}^{-1}\mathbf s_O,
\qquad
\mathbf D^{\mathrm{2D}}=\mathbf D_{II}-\mathbf D_{IO}\mathbf D_{OO}^{-1}\mathbf D_{OI}.
$$

For a linear isotropic host the result is the familiar matrix

$$
\mathbf D^{\mathrm{2D}}=\dfrac{E}{1-\nu^2}
\begin{bmatrix}
1&\nu&0\\
\nu&1&0\\
0&0&\dfrac{1-\nu}{2}
\end{bmatrix},
$$

which differs distinctly from the plane strain matrix, especially as $\nu$ approaches $0.5$.

The implementation is shared with [Uniaxial](Uniaxial.md) and [OS146](OS146.md) through the `StressWrapper` base class.
The active set is `F1={0,1,3}`, namely $\sigma_{11}$, $\sigma_{22}$ and $\tau_{12}$, and the complementary set `F2={2,4,5}` is driven to zero by the condensation above.
With the default `[3]=1` the wrapper performs one Newton update using the host trial tangent and accepts the result without rechecking the residual.
Setting `[3]` greater than one activates local iterations that repeatedly evaluate the host, solve $\mathbf D_{OO}\Delta\mathbf e_O=-\mathbf s_O$ and stop when the correction drops below the tolerance or the residual is small.

!!! warning "implementation limitation"
    With the default `[3]=1` the constrained stresses $\mathbf s_O$ are not exactly zero after the update.
    The reported in-plane stress is condensed with the newly evaluated host tangent, which does not remove that residual.

!!! note "developer note"
    The correction is formed from the host stress and tangent of the previous step and applied only once.
    With `[3]>1` the convergence test uses a tolerance relative to the first correction and the counter is tested before each evaluation, so at most `[3]-1` corrections are applied.

The returned stiffness is recomputed by condensation from the host trial tangent, so it is the consistent plane stress tangent when the host tangent is consistent.
Nonlocal history variables of the host, if any, are appended after the six strain components and carried through unchanged.

## Syntax

```text title="PlaneStress"
material PlaneStress (1) (2) [3]
# (1) int, unique tag
# (2) int, 3D material tag
# [3] int, maximum iteration, default: 1
```

The response of attached 3D material model will be output when recorded.

By default, a non-iterative algorithm is implemented.
If the strain increment is large, the algorithm may not converge.
In this case, the optional argument `[3]` can be used to activate local iterations.
If it is greater than one, the algorithm will perform local iteration up to `[3]` times.

## Remarks

The host material must be a registered 3D model, and the wrapper inherits its density.
The wrapper reports the 2D stress and stiffness to the element, while `record` forwards to the host so that recorded 3D quantities retain their original layout.
See [Material2D](../../Material/Material2D/Material2D.md) for the in-plane remapping of recorded stresses.
Use this wrapper with membrane, plate or shell elements whose material plane is the $x_1$–$x_2$ plane.
For a thick or constrained body use [PlaneStrain](PlaneStrain.md) instead, and for a body of revolution use [Axisymmetric](Axisymmetric.md).
For an open thin-walled section use [OS146](OS146.md), which condenses a different set of stress components.
A host with a singular out-of-plane tangent block $\mathbf D_{OO}$ cannot be used, since the condensation requires its inverse.
Large strain increments combined with yielding or softening can leave a noticeable residual in the single-pass mode, so increase `[3]` or reduce the global step size in that case.
Near incompressibility makes $\mathbf D_{OO}$ poorly conditioned and local iteration particularly valuable.

## References

- [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
- [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
- [Plane stress and plane strain](https://search.worldcat.org/search?q=ti:Plane+stress+and+plane+strain)
