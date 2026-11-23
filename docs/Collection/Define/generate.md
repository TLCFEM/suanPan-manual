# generate

The `generate` command creates node or element groups according to predefined rules.

For custom rules, refer to [`CustomNodeGroup`](../../Library/Group/CustomNodeGroup.md).

!!! warning "precision"
    For all forms, whenever floating-point operations are involved, the criterion is evaluated within machine precision (machine epsilon).
    Coordinates should therefore be specified as accurately as possible, with at least 16 significant digits.

## form one: generate based on a fixed interval

```
# to hold one node/element only
generate nodegroup (1) (2)
generate elementgroup (1) (2)
# (1) int, unique group tag
# (2) int, object tag

# generate from tag (2) to tag (3) with unit increment
generate nodegroup (1) (2) (3)
generate elementgroup (1) (2) (3)
# (1) int, unique group tag
# (2) int, starting object tag
# (3) int, ending object tag

# generate according to given increment
generate nodegroup (1) (2) (3) (4)
generate elementgroup (1) (2) (3) (4)
# (1) int, unique group tag
# (2) int, starting object tag
# (3) int, interval
# (4) int, ending object tag
```

Note that the starting tag does not have to be smaller than the ending tag.

## form two: generate a node group based on polynomial

```
generatebyrule nodegroup (1) (2) [(3)...]
# (1) int, unique group tag
# (2) int, DoF tag that polynomial shall be applied on
# [(3)...] double, parameters a_n, a_{n-1}, a_{n-2},..., a_0
```

The polynomial constraint is defined to be

$$
\sum{}a_nx^n=0,
$$

Here, $$x$$ is the coordinate of the target DoF of the target node.

For example, to select all nodes on the line $$y=200$$, use the following command.

```
generatebyrule nodegroup 1 2 1. -200.
```

## form three: generate a node group based on the line segment

To select all nodes that lie on a straight line segment, use the following command.

```
generatebypoint nodegroup (1) [(2)...]
# (1) int, unique group tag
# [(2)...] double, coordinates of two end points
```

There is no restriction on the number of coordinates of each point, but the two points must have the same number of coordinates.
For example, to select all points on the line segment between $$(3,~4)$$ and $$(8,~7)$$, use

```
generatebypoint nodegroup 1 3. 4. 8. 7.
```

## form four: generate a node group based on plane

```
generatebyplane nodegroup (1) [(2)...]
# (1) int, unique group tag
# [(2)...] double, parameters that define a plane
```

A plane is defined by

$$
\sum{}a_ix_i+b=0,
$$

Here, $$x_i$$ are coordinates, $$a_i$$ are the corresponding coefficients, and $$b$$ is a constant.

For example, a plane can be defined as

$$
3x+2y-z+7=0.
$$

Then

```
generatebyplane nodegroup 1 3. 2. -1. 7.
```

This finds all nodes that lie on the plane and groups them.

There is no restriction on the number of coordinates used, so it is possible to define a hyperplane or a line.
The last parameter is always the constant.
For example, the following command defines the line $$x+2y-3=0$$ in the 2D plane.

```
generatebyplane nodegroup 1 1. 2. -3.
```

If this is used to find nodes for a group in a 3D problem, the $$z$$ coordinates of all nodes are automatically skipped.
Nodes such as $$(2,1,0)$$ and $$(2,1,10)$$ are then both added to the group.
