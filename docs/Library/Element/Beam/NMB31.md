# NMB31

3D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections

* Number of Nodes: 2
* Number of DoFs: 6 (Translation, Translation, Translation, Rotation, Rotation, Rotation)
* DoF Label: U1, U2, U3, UR1, UR2, UR3

## Background

`NMB31` is the three-dimensional member of the concentrated-plasticity NMB family and is described in full on the [NMB21](NMB21.md) page.
The attached `NM3D*` [SectionNM](../../Section/SectionNM/SectionNM.md) model works with element-level deformations of both ends and defines an interaction surface in the space of axial force $N$ and bending moments $M_y$, $M_z$.

The rigid-body-removal transformation produces six local deformation components, which are divided by the element length $L$ before being sent to the section.
The section tangent $\mathbf k_s$ and resistance $\mathbf r_s$ are converted to the element quantities by $\mathbf k_e=\mathbf k_s/L$ and $\mathbf r_e=\mathbf r_s$ and then transformed to the global system.
Torsion does not participate in the interaction surface and is treated as elastic, so biaxial bending and axial force are coupled while the torsional response is not.

!!! warning "implementation limitation"
    The `NM3D*` section assigns the torsional stiffness a penalty value of $10^3\max(4EI_S,4EI_W,EA)$ rather than a physical $GJ$, so neither torsional deformation nor torsional yielding is represented.
    Six local deformation components are passed to the section, but only the axial and two bending components enter the interaction surface.

The `B3DL` orientation is used for linear geometry and `B3DC` for the corotational formulation, and the orientation flag must match the element nonlinear geometry switch.

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```text title="NMB31"
element NMB31 (1) (2) (3) (4) (5) [6]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# (5) int, orientation tag
# [6] bool string, nonlinear geometry switch, default: false
```

## Remarks

1. Please check [`orientation`](Orientation.md) for its definition.
2. Only `NM3D*` sections are supported.
   There is no validation of the section attached, analysts shall make sure proper sections are used.
3. There is no information about torsion in the formulation.
   Thus, the local deformation only consists of five (instead of six) components.
   But for compatibility with general purpose beam transformation, six components are computed and stored at the element level as usual.
   The first five are sent to the section for computation of response.
   The torsion response is assumed to be elastic.
4. The element has no integration points along its length, so it should be used as a lumped-plasticity member with one element per hinge region.
5. The treatment of torsion is analogous to that of the force-based beam [F31](F31.md), which also keeps torsion elastic.

See [SectionNM](../../Section/SectionNM/SectionNM.md) for more information about the section.

## Output Type

This model supports the following additional history variables to be recorded.

| variable label | physical meaning          |
|----------------|---------------------------|
| BEAME          | local element deformation |
| BEAMS          | local element resistance  |

For example,

```text
hdf5recorder (1) Element BEAME (2...)
hdf5recorder (1) Element BEAMS (2...)
# (1) int, unique recorder tag
# (2...) int, tags of elements to record
```

Those are local deformation and resistance (with respect to the local coordinate system) of the element.
