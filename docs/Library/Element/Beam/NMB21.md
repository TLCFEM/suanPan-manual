# NMB21

2D Displacement Based Bernoulli Beam With $$N$$-$$M$$ Interaction Sections

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Rotation)

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