# generate

The `generate` command is used to generate node/element groups according to predefined rules.

For custom rules, please refer to [`CustomNodeGroup`](../../Library/Group/CustomNodeGroup.md).

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

It shall be noted that the starting tag does not have to be smaller than the ending tag.

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

where $$x$$ is the coordinate of the target DoF of the target node.

For example, if one wants to select all nodes on the line $$y=200$$, then the following command can be defined.

```
generatebyrule nodegroup 1 2 1. -200.
```

## form three: generate a node group based on the line segment

It is sometimes useful to select all nodes lie in a straight line segment. The following command can be used.

```
generatebypoint nodegroup (1) [(2)...]
# (1) int, unique group tag
# [(2)...] double, coordinates of two end points
```

There is no restriction on the size of each point defined, but the sizes of two points must match. If one wants to
select all points lie on the line segment between points $$(3,~4)$$ and $$(8,~7)$$, then

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

where $$x_i$$ are coordinates and $$a_i$$ are the corresponding constants, $$b$$ is constant.

For example, a plane can be defined as

$$
3x+2y-z+7=0.
$$

Then

```
generatebyplane nodegroup 1 3. 2. -1. 7.
```

finds all nodes that fall in this plane and groups them.

There is no restriction on the number of coordinates used. So it is possible to define a hyper-plane, or a line.
However, the last parameter will always be the constant. For example, the following command defines the line
$$x+2y-3=0$$ in the 2D plane.

```
generatebyplane nodegroup 1 1. 2. -3.
```

If this is used to find nodes to define a group in a 3D problem, then the $$z$$ coordinates of all nodes will be
automatically skipped so that nodes such as $$(2,1,0)$$ and $$(2,1,10)$$ will be added to the group.