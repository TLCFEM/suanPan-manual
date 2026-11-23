# Tie

Multipoint Constraint Implemented As Element

* Number of Nodes: varies
* Number of DoFs: varies

## Background

A `Tie` element imposes a linear multipoint constraint by the penalty method, without introducing Lagrange multipliers or additional unknowns.
For a weighted sum of selected DoFs the constraint is

$$
\sum_a w_a\,u_a=b ,
$$

where $b$ is the right-hand side and $w_a$ is the weight of the $a$-th DoF.
The penalty energy $\Pi=\tfrac12\alpha\big(\sum_a w_a u_a-b\big)^2$ gives the rank-one element stiffness and residual

$$
\boldsymbol K_e=\alpha\,\boldsymbol w\boldsymbol w^{\mathrm T},\qquad
\boldsymbol R_e=\alpha\,\boldsymbol w\big(\boldsymbol w^{\mathrm T}\boldsymbol u-b\big).
$$

As $\alpha\to\infty$ the constraint is enforced exactly, but a very large penalty makes the global system ill conditioned.

!!! info "deviation from theory"
    The penalty form enforces the constraint only approximately.
    The residual of the weighted sum is generally nonzero and scales as $1/\alpha$.

The element is purely algebraic, so it does not use nodal coordinates and the tied DoFs need not have the same type or belong to the same dimension.
A geometric constraint that attaches a node to a line is provided by [`TranslationConnector`](TranslationConnector.md).

## Syntax

```text title="Tie"
element Tie (1) (2) (3) [(4) (5) (6)...]
# (1) int, unique element tag
# (2) double, right hand side of the constraint equation, the constraint is homogeneous if this parameter is zero
# (3) double, penalty number, a relatively large number
# (4) int, node tag
# (5) int, dof tag
# (6) double, weight
```

## Example

Each `Tie` element can have multiple DoFs included.
For example, to define the following constraint,

$$
5u_2+6v_4=9,
$$

where $$u_2$$ and $$v_4$$ are horizontal displacement of node `2` and vertical displacement of node `4` in a 2D model, then

```
element Tie 1 9. 1E8 2 1 5. 4 2 6.
```

In the above command, a large number `1E8` is used as a penalty.

The `Tie` element does not care about the geometric implication.
The tied DoFs can be of different types.

To tie a node to a line, consider the [`TranslationConnector`](TranslationConnector.md) element.

The penalty should be large relative to the stiffness of the connected structure but not so large that the global matrix loses conditioning.
Because the tangent is rank one, a `Tie` element adds only one constrained mode and does not change the rank of the remaining system.
Setting the right-hand side to zero gives a homogeneous constraint, which is the usual choice for connecting coincident nodes.
