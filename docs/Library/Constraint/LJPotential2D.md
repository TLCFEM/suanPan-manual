# LJPotential2D

2D Lennard-Jones Potential

## Syntax

```text
constraint LJPotential2D (1) [2] [3]
# (1) int, unique constraint tag
# [2] double, spacing, default: 1.0
# [3] double, alpha, default: 1.0
```

## Theory

This constraint implements the Lennard-Jones potential for 2D systems, viz.,

$$
V_{LJ}=4\alpha\left(\left(\dfrac{\sigma}{r}\right)^{12}-\left(\dfrac{\sigma}{r}\right)^{6}\right),
$$

where $$r$$ is the distance between two particles, $$\sigma$$ is the size of particle,
which is taken as **one tenth** of spacing `[2]`.

The force is computed as

$$
F_{LJ}=-\dfrac{\partial{}V_{LJ}}{\partial{}r}
=\dfrac{24\alpha}{r}\left(\left(\dfrac{\sigma}{r}\right)^{6}-2\left(\dfrac{\sigma}{r}\right)^{12}\right).
$$
