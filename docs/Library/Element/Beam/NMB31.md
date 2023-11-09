# NMB31

3D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections

* Number of Nodes: 2
* Number of DoFs: 6 (Translation, Translation, Translation, Rotation, Rotation, Rotation)

## Reference

1. [10.1061/JSENDH.STENG-12176](http://dx.doi.org/10.1061/JSENDH.STENG-12176)

## Syntax

```
element NMB31 (1) (2) (3) (4) (5)
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# (5) int, orientation tag
```

## Remarks

1. Please check [`orientation`](Orientation.md) for its definition.
2. Only `NM3D*` sections are supported. There is no validation of section attached, analysts shall make sure proper
   sections are used.
3. There is no information about torsion in the formulation. Thus, the local deformation only consists of five (instead
   of six) components. But for compatibility with general purpose beam transformation, at element, six components as
   usual are computed and stored, the first five are sent to section for computation of response, the torsion response
   is assumed to be elastic.

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
