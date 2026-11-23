# Spring01

Spring Using Displacement

* Number of DoFs: 2
* DoF Label: U1, U2

## Background

A zero-length spring connects the translations of two nodes with a force that depends only on their relative displacement, so it introduces no geometric length scale.
Let $\mathbf c$ be the unit direction from node $i$ to node $j$, computed once from the initial coordinates.
The material is given the scalar relative displacement

$$
\Delta=\mathbf c\cdot(\mathbf u_j-\mathbf u_i),
$$

and returns a force $N$ together with the tangent stiffness $k=\mathrm dN/\mathrm d\Delta$.
The element assembles the rank-one stiffness and the internal force

$$
\mathbf K_e=k\begin{bmatrix}\mathbf c\\-\mathbf c\end{bmatrix}
\begin{bmatrix}\mathbf c&-\mathbf c\end{bmatrix}^{\mathrm T},
\qquad
\mathbf R_i=-N\mathbf c,\qquad \mathbf R_j=N\mathbf c .
$$

Unlike [`Spring02`](Spring02.md), there is no division by the initial node separation, so the input is a displacement and the material must use a displacement--force law such as a linear or hysteretic spring.
The direction $\mathbf c$ is fixed at initialisation and the formulation is infinitesimal.
For finite deformation or rigid-body motion, use the truss elements `T2D2` and `T2D2S`, which update the axis and use a proper strain measure.

!!! info "deviation from theory"
    A conventional axial spring converts the relative displacement into strain by dividing by the member length.
    This element passes the raw projected displacement, so the material stiffness has units of force per length.

!!! warning "implementation limitation"
    The direction cosine is frozen at initialization and no geometric stiffness is formed.
    Finite rotations and follower-load effects are not captured.

The same projection is used by [`Damper01`](Damper01.md), which passes both projected displacement and projected velocity to a viscosity material.
When the two nodes coincide, the direction is undefined, and a multi-DoF connection should use [`Joint`](Joint.md) instead.

## Syntax

```text title="Spring01"
element Spring01 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag
```

## Remarks

The `Spring01` uses displacement as the input quantity and computes force.
It can be used as a zero-length element to connect two nodes.

Note only infinitesimal strain/deformation formulation is supported.
If finite deformation, such as rigid body dynamics, is involved, analysts shall use `T2D2` and `T2D2S` elements.

1. The material stiffness has units of force per length, since the input is a displacement rather than a strain.
2. The element axis is taken from the initial coordinates and is not updated during the analysis.
3. The two nodes must not coincide, otherwise the direction cosine cannot be normalised.
4. See [`Spring02`](Spring02.md) for the strain-based variant and [`Joint`](Joint.md) for a coincident-node connection with several DoFs.
