# B31OS

3D Displacement Based Beam With Torsion and Warping

* Number of Nodes: 2
* Number of DoFs: 7 (Translation, Translation, Translation, Rotation, Rotation, Rotation, Warping)

## Reference

1. [Distributed plasticity analysis of steel building structural systems](https://www.proquest.com/dissertations-theses/distributed-plasticity-analysis-steel-building/docview/304696456/se-2)

## Syntax

```
element B31OS (1) (2) (3) (4) (5) [6] [7]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# (5) int, orientation tag
# [6] int, number of integration points, default: 6
# [7] int, nonlinear geometry switch, default: false
```

## Remarks

1. The Lobatto integration is used by default. The number of integration points ranges from 3 to 20.
2. Please check [`orientation`](Orientation.md) for its definition.
3. To use the corotational formulation for nonlinearity, please attach a corotational
   transformation [`B3DOSC`](Orientation.md).
4. The reference also introduced a circumvention of membrane locking.
   It _**is**_ implemented in this element.
   The Hermite shape function is used for the interpolation of $$\phi$$.
5. A 3D OS section is required for this element.

The Alemdar's thesis contains a few typos. The following expressions are confirmed to be correct and used in the
implementation.

1. Eq. 7.12 (Eq. 7.63)
2. Eq. 7.41
3. Eq. 7.69

Use `BEAMS` to record section forces.
Each section contains six force components, namely axial force, bending moment about major axis, bending moment about
minor axis, Wagner stress resultant, bi-moment and St. Venant torsion.

$$
\begin{bmatrix}
P&M_z&M_y&W&B&T_{sv}
\end{bmatrix}
$$

If five integration points are used, the output file contains $$6\times5=30$$ columns.

At element level, the implementation transforms global nodal quantities to local elemental quantities, namely,

1. uniform axial
2. strong axis bending near node
3. strong axis bending far node
4. weak axis bending near node
5. weak axis bending far node
6. torsion near node
7. torsion far node
8. warping near node
9. warping far node

Those quantities are further interpolated to sectional quantities, namely,

$$
\begin{bmatrix}
u'&v'&w'&v''&w''&\phi&\phi'&\phi''&\theta_{z,i}&\theta_{z,j}&\theta_{y,i}&\theta_{y,j}
\end{bmatrix}
$$

Not all quantities would be used by section state determination.
See [Fibre3DOS](../../Section/SectionOS/Fibre3DOS.md) for further explanation.

## Example

See [this](../../../Example/Structural/Statics/thin-walled-section.md) example.

Also see [benchmark](B31OS.BENCHMARK.md) problems.
