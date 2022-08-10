# NMB21E

2D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections And End Moment Release

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)

## Syntax

```
element NMB21EL (1) (2) (3) (4) [5]
element NMB21EH (1) (2) (3) (4) [5]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
```

## Remarks

Only `NM2D*` sections are supported. There is no validation of section attached, analysts shall make sure proper
sections are used.

The `NMB21EL` element releases the moment at low node `i` and the `NMB21EH` element releases the moment at high node 
`j`.

A non-iterative algorithm is used.
