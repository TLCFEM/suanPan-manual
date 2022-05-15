# NodeLine

The `NodeLine` constraint implements 2D node-line contact via Lagrangian multiplier method.

## Syntax

```
constraint NodeLine (1) (2) (3) (4)
# (1) int, unique constraint tag
# (2) int, master node i tag
# (3) int, master node j tag
# (4) int, slave node k tag
```

## Remarks

1. The outer normal vector of master line is defined by rotating the master axis defined by $$\mathbf{x}_j-\mathbf{x}_
   i$$ by $$\pi/2$$ anticlockwise. Thus, the sequence of master nodes matters.
