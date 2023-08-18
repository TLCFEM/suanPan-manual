# NMB21

2D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)

## Reference

1. [10.1061/JSENDH/STENG-12176](http://dx.doi.org/10.1061/JSENDH/STENG-12176)

## Syntax

```
element NMB21 (1) (2) (3) (4) [5]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
```

## Remarks

Only `NM2D*` sections are supported. There is no validation of section attached, analysts shall make sure proper
sections are used.

See [SectionNM](../../Section/SectionNM/SectionNM.md) for more information about the section.

## Output Type

The `NMB21` element additional support recording element deformation and resistance via the `BEAME` and `BEAMS` tokens.

For example,

```text
hdf5recorder (1) Element BEAME (2...)
hdf5recorder (1) Element BEAMS (2...)
# (1) int, unique recorder tag
# (2...) int, tags of elements to record
```

Those are local deformation and resistance (with respect to the local coordinate system) of the element.
