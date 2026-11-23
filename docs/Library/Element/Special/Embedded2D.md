# Embedded2D

2D Embedded Element

* Number of DoFs: 2
* DoF Label: U1, U2

## Background

An embedded (or immersed) element ties a slave node to a host continuum element without requiring the node to share a mesh line or nodes with the host.
A penalty constraint is enforced between the displacement of the embedded node and the displacement interpolated by the host element shape functions at the node position.

Let $$\mathbf u_s$$ be the displacement of the slave node and $$\mathbf u_a$$ those of the $$n_h$$ host nodes.
The host interpolant at the embedded point is $$\bar{\mathbf u}=\sum_a N_a(\mathbf\xi)\mathbf u_a$$, where $$\mathbf\xi$$ are the natural coordinates of that point in the host element.
The penalty energy $$\Pi=\tfrac12\alpha\lVert\mathbf u_s-\bar{\mathbf u}\rVert^2$$ gives the constraint vector and force

$$
\mathbf w=\begin{bmatrix}1&-N_1&\cdots&-N_{n_h}\end{bmatrix},\qquad
\mathbf R_e=\alpha\,(\mathbf u_s-\bar{\mathbf u})\,\mathbf w,
$$

with an associated tangent $$\alpha\,\mathbf w^{\mathrm T}\mathbf w$$ assembled once at initialisation.

The natural coordinates $$\mathbf\xi$$ are found by an iterative inverse mapping at initialisation.
Newton updates $$\mathbf\xi\leftarrow\mathbf\xi+\mathbf J^{-1}(\mathbf x_s-\mathbf N(\mathbf\xi)\mathbf X_h)$$ are performed with the shape-function Jacobian $$\mathbf J=\partial\mathbf N/\partial\mathbf\xi\,\mathbf X_h$$ until $$\lVert\Delta\mathbf\xi\rVert_\infty<10^{-14}$$ or 20 iterations are exhausted.
The shape functions are then frozen, so the penalty stiffness remains constant throughout the analysis.

!!! warning "implementation limitation"
    The natural coordinates are found once from the initial geometry and are not updated as the host element deforms.
    Initialization fails if the inverse mapping does not converge.

!!! note "developer note"
    The inverse mapping is capped at 20 iterations.

!!! info "deviation from theory"
    Only translational DoFs are tied.
    Rotational compatibility between the embedded node and the host rotation field is not enforced.

## Syntax

```text title="Embedded2D"
element Embedded2D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, host element tag
# (3) int, slave node tag
# [4] double, penalty factor, default: 1E4
```

## Remarks

1. Currently, the following element types are supported: [`CP4`](../Membrane/Plane/CP4.md), [`CP5`](../Membrane/Plane/CP5.md), [`CP7`](../Membrane/Plane/CP7.md) and [`CP8`](../Membrane/Plane/CP8.md).
2. If `[4]` is omitted, the parser uses a default penalty of $$1E4$$.
3. Only translational DoFs are tied, and the host element must provide shape functions and their derivatives in natural coordinates.
4. The slave node should lie inside the host element so that the inverse mapping converges to a meaningful point.
5. A small penalty permits relative slip, while an excessively large penalty degrades conditioning; see [`Tie`](Tie.md) for a purely algebraic penalty constraint and [`Contact2D`](Contact2D.md) for contact without mesh connectivity.
