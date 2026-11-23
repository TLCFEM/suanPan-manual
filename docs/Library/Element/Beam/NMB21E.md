# NMB21E

2D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections And End Moment Release

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)
* DoF Label: U1, U2, UR3

## Background

`NMB21E` extends the concentrated-plasticity model [NMB21](NMB21.md) by releasing the bending moment at one end of the member.
The general formulation of the element and its `SectionNM` interaction law are described on the [NMB21](NMB21.md) page.

Let $$a$$ denote the released deformation component, which is the rotation at node $$i$$ for `NMB21EL` and the rotation at node $$j$$ for `NMB21EH`, and let $$b$$ collect the remaining components.
After the section returns its trial tangent $$\mathbf k_s$$ and resistance $$\mathbf r_s$$, the released deformation is adjusted so that the released moment vanishes,
$$
d_a\leftarrow d_a-\dfrac{r_{s,a}L+\mathbf k_{s,ab}\Delta\mathbf d_b}{k_{s,aa}}.
$$
The resistance and stiffness are then statically condensed to the retained components,
$$
\mathbf r_b'=\mathbf r_{s,b}-\mathbf k_{s,ba}k_{s,aa}^{-1}r_{s,a},\qquad
\mathbf k_{bb}'=\mathbf k_{s,bb}-\mathbf k_{s,ba}k_{s,aa}^{-1}\mathbf k_{s,ab}.
$$
This condensation is performed in closed form, which is why the implementation is non-iterative.

!!! info "deviation from theory"
    The released deformation is computed from the section tangent and resistance of the current trial state and the section is then updated only once, so the released moment vanishes only to the accuracy of that single update.
    A classical static condensation solves the release condition together with the constitutive update to convergence.

The condensed quantities are divided by the element length and transformed to the global system exactly as in [NMB21](NMB21.md).

## References

1. [10.1061/JSENDH.STENG-12176](https://doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```text title="NMB21E"
element NMB21EL (1) (2) (3) (4) [5]
element NMB21EH (1) (2) (3) (4) [5]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
```

## Remarks

Only `NM2D*` sections are supported.
There is no validation of the section attached, analysts shall make sure proper sections are used.

The `NMB21EL` element releases the moment at low node `i` and the `NMB21EH` element releases the moment at high node `j`.

A non-iterative algorithm is used.
Only one end can be released per element, since the release is selected by the element name and there is no option for two releases.
The released component is eliminated by static condensation with the current section tangent, so the element stiffness remains symmetric for a symmetric section tangent.
The nonlinear geometry switch has the same corotational meaning as in [NMB21](NMB21.md).

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
