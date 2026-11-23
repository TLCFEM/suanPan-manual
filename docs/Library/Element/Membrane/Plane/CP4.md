# CP4

Bilinear Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2
* Integration Scheme: 2nd Order Gaussian (Full) or 1st Order Gaussian (Reduced)
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

[`CP4`](CP4.md) is the four-node isoparametric quadrilateral, also known as the bilinear quad or Q4.
Its shape functions in parent coordinates $(\xi,\eta)\in[-1,1]^2$ are
$$
N_1=\tfrac14(1-\xi)(1-\eta),\quad N_2=\tfrac14(1+\xi)(1-\eta),\quad N_3=\tfrac14(1+\xi)(1+\eta),\quad N_4=\tfrac14(1-\xi)(1+\eta).
$$
The nodes are ordered counter-clockwise starting at $(\xi,\eta)=(-1,-1)$, so node 5 of a quadratic edge is inserted between nodes 1 and 2 in [`CP5`](CP5.md).
The isoparametric map $\boldsymbol x=\sum_aN_a\boldsymbol x_a$ gives the Jacobian $\boldsymbol J=\partial\boldsymbol x/\partial\boldsymbol\xi$, and the physical shape-function gradients are $\nabla N_a=\boldsymbol J^{-\mathrm T}\nabla_{\!\xi}N_a$.
The small-strain vector is $\boldsymbol\varepsilon=\boldsymbol B\boldsymbol a$, with
$$
\boldsymbol B=\begin{bmatrix}
N_{1,x}&0&N_{2,x}&0&N_{3,x}&0&N_{4,x}&0\\
0&N_{1,y}&0&N_{2,y}&0&N_{3,y}&0&N_{4,y}\\
N_{1,y}&N_{1,x}&N_{2,y}&N_{2,x}&N_{3,y}&N_{3,x}&N_{4,y}&N_{4,x}
\end{bmatrix}.
$$
The stiffness and internal force are assembled as $\boldsymbol K^e=\sum_q t\,J_qw_q\,\boldsymbol B_q^\mathrm T\boldsymbol D_q\boldsymbol B_q$ and $\boldsymbol f^e=\sum_q t\,J_qw_q\,\boldsymbol B_q^\mathrm T\boldsymbol\sigma_q$.

Full integration uses a $2\times2$ Gauss rule, which is exact for the bilinear stiffness of a parallelogram.
Reduced integration uses one point at the element centre, where the strain sampled is the mean strain of the element.
One-point integration admits the two hourglass displacement patterns $\boldsymbol h=[1,-1,1,-1]$ in the $x$ and $y$ directions, which produce no strain at the centre and would otherwise make the stiffness matrix rank deficient.

The stabilisation follows the orthogonal hourglass projection of Flanagan, Belytschko and co-workers.
The physical hourglass vector is obtained by projecting the algebraic mode $\boldsymbol h$ orthogonal to the rigid-body and constant-strain modes,
$$
\boldsymbol\gamma=\boldsymbol h-(\boldsymbol h\cdot\boldsymbol x)\,\boldsymbol b_1-(\boldsymbol h\cdot\boldsymbol y)\,\boldsymbol b_2.
$$
Here $\boldsymbol b_1$ and $\boldsymbol b_2$ are the centre-point shape-function gradients divided by $\texttt{double\_area}$, the quantity computed from the nodal coordinates that equals twice the element area $A$.
The stabilisation matrix is added to the stiffness as $\mu\,(2t/A)\,\boldsymbol\gamma\boldsymbol\gamma^\mathrm T$, and the corresponding hourglass force is $\mu\,(2t/A)(\boldsymbol\gamma^\mathrm T\boldsymbol a)\boldsymbol\gamma$.

