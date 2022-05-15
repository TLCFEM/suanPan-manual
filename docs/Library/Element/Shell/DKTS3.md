# DKTS3

DKT Triangle Shell

* Number of Nodes: 3
* Number of DoFs: 6 (Translation, Translation, Translation, Rotation, Rotation, Rotation)

## Syntax

```
element DKTS3 (1) (2...4) (5) (6) [7]
# (1) int, unique element tag
# (2...4) int, node i, j, k
# (5) int, material tag
# (6) double, thickness
# [7] int, number of integration points, default: 3
```

## Sample

The model can be downloaded. [DKTS3.zip](DKTS3.zip)

![example](DKTS3.png)
