# RigidWall

The `RigidWall` constraint implements the contact between model and the assigned rigid walls. The rigid walls can have
either finite or infinite dimensions.

## Theory

Two methods are implemented, namely, the multiplier method and the penalty method.

### Multiplier Method

The implementation is identical to a conventional constraint.

### Penalty Method

The impenetrable condition is implemented by adding resisting forces to the right hand of the equation. The force $$F$$
is proportional to the penetration $$U_p$$.

$$
F=\dfrac{\alpha}{\Delta{}t^2}U_p,
$$

where $$\Delta{}t$$ is the time increment of current substep, $$\alpha$$ is the multiplier. The denominator
$$\Delta{}t^2$$ is included to produce (relatively) objective results. The determination of multiplier $$\alpha$$ often
requires trial and error. In general, too large values shall be avoided.

## Syntax

```
! infinite rigid wall by penalty
rigidwall (1) (2...4) (5...7) [8]
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of normal direction
# [8] double, multiplier, default: 1.0

! infinite rigid wall by multiplier
rigidwallmultiplier (1) (2...4) (5...7)
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of normal direction

! finite rigid wall by penalty
finiterigidwall (1) (2...4) (5...7) (8...10) [11]
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of first edge
# (8...10) double, vector of second edge
# [11] double, multiplier, default: 1.0

! finite rigid wall by multiplier
finiterigidwallmultiplier (1) (2...4) (5...7) (8...10)
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of first edge
# (8...10) double, vector of second edge
```

## Remarks

1. The sizes of origin and norm shall be identical (three), no matter if it is a 2D or 3D model.
2. The normal vector of finite rigid walls is computed by cross product between two edges defined. Beware of the order.