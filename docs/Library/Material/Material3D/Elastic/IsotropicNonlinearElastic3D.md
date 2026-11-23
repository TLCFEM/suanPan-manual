# IsotropicNonlinearElastic3D

General Nonlinear Elastic Isotropic 3D Material Framework

The `IsotropicNonlinearElastic3D` class is an abstract general purpose framework.

It offers an interface to allow users to define arbitrary strain energy potential based on volumetric strain and equivalent strain (squared), that is

$$
W=f\left(\varepsilon_v,\varepsilon_p^2\right),
$$

where

$$
\varepsilon_v=\text{trace}\left(\varepsilon\right),\qquad\varepsilon_p=\sqrt{\dfrac{2}{3}\varepsilon_d:
\varepsilon_d}.
$$

Note it is normally expressed in terms of equivalent strain rather than its square.
However, the derivation of tangent stiffness would be too cumbersome.

## Overridden Method

The `IsotropicNonlinearElastic3D` provides a method that shall be overridden.

```cpp
virtual vec compute_derivative(double, double) = 0;
```

The first argument is $$\varepsilon_v$$.
The second argument is $$\varepsilon_s=\varepsilon_p^2$$.

The method shall return a vector of size six with the following values computed.

| **index** | **value**                                                           |
|:----------|:--------------------------------------------------------------------|
| $$0$$     | $$\dfrac{\partial{}W}{\partial\varepsilon_v}$$                      |
| $$1$$     | $$\dfrac{\partial{}W}{\partial\varepsilon_s}$$                      |
| $$2$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_v^2}$$                    |
| $$3$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_s^2}$$                    |
| $$4$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_v\partial\varepsilon_s}$$ |
| $$5$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_s\partial\varepsilon_v}$$ |

The volumetric strain and the squared equivalent strain are work-conjugate to $\partial W/\partial\varepsilon_v$ and $\partial W/\partial\varepsilon_s$, respectively.
Writing $\varepsilon_s=\varepsilon_p^2$ removes the square root from the derivatives and keeps the tangent defined at $\varepsilon_p=0$, at the cost of an energy that is even in the deviatoric strain.

!!! info "deviation from theory"
    Because the potential depends only on $\varepsilon_s=\varepsilon_p^2$, the deviatoric response is even in $\varepsilon_p$.
    Tension-compression asymmetry in the deviatoric response cannot be represented by this framework.

With $\boldsymbol I$ the identity and $\mathbf P_\mathrm{dev}$ the fourth-order deviatoric projector, the chain rule gives

$$
\boldsymbol\sigma=\dfrac{\partial W}{\partial\varepsilon_v}\boldsymbol I+\dfrac{\partial W}{\partial\varepsilon_s}\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon},
\qquad
\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon}=\dfrac43\boldsymbol\varepsilon_d,
\qquad
\dfrac{\partial^2\varepsilon_s}{\partial\boldsymbol\varepsilon\partial\boldsymbol\varepsilon}=\dfrac43\mathbf P_\mathrm{dev}.
$$

The consistent tangent is

$$
\mathbb D=\dfrac{\partial^2W}{\partial\varepsilon_v^2}\boldsymbol I\otimes\boldsymbol I
+\dfrac{\partial^2W}{\partial\varepsilon_v\partial\varepsilon_s}\left(\boldsymbol I\otimes\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon}+\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon}\otimes\boldsymbol I\right)
+\dfrac{\partial^2W}{\partial\varepsilon_s^2}\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon}\otimes\dfrac{\partial\varepsilon_s}{\partial\boldsymbol\varepsilon}
+\dfrac{\partial^2W}{\partial\varepsilon_s}\dfrac43\mathbf P_\mathrm{dev}.
$$

The two mixed derivatives at indices 4 and 5 occupy the two off-diagonal blocks of $\mathbb D$ and coincide for a smooth potential.

## Remarks

This class is abstract and has no command-line token.
It serves as the base for concrete potentials such as [`NLE3D01`](NLE3D01.md).
The strain measure is the infinitesimal strain tensor rather than the Green strain, so nonlinear geometry is not required.

!!! warning "implementation limitation"
    This is a small-strain nonlinear elastic framework.
    It does not use finite deformation measures and must not be combined with nonlinear geometry for large rotations.

The method `compute_derivative` is called at zero strain during initialisation to build the initial stiffness, so the potential must be differentiable there.
The squared equivalent strain is floored at machine epsilon in derived implementations, which keeps the derivative finite when the power-law exponent is negative.

!!! warning "implementation limitation"
    Flooring $\varepsilon_s$ at machine epsilon replaces the exact power-law derivative by a regularised value near zero strain.
    The tangent at the origin is therefore finite but depends on the floor value.

The response is isotropic by construction, so the [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper has no effect on the elastic response.

## References

1. G. A. Holzapfel, *Nonlinear Solid Mechanics*, Wiley, 2000, Chapter 3.
2. R. W. Ogden, *Non-linear Elastic Deformations*, Dover, 1997, Chapter 2.
