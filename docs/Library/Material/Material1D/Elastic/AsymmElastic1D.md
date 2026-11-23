# AsymmElastic1D

Uniaxial Elastic Material With Asymmetric Stiffness

The `AsymmElastic1D` model applies one elastic modulus in tension and another in compression.
It is the simplest extension of [`Elastic1D`](Elastic1D.md) that can represent a different axial stiffness in the two loading directions.

## Background

The axial response is piecewise linear and continuous at the origin,

$$
\sigma=\begin{cases}
E_t\varepsilon, & \varepsilon\ge 0,\\[1mm]
E_c\varepsilon, & \varepsilon<0,
\end{cases}\qquad
E_T=\frac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}=\begin{cases}
E_t, & \varepsilon\ge 0,\\
E_c, & \varepsilon<0.
\end{cases}
$$

Here $$E_t$$ is the tension modulus `(2)` and $$E_c$$ is the compression modulus `(3)`.
The secant stiffness equals the tangent stiffness on either side of the origin, but the two branches generally differ.
The model is path independent and stores no history variables, so unloading follows the same branch as loading.

## Syntax

```text title="AsymmElastic1D"
material AsymmElastic1D (1) (2) (3) [4]
# (1) int, unique material tag
# (2) double, tension elastic modulus
# (3) double, compression elastic modulus
# [4] double, density, default: 0.0
```

## Remarks

The branch is selected by the sign of the trial strain, with zero strain assigned to the tension branch.
Both moduli are used as given, without conversion to absolute values, so positive inputs should be used.

!!! warning "implementation limitation"
    A negative modulus input produces a negative stiffness on that branch.
    The tangent jumps from one modulus to the other at zero strain without a transition region.

!!! note "developer note"
    The constructor stores both moduli without `fabs`, unlike [`BilinearElastic1D`](BilinearElastic1D.md).

The density `(4)` defaults to zero.
The stiffness is discontinuous at $$\varepsilon=0$$, which can slow convergence if the solution oscillates about zero strain.
Use [`Elastic1D`](Elastic1D.md) when the two moduli are equal, and [`BilinearElastic1D`](BilinearElastic1D.md) when the stiffness should change after a yield stress rather than at the origin.
