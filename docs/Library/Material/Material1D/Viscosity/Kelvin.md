# Kelvin

Kelvin Model

The `Kelvin` model represents a dashpot and a spring in parallel.
This material model does respond to both displacement and velocity.

## Syntax

```text title="Kelvin"
material Kelvin (1) (2) (3)
# (1) int, unique material tag
# (2) int, damper tag
# (3) int, spring tag
```

## Theory

The Kelvin or Kelvin--Voigt element places a spring of stiffness $$E$$ and a dashpot of viscosity $$\eta$$ in parallel, so that both components share the same strain $$\varepsilon$$ and strain rate $$\dot\varepsilon$$.

$$
\sigma=\sigma_s+\sigma_d=E\varepsilon+\eta\dot\varepsilon.
$$

The retardation time

$$
\tau_r=\dfrac{\eta}{E}
$$

sets the time scale over which creep strain accumulates.
Under a suddenly applied constant stress $$\sigma_0$$ the strain approaches $$\sigma_0/E$$ according to

$$
\varepsilon(t)=\dfrac{\sigma_0}{E}\left[1-\exp\left(-\dfrac{t}{\tau_r}\right)\right].
$$

In the implementation the spring tag `(3)` receives the trial strain, while the damper tag `(2)` receives both strain and strain rate.
The trial stress is the sum of the two constituent stresses, the trial stiffness is the spring stiffness plus any damper stiffness, and the trial damping is taken from the damper.
A nonlinear spring or a nonlinear dashpot can be supplied through the corresponding tag, which makes it possible to assemble a nonlinear Kelvin--Voigt element.
The model captures creep but not stress relaxation under fixed strain, so use [`Maxwell`](Maxwell.md) when relaxation is important.

!!! info "deviation from theory"
    The stress is the sum of whatever the two tagged constituents return, so the closed form $$E\varepsilon+\eta\dot\varepsilon$$ holds only when both tags are linear.
    The assembled tangent stiffness adds any strain stiffness reported by the damper to the spring stiffness, whereas the textbook Kelvin--Voigt tangent with respect to strain is the spring stiffness alone.

## Remarks

1. Elements that pass both strain and strain rate to material models shall be used.

2. The damper tag `(2)` is read before the spring tag `(3)`.

3. The spring and damper may themselves be nonlinear 1D materials, so the wrapper can represent a nonlinear parallel rheology.

4. A conventional element that supplies strain only is rejected, since this class implements no strain-only update.

5. For stress relaxation or for a broadband relaxation spectrum, use [`Maxwell`](Maxwell.md) or a generalised Maxwell assembly instead.

## References

1. [ISBN 978-0-12-174250-8](https://search.worldcat.org/search?q=bn:9780121742508)

2. Solid Mechanics Part I: An Introduction to Solid Mechanics

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning   |
|----------------|--------------------|
| S              | total stress       |
| E              | total strain       |
| V              | total strain rate  |
| SD             | damper stress      |
| ED             | damper strain      |
| VD             | damper strain rate |
| SS             | spring stress      |
| ES             | spring strain      |
| VS             | spring strain rate |