When the nonlinear geometry switch is set, the element uses a Total Lagrangian formulation.
The trial deformation gradient is $\boldsymbol F=\boldsymbol I+\sum_a\boldsymbol u_a\otimes\nabla N_a$, and the Green-Lagrange strain $\boldsymbol E=(\boldsymbol F^\mathrm T\boldsymbol F-\boldsymbol I)/2$ is passed to the material.
The second Piola-Kirchhoff stress returned by the material is contracted with the nonlinear strain-displacement matrix $\boldsymbol B_{NL}$, and an initial-stress geometric stiffness is assembled from that stress and the shape-function gradients.

## Syntax

```text title="CP4"
element CP4 (1) (2...5) (6) [7] [8] [9] [10]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
# [8] bool string, reduced integration switch, default: false
# [9] bool string, nonlinear geometry switch, default: false
# [10] double, hourglassing penalty multiplier, default: 1.0
```

## Remarks

* The `CP4` element resembles CPS4 and CPE4 elements in ABAQUS.

!!! info "deviation from theory"
    Only `CP4` and `CP4R` are accepted element tokens; the names CPS4, CPE4, CPS4R and CPE4R are not registered and cannot be used in an `element` command.
    Plane stress or plane strain is selected by the material plane type, not by a separate element name.

!!! note "developer note"
    The class documentation mentions CPS4, CPE4, CPS4R and CPE4R, but the element parser registers only the tokens `CP4` and `CP4R`.

* The full integration scheme uses 2-by-2 Gaussian scheme and the reduced integration uses a single integration point at the center of the element.
* The reduced integration scheme also imports anti-hourglassing technique.
* The thickness `(7)` is ignored and forced to unity when the material uses plane strain.
* The characteristic length used by nonlocal or damage materials is $\sqrt{A}$, with $A$ the element area computed by the shoelace formula.
* The nonlinear geometry switch `(9)` activates the Total Lagrangian formulation with Green-Lagrange strain and a geometric stiffness.
* Full integration is prone to shear and volumetric locking in bending and nearly incompressible plasticity; reduced integration with hourglass control is the cheaper alternative.
* For assumed-stress and enhanced-strain alternatives that do not need hourglass control, see [`PS`](../Mixed/PS.md), [`QE2`](../Mixed/QE2.md) and [`CP4I`](CP4I.md).

For the hourglassing control, see [10.1016/0045-7825(84)90067-7](https://doi.org/10.1016/0045-7825(84)90067-7).
The hourglassing penalty multiplier (denoted as $$\mu$$) is an overall multiplier that is applied to the hourglassing stiffness matrix.

$$
\mu\mathbf{\gamma}\mathbf{\gamma}^\mathrm{T}.
$$

In the above, $$\mathbf{\gamma}$$ is identical to Eq. (19) in the reference paper.
Thus, $$\mu$$ shall be set to some value proportional to the elastic modulus.
The code forms the hourglass vectors with the centre gradients divided by $\texttt{double\_area}=2A$, then multiplies $\boldsymbol\gamma\boldsymbol\gamma^\mathrm T$ by $2t\mu/A$.
The penalty argument is converted to its absolute value, so a negative entry has the same effect as a positive one.

!!! warning "implementation limitation"
    The default hourglass multiplier is unity and it is not scaled by the elastic modulus.
    For a material with a modulus of order GPa the default stabilisation is negligible, so reduced integration requires a multiplier scaled with the material stiffness and a reference area.

## Variants

`CP4R` forces reduced integration with hourglassing control, so the reduced-integration switch is dropped: `element CP4R (1) (2...5) (6) [7] [8] [9]` reads thickness, nonlinear-geometry switch and hourglassing penalty multiplier.
`NonlocalCP4` is the nonlocal-damage variant; `element NonlocalCP4 (1) (2...5) (6) [7]` takes the material tag and optional thickness (default 1.0), requires a material with exactly one nonlocal variable, and adds an NL1 DoF at every node.

## References

1. [10.1016/0045-7825(84)90067-7](https://doi.org/10.1016/0045-7825(84)90067-7)
2. [10.1002/nme.1620170504](https://doi.org/10.1002/nme.1620170504)
3. [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)
4. [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
