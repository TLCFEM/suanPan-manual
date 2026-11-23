# Embedded3D

3D Embedded Element

* Number of DoFs: 3
* DoF Label: U1, U2, U3

## Background

`Embedded3D` is the spatial counterpart of [`Embedded2D`](Embedded2D.md).
It ties the three translations of a slave node to the displacement interpolated by a solid host element at that node's position, using the same penalty formulation.

With host shape functions $$N_a$$ evaluated at the natural coordinates $$\mathbf\xi=(\xi,\eta,\zeta)$$ of the embedded point, the constraint force is

$$
\mathbf R_e=\alpha\left(\mathbf u_s-\sum_a N_a\mathbf u_a\right)
\begin{bmatrix}1&-N_1&\cdots&-N_{n_h}\end{bmatrix}.
$$

The point $$\mathbf\xi$$ is located once at initialisation by Newton iteration on $$\mathbf J^{-1}(\mathbf x_s-\mathbf N\mathbf X_h)$$, where $$\mathbf J=\partial\mathbf N/\partial\mathbf\xi\,\mathbf X_h$$ is the host Jacobian, and the resulting tangent $$\alpha\,\mathbf w^{\mathrm T}\mathbf w$$ is kept constant for the analysis.
The full derivation and the choice of penalty factor are discussed on the [`Embedded2D`](Embedded2D.md) page.

!!! warning "implementation limitation"
    The natural coordinates and shape functions are fixed from the initial host geometry and are not updated during the analysis.
    Initialization fails if the inverse mapping does not converge.
    No rotational DoFs are tied.

!!! note "developer note"
    The inverse mapping uses Newton iteration and is capped at 20 iterations.

## Syntax

```text title="Embedded3D"
element Embedded3D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, host element tag
# (3) int, slave node tag
# [4] double, penalty factor, default: 1E4
```

## Remarks

1. Currently, the following element types are supported: [`C3D8`](../Cube/C3D8.md) and [`C3D20`](../Cube/C3D20.md).
2. If `[4]` is omitted, the parser uses a default penalty of $$1E4$$.
3. All three translations are tied with the same penalty and no rotational coupling is introduced.
4. The inverse mapping uses the initial geometry, so large host distortions are not tracked; see [`Embedded2D`](Embedded2D.md) for further remarks.
