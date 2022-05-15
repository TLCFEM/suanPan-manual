# ParticleCollision

The `ParticleCollision2D` and `ParticleCollision3D` constraints can be used to simulate collision of particles of
uniform size.

## Syntax

```
ParticleCollision2D (1) (2) (3)
ParticleCollision3D (1) (2) (3)
# (1) int, unique constraint tag
# (2) double, space
# (3) double, penalty number
```

The constraint is applied to ALL particles defined in the system. Since any two particles can collide with each other,
there is no way to obtain the structural topology. Thus, the full/sparse matrix storage shall be used. Parameter `(2)`
controls the uniform size of particles. When any two particles are closer than the value defined in `(2)`, interaction
forces will be applied. The penalty method is used in implementation, thus parameter `(3)` represents the penalty
number, adjusting this value leads to different magnitudes of interaction forces.