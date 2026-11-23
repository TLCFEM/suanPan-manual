# Maxwell

Maxwell Model Using An Iterative Solving Algorithm

This material model does respond to both displacement and velocity.

## References

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

2. Chang, T. L., and Lee, C.-L. (2022), "Numerical simulation of generalised Maxwell-type viscous dampers with an efficient iterative algorithm," Mechanical Systems and Signal Processing, 170, 108795, [doi:10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795).

3. Christensen, R. M. (1982), Theory of Viscoelasticity: An Introduction, 2nd edition, Academic Press.

## Syntax

```text title="Maxwell"
material Maxwell (1) (2) (3) [4] [5] [6]
# (1) int, unique tag
# (2) int, damper tag
# (3) int, spring tag
# [4] bool string, whether to use matrix formulation, default: false
# [5] int, the maximum unconverged substep allowed, default: 0
# [6] double, local time integration parameter, default: 0.5
```

## Theory

A Maxwell element consists of a spring of stiffness $E$ and a dashpot of viscosity $\eta$ in series, so that both carry the same stress $\sigma$ and the total strain is the sum of the two internal strains.

$$
\sigma=E\varepsilon_s=\eta\dot\varepsilon_d,\qquad \varepsilon=\varepsilon_s+\varepsilon_d.
$$

Differentiating the compatibility relation and eliminating the internal strains gives the standard differential form

$$
\dot\varepsilon=\dfrac{\dot\sigma}{E}+\dfrac{\sigma}{\eta}.
$$

A suddenly imposed strain $\varepsilon_0$ produces an exponentially decaying stress,

$$
\sigma(t)=E\varepsilon_0\exp\left(-\dfrac{t}{\tau}\right),\qquad \tau=\dfrac{\eta}{E},
$$

where $\tau$ is the relaxation time.
Under constant stress the dashpot creeps indefinitely, so a single Maxwell element behaves as a fluid at long time.
The implementation solves three local unknowns, namely the spring strain increment, the dashpot strain increment and the dashpot strain-rate increment, by Newton iteration on strain compatibility and stress equality.
The dashpot strain rate is integrated with a $\beta$-method whose local target is $\Delta t(\dot\varepsilon_n-\dot\varepsilon_{d,n})+\beta\Delta t\,\Delta\dot\varepsilon$, so $\beta=0.5$ corresponds to a linear distribution of spring strain over the step.
The scalar algorithm condenses the three equations to one unknown and is cheaper per iteration but less robust for strongly nonlinear dashpots.
The stress reported by the material is the average of the spring and dashpot stresses, which coincide once the local iteration converges.

!!! warning "implementation limitation"
    The local Newton iteration stops after 20 steps with a tolerance of $5\times10^{-13}$ rather than solving the continuous Maxwell equation exactly.
    The spring and damper tangents are held at their trial values during each local iteration, so nonlinear constituents are treated with a linearised local solve.
    When `[5]` is positive, a failed local solve is silently reset to the last committed state for a limited number of steps instead of failing immediately.
    The reported stress is an average of the two constituent stresses rather than a single equilibrium force.

## Remarks

1. When `[4]` is set to true, the matrix formulation is used, that is, a 3-by-3 matrix is used in local iterations.
   However, the inverse of the Jacobian is not computed numerically, but analytically.
   When it is set to false, the scalar iteration is performed.
   In general, a scalar algorithm requires fewer floating number operations but may be less numerically stable.
2. The parameter `[5]` can be set to a nonzero positive integer to allow some unconverged substeps to be accumulated to avoid sharp transition regions that may cause numerical issues.
   As a result, the response may not be as smooth as in other regions.
3. The parameter `[6]` is used to control how local strain is integrated.
   A value of $$0.0$$ indicates it would be automatically computed based on the input strain and strain rate increments.
   A value of $$0.5$$ indicates a linear distribution of spring strain over time.

4. Both material tags `(2)` and `(3)` must refer to previously defined 1D materials, with the dashpot tag given first and the spring tag second.

5. The constructor takes the absolute value of the integration parameter and clamps it to $$0\leq\beta\leq1$$, so out-of-range values are silently mapped into the admissible interval.

6. The local convergence tolerance is fixed at $$5\times10^{-13}$$ in the implementation and is not exposed as an input.

7. An element that supplies both strain and strain rate is required, for example [`Damper02`](../../../Element/Special/Damper02.md).

8. A generalised Maxwell solid, consisting of several Maxwell branches in parallel with an equilibrium spring, is the standard rheology for broadband viscoelasticity and is the subject of the reference below.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning        |
|----------------|-------------------------|
| SD, SS, S      | stress                  |
| ED             | damper strain           |
| VD             | damper strain rate      |
| ES             | spring strain           |
| VS             | spring strain rate      |
| E              | total strain            |
| V              | total strain rate       |
| LITR           | local iteration counter |
