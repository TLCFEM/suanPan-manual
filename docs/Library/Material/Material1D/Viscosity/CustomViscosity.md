# CustomViscosity

Viscous Material Using Custom Model

Reference:

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Syntax

```text title="CustomViscosity"
material CustomViscosity (1) (2)
# (1) int, unique material tag
# (2) int, expression tag
```

## Background

`CustomViscosity` is the user-programmable member of the [`NonlinearViscosity`](NonlinearViscosity.md) family and is constructed with the power-law exponent fixed at zero.
With $$\alpha=0$$ the base class returns the viscosity itself as the stress, so the expression defines the complete stress law

$$
\sigma=\eta\left(\varepsilon,\dot\varepsilon\right).
$$

The expression is called with the two inputs $$x_0=\varepsilon$$ and $$x_1=\dot\varepsilon$$ and must return three outputs,

$$
y_0=\eta,\qquad y_1=\dfrac{\partial\eta}{\partial\varepsilon},\qquad y_2=\dfrac{\partial\eta}{\partial\dot\varepsilon}.
$$

For $$\alpha=0$$ the base class assembles the tangent stiffness and damping directly from these derivatives as $$k=y_1$$ and $$c=y_2$$.
The expression is evaluated once for each of the three outputs during a trial update, so it should be free of side effects and depend only on its two inputs.
Initialization fails if the expression tag cannot be found in the domain or if the expression does not have exactly two inputs and three outputs.

!!! warning "implementation limitation"
    The exponent is fixed at zero, so the expression must supply any rate exponent and the correct sign of the response itself.
    Side effects inside the expression will corrupt the returned tangent, so the expression must be a pure function of its inputs.
    The derivatives are used without any numerical verification.

!!! note "developer note"
    The base class calls the expression three times per trial update, once for each output.

## Remarks

The expression needed takes strain and strain rate as the inputs and returns the damping coefficient and its derivatives as the outputs.

The input size shall be 2 and the output size shall be 3.

## Example

Imagine modelling a linear viscous material such that

$$
\sigma=1234\dot{\epsilon},
$$

One can define the expression as

```text
expression SimpleVector 1 x|2 y|3 y[0]:=1234*x[1];y[1]:=0;y[2]:=1234;
```

The strain maps to `x[0]` and the strain rate maps to `x[1]`.

The stress output maps to `y[0]` and its derivatives regarding strain and strain rate map to `y[1]` and `y[2]` respectively.

The derivatives are used directly to form the global tangent, so an inconsistent derivative will degrade convergence of the Newton iteration.
Sign conventions, saturation and hardening must all be encoded in the expression itself, since this class applies no further transformation to the returned stress.
As with the other dashpots in this section, the material must be attached to an element that supplies strain rate, for example [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
The generalised viscous damper formulation behind this class is due to Chang and Lee (2022).
