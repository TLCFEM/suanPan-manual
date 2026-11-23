# Spring02

Spring Using Strain

* Number of DoFs: 2
* DoF Label: U1, U2

## Background

`Spring02` is the strain-based counterpart of [`Spring01`](Spring01.md).
The initial node separation $L=\lVert\mathbf x_j-\mathbf x_i\rVert$ is computed at initialisation, and a separation below $10^{-10}$ is replaced by $L=1$ to avoid division by zero.
With $\mathbf d=\mathbf x_j-\mathbf x_i$, the scaled direction $\mathbf b=\mathbf d/L^2$ gives the scalar input

$$
\epsilon=\mathbf b\cdot(\mathbf u_j-\mathbf u_i)
=\dfrac{\mathbf d\cdot(\mathbf u_j-\mathbf u_i)}{L^2}=\dfrac{\Delta}{L},
$$

so the material receives the axial strain $\epsilon$ and returns a stress $\sigma$ and tangent stiffness $k$.
The assembled stiffness and internal force are

$$
\mathbf K_e=\dfrac{k}{L^2}\mathbf c\,\mathbf c^{\mathrm T},
\qquad
\mathbf R_j=\dfrac{\sigma}{L}\mathbf c,\qquad \mathbf R_i=-\mathbf R_j,
$$

where $\mathbf c=\mathbf d/L$ is the initial unit direction.
The derivation of the rank-one projection and the remarks on fixed geometry are given on the [`Spring01`](Spring01.md) page.

!!! info "deviation from theory"
    For coincident or nearly coincident nodes the resulting strain is not physically meaningful.

!!! note "developer note"
    An initial length at or below $10^{-10}$ is replaced by $L=1$ before the direction vector is scaled.

## Syntax

```text title="Spring02"
element Spring02 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag
```

## Remarks

The `Spring02` uses strain as the input quantity and computes stress.

1. The material must use a stress--strain law, since the element divides the relative displacement by the initial length.
2. The initial length and axis are fixed at initialisation and are not updated.
3. For a law formulated in displacement and force, use [`Spring01`](Spring01.md) instead.

Note only infinitesimal strain/deformation formulation is supported.
If finite deformation, such as rigid body dynamics, is involved, analysts shall use `T2D2` and `T2D2S` elements.
