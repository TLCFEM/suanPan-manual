# C3D8I

Linear Cube/Brick With Incompatible Modes

* Number of Nodes: 8
* Number of DoFs: 3 (All Translation)
* DoF Label: U1, U2, U3
* Supports Body Force
* Integration Scheme: Irons Six-Point
* Constant Consistent Mass Matrix With Same Order Integration

## Theory

`C3D8I` is the eight-node hexahedron with incompatible displacement modes, intended to remove the shear locking of the fully integrated Q1 brick.
The displacement field is enriched by nine element-internal modes, three per coordinate direction:
$$
\boldsymbol u=\sum_{I=1}^8N_I\boldsymbol u_I+\sum_{\alpha=1}^9 M_\alpha\boldsymbol a_\alpha,
$$
with $M_1=1-\xi^2$, $M_2=1-\eta^2$, $M_3=1-\zeta^2$ and the analogous functions for the other displacement directions.

The enrichment gradients in the parent domain are $-2\xi$, $-2\eta$ and $-2\zeta$, which the implementation maps to the physical frame through $\boldsymbol J^{-1}$ at each sampling point.
The strain field is $\boldsymbol\varepsilon=\boldsymbol B_1\boldsymbol u_e+\boldsymbol B_2\boldsymbol a$, where $\boldsymbol B_1$ is the usual Q1 strain-displacement matrix and $\boldsymbol B_2$ has size $6\times9$.

The enhanced modes are not global DoFs and are eliminated by static condensation of the element equations.
With $\boldsymbol K_{uu}=\sum_g w_g\det\boldsymbol J_g\,\boldsymbol B_1^{\mathrm T}\boldsymbol D\boldsymbol B_1$, $\boldsymbol K_{ua}=\sum_g w_g\det\boldsymbol J_g\,\boldsymbol B_1^{\mathrm T}\boldsymbol D\boldsymbol B_2$ and $\boldsymbol K_{aa}=\sum_g w_g\det\boldsymbol J_g\,\boldsymbol B_2^{\mathrm T}\boldsymbol D\boldsymbol B_2$, the condensed stiffness is
$$
\boldsymbol K_e^{\mathrm{cond}}=\boldsymbol K_{uu}-\boldsymbol K_{ua}\boldsymbol K_{aa}^{-1}\boldsymbol K_{ua}^{\mathrm T}.
$$
The residual is condensed in the same way, with the internal amplitudes recovered locally from $\boldsymbol a=-\boldsymbol K_{aa}^{-1}(\boldsymbol K_{ua}^{\mathrm T}\boldsymbol u_e+\boldsymbol r_a)$, where $\boldsymbol r_a=\sum_g w_g\det\boldsymbol J_g\,\boldsymbol B_2^{\mathrm T}\boldsymbol\sigma$.

!!! note "developer note"
    The internal-mode amplitudes are not recovered by iteration: the stress is evaluated with a zero enhanced strain and condensed once with the current tangent, so for nonlinear materials the orthogonality condition $\boldsymbol r_a=0$ is only approximately enforced.

The formulation is the three-dimensional analogue of the Wilson incompatible-mode element and belongs to the enhanced-strain family of Taylor and Simo.
The static condensation enforces orthogonality of the incompatible strains to the stress field, which recovers the patch test on regular shapes.
The element is integrated with the Irons six-point rule, and no geometric nonlinearity is implemented.

## Syntax

```text title="C3D8I"
element C3D8I (1) (2...9) (10)
# (1) int, unique element tag
# (2...9) int, eight corner nodes with conventional order
# (10) int, material tag
```

## Remarks

1. `C3D8I` is `C3D8` with incompatible modes.
2. Nonlinearity is not implemented in `C3D8I`.

There are no optional arguments beyond the element tag, the eight node tags and a 3D material tag.
The nine internal modes are eliminated at element level, so the global system retains only the twenty-four translational DoFs of the eight nodes.
The element uses the same six-point Irons rule as the default scheme of [C3D8](C3D8.md), but it does not require hourglass control.
Strongly distorted elements degrade the patch-test correction, so reasonably regular bricks are recommended.
For finite-strain analysis use [C3D8](C3D8.md) with the nonlinear-geometry switch or the quadratic [C3D20](C3D20.md), because `C3D8I` has no total-Lagrangian formulation.

## References

1. [10.1016/B978-0-12-253250-4.50008-7](https://doi.org/10.1016/B978-0-12-253250-4.50008-7)
2. A non-conforming element for stress analysis
3. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
