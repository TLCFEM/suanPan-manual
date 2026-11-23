# LinearSpring2D

The `LinearSpring2D` constraint adds a pairwise linear spring interaction between particles in a 2D system.
It is applied to every pair of particles in the model and is intended for discrete-element simulations.

## Syntax

```text title="LinearSpring2D"
constraint LinearSpring2D (1) [2] [3]
# (1) int, unique constraint tag
# [2] double, spacing, default: 1.0
# [3] double, alpha (spring stiffness), default: 1.0
```

## Theory

For two particles separated by a distance $$r<s$$, the force magnitude is $$F=\alpha(s-r)$$, where $$s$$ is the spacing and $$\alpha$$ the stiffness.
The force vanishes as soon as the separation reaches the spacing, so the interaction is repulsive and has finite range.
This differs from [`ParticleCollision`](ParticleCollision.md), whose force grows without bound as two particles approach.

## Remarks

The spacing is limited to a minimum of $$10^{-4}$$ internally.
The full or sparse matrix storage scheme is required because the pair topology is not known in advance.

## Example

```text
node 1 -1 0
node 2 1 0
mass 1 1 100 1 2
mass 2 2 100 1 2
constraint LinearSpring2D 1 3. 10.
```
