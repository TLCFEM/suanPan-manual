# Joint

Joint Element

The `Joint` is a joint element that uses **displacement** as inputs.

* Number of Nodes: 2
* Number of DoFs: varies

## Background

A joint connects two nodes that may occupy the same coordinates with a set of independent nonlinear springs, one per connected degree of freedom.
Because the nodes can coincide, the element is effectively zero length: no axis or element length is used and the relative displacement is passed directly to each material as a scalar deformation.

For the $$k$$-th connected DoF, let $$u_i^{(k)}$$ and $$u_j^{(k)}$$ be the displacement components of the two nodes.
The material receives

$$
\Delta^{(k)}=u_i^{(k)}-u_j^{(k)},
$$

and returns a force $$N^{(k)}$$ with tangent stiffness $$k^{(k)}=\mathrm dN^{(k)}/\mathrm d\Delta^{(k)}$$.
The element assembles $$R_i^{(k)}=N^{(k)}$$, $$R_j^{(k)}=-N^{(k)}$$ and the two-by-two block

$$
\begin{bmatrix}1&-1\\-1&1\end{bmatrix}k^{(k)}
$$

for each connected DoF.

The number of material tags equals the number of connected DoFs per node, so $$m$$ material tags create $$2m$$ element DoFs and the materials act in the order in which the tags are given.
No geometric transformation is applied, so the connected DoFs are the global directions encoded on the nodes.
This is the multi-DoF generalisation of the single-direction [`Spring01`](Spring01.md) element.

!!! info "deviation from theory"
    A general joint element projects the relative displacement into a local coordinate system before passing it to the material.
    This element passes the global displacement components directly, so kinematic coupling between directions is not represented.

!!! warning "implementation limitation"
    Initialization fails unless the number of material tags equals the number of DoFs per node.

## Syntax

```text title="Joint"
element Joint (1) (2) (3) (4...)
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4...) int, material tags
```

## Remarks

The `Joint` element defines a joint connecting two nodes that can coincide with each other regarding their coordinates.
The relative displacement is used as strain input.
Thus, the corresponding material model shall be defined to use displacement and force.
Note in the current implementation the global horizontal and vertical displacements are passed to the material models to compute the response.

The number of connected degrees of freedom can vary based on the number of tags of material models assigned to the element.
The material models are used for each DoF sequentially according to the definition.
If one wants to define a joint tagged `5` between node `1` and node `2` using material `3` for the first four DoFs, the following command can be used.

```
element Joint 5 1 2 3 3 3 3
```

The material models must use a displacement--force law, because the input is a relative displacement rather than a strain.
For a single connected direction with a defined axis, prefer [`Spring01`](Spring01.md), which projects onto the element direction instead of using global components.
To impose a constraint instead of a force--deformation relation, use [`Tie`](Tie.md).
