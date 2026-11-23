# Contact3D

3D Node(Slave)-Triangular Facet(Master) Contact Element

* Number of DoFs: 3
* DoF Label: U1, U2, U3

## Background

`Contact3D` is the spatial counterpart of [`Contact2D`](Contact2D.md).
It enforces frictionless node-to-facet contact between slave nodes and the triangular facets formed from the master node group using the same penalty idea.
The full derivation of the penalty method, the gap definition and the consistent tangent is given on the [`Contact2D`](Contact2D.md) page, so only the 3D-specific geometry is summarised here.

Three consecutive master nodes $(\mathbf r_i,\mathbf r_j,\mathbf r_k)$ define one planar facet with outward unit normal $\mathbf n_f$ and area $A_f$.
For a slave node at $\mathbf r_s$, the signed normal gap is

$$
g=\mathbf n_f\cdot(\mathbf r_s-\mathbf r_i)\le 0.
$$

The projection is accepted only when it falls inside the triangle, which the implementation tests with three edge-based quantities $h_i$, $h_j$ and $h_k$ formed from the edge normals.
If any $h$ is positive, the closest point lies outside the facet and the pair is skipped.
The nodal weights are the barycentric coordinates $n_i=h_i/A_f$, $n_j=h_j/A_f$ and $n_k=h_k/A_f$.
The penalty resistance is assembled as

$$
\mathbf F_s=\alpha\,g\,\mathbf n_f,\qquad
\mathbf F_i=\alpha\,n_i\,g\,\mathbf n_f,\qquad
\mathbf F_j=\alpha\,n_j\,g\,\mathbf n_f,\qquad
\mathbf F_k=\alpha\,n_k\,g\,\mathbf n_f.
$$

The consistent tangent contains the derivatives of $\mathbf n_f$ with respect to all three master nodes as well as the derivatives of the barycentric weights.
All facets and slave positions are updated from the current trial configuration before the contact check.

!!! warning "implementation limitation"
    Contact is checked only when the projection lies inside a master triangle.
    A slave node outside all facets is ignored even if it is close to an edge.
    The facet normal is divided by the facet area without a degeneracy guard, so zero-area triangles must be avoided.

!!! info "deviation from theory"
    This is a one-pass node-to-facet scheme.
    Master nodes are not tested against slave facets, so master-side penetration requires a second element with the groups swapped.

## Syntax

```text title="Contact3D"
element Contact3D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, master group tag
# (3) int, slave group tag
# [4] double, penalty factor
```

## Remarks

1. The contact algorithm is implemented via penalty function method as an element.
   The parameter `[4]` controls the magnitude of penalty.
2. No matter whether the `nlgeom` switch is on or off for connected elements, the contact detection itself is always conducted in a nonlinear manner, similar to the total Lagrangian formulation for the precise computation of contact.
3. The node-facet contact detection is performed for all nodes defined in slave group and facets defined by nodes in master group.
   There are $$n/3$$ facets for $$n$$ nodes in master group.
   So the number of nodes in master group must be a multiple of $$3$$.
4. If `[4]` is omitted, the parser uses a default penalty of $$1E6$$.
5. Master facets are flat triangles and the contact is frictionless, so only a normal penalty force is transferred.
6. This is a one-pass scheme, hence master nodes can penetrate slave facets; define a second element with the groups swapped to detect that case, as described on the [`Contact2D`](Contact2D.md) page.

## References

1. [ISBN 978-0-521-34796-9](https://search.worldcat.org/search?q=bn:9780521347969)
2. [10.1016/j.cma.2009.06.022](https://doi.org/10.1016/j.cma.2009.06.022)
