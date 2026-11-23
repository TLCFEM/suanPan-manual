# Contact2D

2D Node(Slave)-Line(Master) Contact Element

* Number of DoFs: 2
* DoF Label: U1, U2

## Background

The `Contact2D` element enforces frictionless unilateral contact between a slave node and the master line segments formed by consecutive nodes of a master group.
It is implemented as a finite element so that both the contact force and its consistent tangent are assembled directly into the global residual and stiffness.

Let $\boldsymbol r_1$ and $\boldsymbol r_2$ be the current positions of the two master nodes of one segment and $\boldsymbol r_3$ that of the slave node, each position being the sum of the original coordinate and the trial displacement.
The segment axis is $\boldsymbol l=\boldsymbol r_2-\boldsymbol r_1$ with length $l=\lVert\boldsymbol l\rVert$.
The outward unit normal is obtained by rotating the normalised axis by $\pi/2$,

$$
\boldsymbol n=\boldsymbol T\dfrac{\boldsymbol l}{l},\qquad
\boldsymbol T=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

Define $\boldsymbol s=\boldsymbol r_3-\boldsymbol r_1$.
Contact is active only when the penetration and the parametric coordinate satisfy

$$
u=\boldsymbol s\cdot\boldsymbol n\le 0,\qquad
t=\dfrac{\boldsymbol s\cdot\boldsymbol l}{\boldsymbol l\cdot\boldsymbol l}\in[0,1].
$$

The parameter $t$ is the closest-point projection of the slave node onto the segment, and the condition $0\le t\le 1$ excludes the extensions beyond the two end nodes.

!!! warning "implementation limitation"
    A slave node whose closest projection falls outside a segment is ignored even if it penetrates near an end node.
    Corner and edge contact are not treated.

The penalty method replaces the exact impenetrability constraint $u=0$ by a contact spring of stiffness $\alpha$ that resists penetration.
The resistance on the slave node is

$$
\boldsymbol F_3=\alpha\,u\,\boldsymbol n,
$$

and the equal-and-opposite reactions on the master nodes follow from force and moment equilibrium,

$$
\boldsymbol F_2=-\alpha\,t\,u\,\boldsymbol n,\qquad
\boldsymbol F_1=\alpha\,(t-1)\,u\,\boldsymbol n.
$$

The distribution $(1-t):t$ is the linear interpolation of the contact force to the segment end nodes, which is the classical 2D node-to-segment weighting.
The tangent stiffness is the consistent linearisation $\boldsymbol K_e=-\partial\boldsymbol F/\partial\boldsymbol r$ of the three nodal resistance vectors.
Because $\boldsymbol n$ depends on the orientation of the segment, its derivative

$$
\dfrac{\partial\boldsymbol n}{\partial\boldsymbol l}=\dfrac{1}{l}\left(\boldsymbol T-\boldsymbol n\otimes\dfrac{\boldsymbol l}{l}\right)
$$

is retained, so the tangent remains symmetric and quadratic convergence of the Newton iteration is preserved.
A positive $\alpha$ gives a repulsive force opposite to $\boldsymbol n$ for $u<0$.
The gap is not enforced exactly: the residual penetration is of order $1/\alpha$, so increasing $\alpha$ reduces penetration at the cost of conditioning.
No tangential traction is included, so the contact is frictionless.

!!! warning "implementation limitation"
    General contact formulations include a tangential traction and a Coulomb friction law.
    Only the normal penalty force is assembled here, so frictional sliding cannot be represented by this element.

## Syntax

```text title="Contact2D"
element Contact2D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, master group tag
# (3) int, slave group tag
# [4] double, penalty factor
```

## Remarks

1. The contact algorithm is implemented via penalty function method as an element.
   The parameter `[4]` controls the magnitude of penalty.
2. No matter whether the `nlgeom` switch is on or off for connected elements, the contact detection itself is always conducted in a nonlinear manner, similar to the total Lagrangian formulation.
3. The node-line contact detection is performed for all nodes defined in slave group and lines defined by nodes in master group.
   There are $n-1$ line segments for $n$ nodes in master group.
4. Master nodes can penetrate lines formed in slave group.
   To prevent this, define a new `Contact2D` element by swapping the order of slave and master groups.
5. Example usage can be seen in the [example](../../../Example/Structural/Contact/contact-between-beam-and-block.md).
6. If `[4]` is omitted, the parser uses a default penalty of $$1E6$$.
7. The penalty acts only on the normal gap; there is no friction or tangential penalty, and a shear transfer must be modelled with a separate element such as [`Tie`](Tie.md).
8. Contact detection always uses current trial positions, so geometric nonlinearity is active even when the connected elements use a linear formulation.
9. For the spatial counterpart based on triangular facets, see [`Contact3D`](Contact3D.md).

## References

1. [ISBN 978-0-521-34796-9](https://search.worldcat.org/search?q=bn:9780521347969)
2. [10.1002/nme.2559](https://doi.org/10.1002/nme.2559)
3. [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
