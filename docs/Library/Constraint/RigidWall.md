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

The rigid wall constraints are single sided. Travelling against the outer normal direction is not allowed while the 
other direction is permitted.

### 1D

The 1D version takes the origin and the side of the wall as the inputs.

```
! infinite rigid wall by penalty
rigidwall (1) (2) (3) [4]
constraint rigidwall (1) (2) (3) [4]
# (1) int, unique constraint tag
# (2) double, coordinate of origin of rigid wall
# (3) double, sign of normal direction +1 or -1
# [4] double, multiplier, default: 1E4

! infinite rigid wall by multiplier
rigidwallmultiplier (1) (2) (3)
constraint rigidwallmultiplier (1) (2) (3)
# (1) int, unique constraint tag
# (2) double, coordinate of origin of rigid wall
# (3) double, sign of normal direction +1 or -1
```

### 2D

The 2D version takes the origin and either the edge vector or the normal vector as the inputs.

```
! infinite rigid wall by penalty
rigidwall (1) (2...3) (4...5) [6]
constraint rigidwall (1) (2...3) (4...5) [6]
# (1) int, unique constraint tag
# (2...3) double, coordinates of origin of rigid wall
# (4...5) double, vector of normal direction
# [6] double, multiplier, default: 1E4

! infinite rigid wall by multiplier
rigidwallmultiplier (1) (2...3) (4...5)
constraint rigidwallmultiplier (1) (2...3) (4...5)
# (1) int, unique constraint tag
# (2...3) double, coordinates of origin of rigid wall
# (4...5) double, vector of normal direction

! finite rigid wall by penalty
finiterigidwall (1) (2...3) (4...5) [6]
constraint finiterigidwall (1) (2...3) (4...5) [6]
# (1) int, unique constraint tag
# (2...3) double, coordinates of origin of rigid wall
# (4...5) double, vector of wall edge
# [6] double, multiplier, default: 1E4

! finite rigid wall by multiplier
finiterigidwallmultiplier (1) (2...3) (4...5)
constraint finiterigidwallmultiplier (1) (2...3) (4...5)
# (1) int, unique constraint tag
# (2...3) double, coordinates of origin of rigid wall
# (4...5) double, vector of wall edge
```

### 3D

The 3D version takes the origin and the normal vector as the inputs. Alternatively, two edges can be specified to 
define a finite wall.

```
! infinite rigid wall by penalty
rigidwall (1) (2...4) (5...7) [8]
constraint rigidwall (1) (2...4) (5...7) [8]
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of normal direction
# [8] double, multiplier, default: 1E4

! infinite rigid wall by multiplier
rigidwallmultiplier (1) (2...4) (5...7)
constraint rigidwallmultiplier (1) (2...4) (5...7)
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of normal direction

! finite rigid wall by penalty
finiterigidwall (1) (2...4) (5...7) (8...10) [11]
constraint finiterigidwall (1) (2...4) (5...7) (8...10) [11]
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of first edge
# (8...10) double, vector of second edge
# [11] double, multiplier, default: 1E4

! finite rigid wall by multiplier
finiterigidwallmultiplier (1) (2...4) (5...7) (8...10)
constraint finiterigidwallmultiplier (1) (2...4) (5...7) (8...10)
# (1) int, unique constraint tag
# (2...4) double, coordinates of origin of rigid wall
# (5...7) double, vector of first edge
# (8...10) double, vector of second edge
```

## Remarks

1. The normal vector of finite rigid walls is computed by cross product between two edges defined. Beware of the order.
2. The penalty function method can be used in both static and dynamic analysis.
3. The multiplier method can only be used in static analysis.
4. Both methods do not perform well in dynamic analysis, to conserve energy and momentum, users may use the 
   [`RestitutionWall`](RestitutionWall.md) constraint instead.