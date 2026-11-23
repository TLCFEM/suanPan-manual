# Damper02/Damper04

Maxwell Model

The `Damper02` and `Damper04` are Maxwell models that use **displacement** and **velocity** as inputs, that is, element length is not used to compute strain or strain rate.

## References

The Maxwell model allows combinations of nonlinear springs and dampers.
The algorithm implemented is documented in the following paper.

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)

## Damper02

The `Damper02` is the 2D version.

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2

## Damper04

The `Damper04` is the 3D version.

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Translation)
* DoF Label: U1, U2, U3

## Background

A Maxwell model connects a spring and a dashpot in series.
For a prescribed end displacement $\epsilon$ and velocity $\dot\epsilon$, the two components carry the same force $N$ but share the deformation,

$$
\epsilon=\epsilon_s+\epsilon_d,\qquad
N=f_s(\epsilon_s)=f_d(\dot\epsilon_d).
$$

Eliminating $\epsilon_d$ gives a scalar evolution equation for the internal spring strain $\epsilon_s$, which has to be solved locally at every trial state.
The implementation uses the Newton--Raphson based state-determination algorithm of Chang and Lee, so the spring may be a rate-independent nonlinear model and the dashpot coefficient may depend on both displacement and velocity.

The element projects the end displacements and velocities onto the initial axis $\boldsymbol c$ and passes $u=\boldsymbol c\cdot(\boldsymbol u_j-\boldsymbol u_i)$ and $v=\boldsymbol c\cdot(\boldsymbol v_j-\boldsymbol v_i)$ to the Maxwell material, so the element length is again not used.
With $\beta$ the local time-integration parameter and $\Delta t$ the time increment, the factor $\beta\Delta t$ controls how the spring strain is interpolated over the increment; $\beta=0.5$ corresponds to a linear spring strain history.
The element assembles the resulting force as $\boldsymbol R_j=\boldsymbol c\,N$, $\boldsymbol R_i=-\boldsymbol R_j$, and forms both a trial tangent stiffness and a trial damping matrix from the Maxwell material.

!!! info "deviation from theory"
    As in [`Damper01`](Damper01.md), the raw projected displacement and velocity are passed to the material without division by the element length.

!!! note "developer note"
    The series spring--dashpot state is found by a local iterative solution rather than by an analytical integration of the governing ODE.

## Syntax

```text title="Damper02"
element Damper02 (1) (2) (3) (4) (5) [6] [7] [8]
element Damper04 (1) (2) (3) (4) (5) [6] [7] [8]
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, damper tag
# (5) int, spring tag
# [6] bool string, whether to use matrix in iteration, default: true
# [7] int, the maximum delay number, default: 0
# [8] double, beta, default: 0.5
```

## Remarks

1. Parameter `[7]` indicates whether to stack diverged increments into next iteration.
   If $$0$$ is assigned, the material returns a failure flag as long as local iteration fails to converge.
   If $$n>0$$, a maximum $$n$$ increments are allowed to be stacked before exit due to divergence.
2. The `[8]` parameter controls the local time integration, $$\beta\in[0,1]$$ shall be defined.
   The default value $$0.5$$ implies a constant acceleration rule for the spring component in the Maxwell model.
3. The parameter `[6]` selects the local solver, with `true` giving a three-by-three matrix Newton iteration and `false` a scalar iteration; the matrix form is more robust but costs more per iteration.
4. When `[7]=n>1`, a failed local iteration resets the trial state and is counted against the limit, so up to $$n-1$$ consecutive failures are tolerated before the state determination is declared divergent.

!!! note "developer note"
    The wording that diverged increments are stacked into the next iteration does not reflect the implementation.
    On a tolerated local failure the code resets the trial state to the converged state and continues the analysis.

5. Both a tangent stiffness and a damping matrix are returned by the Maxwell material, in contrast to [`Damper01`](Damper01.md) where the spring is optional.
6. This element sets `modify_viscous` to false, so element damping modifiers such as [`LinearViscosity`](../Modifier/LinearViscosity.md) skip it.

## Variants

`Damper05` is the revised 2D damper: `element Damper05 (1) (2) (3) (4)` takes two nodes and a damper material tag only, unlike `Damper02` it has no spring, delay or beta arguments, and it updates the material from the relative velocity alone.
`Damper06` is the same revised update in 3D, with three translational DoFs per node; see [Damper01](Damper01.md).
