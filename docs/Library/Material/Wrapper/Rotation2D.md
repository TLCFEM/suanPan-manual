# Rotation2D

2D Rotation Wrapper

Alters the inclination of the 2D host material model and is typically used with anisotropic material models.

## Theory

A two-dimensional anisotropic material stores its constitutive matrix in a local frame whose axes need not coincide with the global element axes.
Let $\theta$ be the counter-clockwise angle from the global axis $x_1$ to the local material axis $x'_1$, and write $c=\cos 2\theta$ and $s=\sin 2\theta$.
In the engineering-shear Voigt convention $\mathbf e=(\varepsilon_{11},\varepsilon_{22},\gamma_{12})$ with $\gamma_{12}=2\varepsilon_{12}$, the global-to-local strain transformation used by the implementation is

$$
\mathbf T(\theta)=
\begin{bmatrix}
\dfrac{1+c}{2}&\dfrac{1-c}{2}&\dfrac{s}{2}\\[2mm]
\dfrac{1-c}{2}&\dfrac{1+c}{2}&-\dfrac{s}{2}\\[2mm]
-s&s&c
\end{bmatrix},
\qquad
\mathbf e'=\mathbf T\,\mathbf e.
$$

The shear row and column carry factors that differ by two because the same physical shear appears as $\gamma=2\varepsilon_{12}$ in the vector but as $\varepsilon_{12}$ in the tensor.
Consequently $\mathbf T$ is not orthogonal, and work conjugacy requires the stress to be mapped back with its transpose rather than its inverse,

$$
\mathbf s=\mathbf T^{\mathrm T}\,\mathbf s',
\qquad
\mathbf D=\mathbf T^{\mathrm T}\,\mathbf D'\,\mathbf T.
$$

The identity $\mathbf s\cdot\mathbf e=(\mathbf T^{\mathrm T}\mathbf s')\cdot\mathbf e=\mathbf s'\cdot(\mathbf T\mathbf e)=\mathbf s'\cdot\mathbf e'$ confirms that energy is invariant under the change of axes.
The initial, current and trial stiffnesses are all rotated with the same expression, so the wrapper preserves the consistency of the host tangent.
The transformation is a fixed rotation of material axes for small-strain tensors, not a finite-rotation or corotational formulation.
The three-dimensional analogue is [Rotation3D](Rotation3D.md), which uses an Euler vector and a $6\times6$ transformation built from a rotation matrix.

## Syntax

```text title="Rotation2D"
material Rotation2D (1) (2) (3)
# (1) int, unique material tag
# (2) int, associated material tag
# (3) double, angle rotated (anti-clockwise positive)
```

The response of attached 2D material model will be output when recorded.

## Remarks

The angle is given in radians, and a positive value rotates the material axes counter-clockwise relative to the global axes.
The host must be a registered 2D material, and the wrapper inherits its density.
Use this wrapper with orthotropic or other direction-dependent 2D hosts, such as a 2D model wrapped around [OrthotropicElastic3D](../Material3D/Elastic/OrthotropicElastic3D.md) by [PlaneStress](PlaneStress.md).
An isotropic host yields the same response in every direction, so rotation has no visible effect for such hosts.
Recorded quantities are forwarded to the host, so stresses are reported in the material axes rather than in the global axes used by the element.
A wrapper can be stacked with [Laminated](Laminated.md) if several differently oriented layers must share the same strain.

## References

- T. Belytschko, W. K. Liu and B. Moran, *Nonlinear Finite Elements for Continua and Structures*, Wiley, 2000.
- H. Goldstein, *Classical Mechanics*, 2nd ed., Addison-Wesley, 1980.
- O. C. Zienkiewicz, R. L. Taylor and J. Z. Zhu, *The Finite Element Method: Its Basis and Fundamentals*, 7th ed., Butterworth-Heinemann, 2013.
