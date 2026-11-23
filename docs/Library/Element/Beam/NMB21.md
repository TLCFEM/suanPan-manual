# NMB21

2D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)
* DoF Label: U1, U2, UR3

## Theory

`NMB21` is the two-dimensional member of the NMB family; see [NMB21E](NMB21E.md) for an end moment release and [NMB31](NMB31.md) for the three-dimensional member.
It is a concentrated-plasticity element that uses a single [SectionNM](../../Section/SectionNM/SectionNM.md) model to describe the axial-force-bending-moment interaction of the whole member.

Unlike a conventional fibre section, a `SectionNM` takes element-level deformations and resistances rather than sectional strain and curvature.

!!! info "deviation from theory"
    A conventional concentrated-plasticity member assigns independent springs to its two ends.
    A `SectionNM` model represents both end sections with one interaction surface and one set of history variables, so the two ends cannot develop independent hysteretic states.

The element transformation removes the rigid-body modes and gives the local deformation $\mathbf d_e=[d_1,d_2,d_3]^\mathrm T$, whose entries are the axial elongation and the two end rotations relative to the chord.
This vector is divided by the element length $L$ before it is passed to the section, and the section resistance contains the conjugate axial force and the two end moments.
The local stiffness and resistance are
$$
\mathbf k_e=\frac{1}{L}\mathbf k_s,\qquad \mathbf r_e=\mathbf r_s,
$$
where $\mathbf k_s$ and $\mathbf r_s$ are the tangent and resistance returned by the section, and both are transformed to the global system by the beam transformation.
The section defines an interaction surface in the normalised force space, together with a back force and an equivalent plastic strain, so that yielding is governed by a combined $N$-$M$ criterion rather than by independent uniaxial laws.

Because the inelastic response is lumped in one constitutive point, one element should resolve one plastic-hinge region, and mesh refinement controls the accuracy of the predicted hinge length.
When the nonlinear geometry switch is on, the corotational transformation `B2DC` and its geometric stiffness are used.

## References

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)
2. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer, 1998.

## Syntax

```text title="NMB21"
element NMB21 (1) (2) (3) (4) [5]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
```

## Remarks

Only `NM2D*` sections are supported.
There is no validation of the section attached, analysts shall make sure proper sections are used.
The section operates on the three element-level quantities $[N,M_i,M_j]$, so conventional fibre sections cannot be used here.
The element has no integration points along its length, which makes it much cheaper than [F21](F21.md) but also means the plastic hinge length is tied to the element length.
With the nonlinear geometry switch off, the `B2DL` transformation is used; with the switch on, `B2DC` adds the corotational update and the geometric stiffness.

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
