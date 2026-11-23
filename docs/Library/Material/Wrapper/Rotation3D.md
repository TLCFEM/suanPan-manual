# Rotation3D

3D Rotation Wrapper

Alters the inclination of the 3D host material model and is typically used with anisotropic material models.

## Theory

An anisotropic material is defined by constitutive tensors whose components are referred to a local material frame $\{\mathbf e'_i\}$.
If the host is evaluated in that local frame, a strain measured in the global frame must be rotated into it and the resulting stress rotated back.
Let $\mathbf R$ be the proper orthogonal matrix generated from the Euler rotation vector described below, so that $\mathbf R=\exp([\mathbf\theta]_\times)$.
The strain tensor transformation applied by the wrapper is

$$
\mathbf\varepsilon'=\mathbf R\,\mathbf\varepsilon\,\mathbf R^{\mathrm T},
\qquad
\mathbf\sigma=\mathbf R^{\mathrm T}\,\mathbf\sigma'\,\mathbf R,
$$

so that the local material axes are the rows of $\mathbf R$ and the stress–strain tangent transforms as $\mathbf D=\mathbf R^{\mathrm T}\,\mathbf D'\,\mathbf R$ when the fourth-order tensor is written with the appropriate index pairing.
In the six-component Voigt convention used by suanPan the same operations are represented by a $6\times6$ matrix $\mathbf T$ built from products of the entries of $\mathbf R$.
With $\mathbf e=(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$ and $\gamma_{ij}=2\varepsilon_{ij}$, the first block of $\mathbf T$ contains $R_{ij}^2$, the coupling block from normal to shear entries contains $R_{ij}R_{ik}$, and the shear block contains factors $2R_{ij}R_{ik}$ and sums $R_{ij}R_{lk}+R_{ik}R_{lj}$.
Because engineering shear is used, $\mathbf T$ is not an orthogonal matrix, but it is constructed so that the work conjugation $\mathbf\sigma:\mathbf\varepsilon=\mathbf\sigma':\mathbf\varepsilon'$ holds when the stress is mapped back with $\mathbf T^{\mathrm T}$.

!!! info "deviation from theory"
    The textbook change of basis to axes rotated by $\mathbf\theta$ uses $\mathbf\varepsilon'=\mathbf R^{\mathrm T}\mathbf\varepsilon\mathbf R$ with the local axes in the columns of $\mathbf R$.
    The suanPan implementation builds $\mathbf T$ from the entries $R_{ij}$, so it applies $\mathbf\varepsilon'=\mathbf R\mathbf\varepsilon\mathbf R^{\mathrm T}$, which is the passive rotation by $-\mathbf\theta$.
    For a rotation about the $x_3$ axis, `Rotation3D` with rotation vector $(0,0,\theta)$ therefore gives the same material response as `Rotation2D` with angle $-\theta$.

The wrapper therefore applies

$$
\mathbf e'=\mathbf T\,\mathbf e,
\qquad
\mathbf s=\mathbf T^{\mathrm T}\,\mathbf s',
\qquad
\mathbf D=\mathbf T^{\mathrm T}\,\mathbf D'\,\mathbf T,
$$

where $\mathbf s$ and $\mathbf D$ are the stress and tangent delivered to the element and primed quantities come from the host.
The same expressions are used for the initial and the trial stiffness, so the rotated tangent is consistent whenever the host tangent is consistent.

The three arguments `(3)` to `(5)` are the components of a single Euler rotation vector $\mathbf\theta$.
Writing $\Theta=\lVert\mathbf\theta\rVert$ and $\mathbf n=\mathbf\theta/\Theta$, the implementation forms the unit quaternion $q=(\cos(\Theta/2),\,\sin(\Theta/2)\mathbf n)$ and converts it to the rotation matrix

$$
\mathbf R=2q_0\,[\mathbf q]\times+2\,\mathbf q\mathbf q^{\mathrm T}+\left(q_0^2-\mathbf q\cdot\mathbf q\right)\mathbf I,
$$

which is equivalent to the matrix exponential $\exp([\mathbf\theta]\times)$ and rotates by $\Theta$ about $\mathbf n$ according to the right-hand rule.
The angle is measured in radians, and the three arguments are the Cartesian components of the rotation vector, not three successive Euler angles.

The rotation is a fixed change of material basis applied to small-strain tensor components.
It does not rotate the geometry and it is not a corotational or objective-rate formulation for finite rotations.
For a planar problem the cheaper [Rotation2D](Rotation2D.md) wrapper applies the corresponding two-dimensional transformation.

## Syntax

```text title="Rotation3D"
material Rotation3D (1) (2) (3...5)
# (1) int, unique material tag
# (2) int, associated material tag
# (3...5) double, three components of rotation vector
```

Rotations in 3D space may have different forms.
The [Euler vector](https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation) is used to represent the axis and angle of rotation.
Parameters `(3)` to `(5)` are three components of the vector $$\mathbf{\theta}$$.

The response of attached 3D material model will be output when recorded.

## Remarks

The host must be a registered 3D material, and the wrapper inherits its density.
Use it for orthotropic or otherwise direction-dependent hosts such as [OrthotropicElastic3D](../Material3D/Elastic/OrthotropicElastic3D.md), whose principal axes are not aligned with the global axes.
For an isotropic host the rotated response is identical to the unrotated one, so the wrapper only adds cost.
The constructor evaluates $\sin(\Theta/2)/\Theta$ directly, so a zero rotation vector is not a safe way to request the identity transformation; omit the wrapper in that case.

!!! warning "implementation limitation"
    A zero rotation vector fills the transformation matrix with NaN values rather than producing the identity.
    Omit the wrapper entirely when the material axes need no rotation.

!!! note "developer note"
    For $\Theta=0$ the quotient $\sin(\Theta/2)/\Theta$ is evaluated as $0/0$.

The wrapper forwards `record` calls to the host, so recorded stresses are expressed in the material axes and may differ from the global stresses returned to the element.
Nested use with dimension-reducing wrappers is possible, for example a rotated host wrapped by [PlaneStress](PlaneStress.md), provided the intended material axes are tracked explicitly.

## References

- [ISBN 978-0-201-02918-5](https://search.worldcat.org/search?q=bn:9780201029185)
- [10.1145/325165.325242](https://doi.org/10.1145/325165.325242)
- [ISBN 978-0-471-98774-1](https://search.worldcat.org/search?q=bn:9780471987741)
