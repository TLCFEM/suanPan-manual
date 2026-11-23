# VAFCRP1D

Viscous J2 Steel Model

The `VAFCRP1D` model is the uniaxial version of the [`VAFCRP`](../../Material3D/vonMises/VAFCRP.md) model.

It adds viscosity on top of the [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md).

## References

1. [10.1017/S0368393100118759](https://doi.org/10.1017/S0368393100118759)
2. [10.1179/096034007X207589](https://doi.org/10.1179/096034007X207589)
3. [10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6)
4. [10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807)

## Theory

The Peric (1993) type definition is used for viscosity.

$$
\dfrac{\gamma}{\Delta{}t}=\dot{\gamma}=\dfrac{1}{\mu}\left(\left(\dfrac{|\eta|}{k}\right)
^{\dfrac{1}{\epsilon}}-1\right),
$$

where $$\mu$$ and $$\epsilon$$ are two material constants that control viscosity.
Note either $$\mu$$ or $$\epsilon$$ can be set to zero to disable rate-dependent response.
In that case this model is identical to the [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md) model.

!!! info "deviation from theory"
    The equation above is a rate law, while the code solves a single implicit algebraic equation per increment.
    The time increment enters only through the factor $$\mu/\Delta t$$, and a unit increment is substituted when no positive increment is available.
    The overstress is therefore tied to the analysis step size rather than being integrated as an independent evolution equation.

Using the backward-Euler approximation $$\dot\gamma\approx\gamma/\Delta t$$, the implementation solves the discrete overstress equation

$$
\left|\xi\right|-\left(E+\sum_i\dfrac{a_i}{1+b_i\gamma}\right)\gamma-k(p)\left(1+\dfrac{\mu\gamma}{\Delta t}\right)^\epsilon=0,
$$

where $$p=p_n+\gamma$$, $$\xi=\sigma^\text{tr}-\sum_i\beta_i^n$$ and the back stresses are updated as

$$
\beta_i=\dfrac{\beta_i^n+\operatorname{sign}(\xi)a_i\gamma}{1+b_i\gamma}.
$$

Here $$k(p)=\sigma^i+Kp+\sigma^s(1-e^{-m^sp})$$ is the isotropic radius.
The viscosity enters through the dimensionless ratio $$\mu/\Delta t$$, so a change of the time step changes the computed overstress.
The consistent tangent has the same form as in [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md), namely $$E^{ep}=E+E^2/J$$ with $$J$$ the derivative of the residual above.

!!! warning "implementation limitation"
    Stress relaxation at fixed strain is possible when viscosity is active, but it is completely absent when either viscosity parameter is zero.

!!! note "developer note"
    The constructor tightens the local Newton tolerance to $$10^{-15}$$, which is much stricter than the global convergence tolerance.
    Unlike [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md), this model does not return early for a zero strain increment.

## Syntax

The following applies to `v3.6` and later.
Check the older syntax in the older version of the documentation.

```text title="VAFCRP1D"
material VAFCRP1D (1) (2) (3) (4) (5) (6) (7) (8) [(9) (10)...] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield stress, \sigma^i
# (4) double, linear hardening modulus, K
# (5) double, saturation stress, \sigma^s
# (6) double, m^s, saturation rate
# (7) double, mu
# (8) double, epsilon
# (9) double, a
# (10) double, b
# [11] double, density, default: 0.0
```

## Remarks

The first seven inputs are optional and default to $$E=2\times10^5$$, $$\sigma^i=400$$, $$K=0$$, $$\sigma^s=100$$, $$m^s=10$$, $$\mu=0$$ and $$\epsilon=0$$.
The kinematic constants are supplied as `a_i b_i` pairs, and a trailing odd number is interpreted as the density.
The model is rate independent when $$\mu=0$$ or $$\epsilon=0$$, so either parameter alone activates viscosity only if both are positive.
The viscosity is divided by the current time increment, and a unit increment is used when no positive increment is available.
Unlike [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md), this model does not skip a step with zero strain increment, so stress relaxation at fixed strain is possible when viscosity is active.
The local Newton tolerance is tightened to $$10^{-15}$$, which is stricter than the global convergence tolerance.
The history consists of the back stresses followed by the accumulated plastic strain.
Because the response depends on $$\Delta t$$, use a step size that resolves the relaxation time scale of interest, and refine the step to check convergence of the rate-dependent result.
A static analysis without a meaningful time increment still runs, but the viscosity then scales with the unit increment and has no physical time meaning.

## Examples

See [`VAFCRP`](../../Material3D/vonMises/VAFCRP.md).
