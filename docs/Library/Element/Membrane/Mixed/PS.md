# PS

Pian-Sumihara Quadrilateral Element

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2
* Supports Body Force
* Integration Scheme: 2nd Order Gauss
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

[`PS`](PS.md) is the four-node assumed-stress quadrilateral of Pian and Sumihara.
It is based on a Hellinger-Reissner or complementary-energy functional in which the stress field and the displacement field are interpolated independently.
The stress interpolation uses the five-parameter pattern
$$
\mathbf P=\begin{bmatrix}
1&0&0&T_{11}\eta&T_{12}\xi\\
0&1&0&T_{21}\eta&T_{22}\xi\\
0&0&1&T_{31}\eta&T_{32}\xi
\end{bmatrix},
$$
where the first column of $$\mathbf T$$ is $$[(\partial x/\partial\xi)^2,(\partial y/\partial\xi)^2,(\partial x/\partial\xi)(\partial y/\partial\xi)]^\mathrm T$$ and the second column is the same expression with $$\xi$$ replaced by $$\eta$$.
The last two columns are therefore the natural-coordinate linear terms $$\eta$$ and $$\xi$$ mapped to physical strain components, which makes the element insensitive to distortion.
With the strain interpolation $$\mathbf\varepsilon=\mathbf B\mathbf a$$ and the elastic compliance $$\mathbf D^{-1}$$, the compatibility and equilibrium matrices are
$$
\mathbf H=\sum_q\mathbf P_q^\mathrm T\mathbf D^{-1}\mathbf P_q\,w_q,\qquad \mathbf N=\sum_q\mathbf P_q^\mathrm T\mathbf B_q\,w_q.
$$
The stress parameters follow from stationarity as $$\mathbf\beta=\mathbf H^{-1}\mathbf N\mathbf a$$, and the stiffness reduces to
$$
\mathbf K^e=\mathbf N^\mathrm T\mathbf H^{-1}\mathbf N.
$$
Because the strain is recovered directly from the assumed stress through $$\mathbf\varepsilon=\mathbf D^{-1}\mathbf P\mathbf\beta$$, no local nonlinear solve is needed when the material is nonlinear.
The element therefore keeps the low cost of [`CP4`](../Plane/CP4.md) while avoiding shear locking.

!!! info "deviation from theory"
    Unlike a fully nonlinear assumed-stress formulation, the stress modes do not adapt to a changing material tangent.

!!! note "developer note"
    A fully nonlinear assumed-stress formulation would rebuild the compatibility matrix $$\mathbf H$$ from the current tangent at every iteration.
    Here the strain interpolation is calibrated once against the initial elastic stiffness.

## References

1. [10.1002/nme.1620200911](https://doi.org/10.1002/nme.1620200911)
2. [10.1002/nme.6066](https://doi.org/10.1002/nme.6066)
3. [ISBN 978-0-486-41181-1](https://search.worldcat.org/search?q=bn:9780486411811)

## Syntax

```text title="PS"
element PS (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

1. The original five-parameter stress field is used for stress interpolation.
2. The mixed framework is used to extend the original formulation to accommodate elastoplastic applications.
3. As there is no enhanced strain, no local iteration is required.
   Hence `PS` is faster than elements such as `QE2`.
4. The thickness argument is ignored when the material declares plane strain.
5. Four Gauss points are used, and the characteristic length is $$\sqrt{A}$$ with $$A$$ the element area.
6. The assumed stress is recovered from the material strain, so stress recording follows the same path as in [`CP4`](../Plane/CP4.md).
7. [`QE2`](QE2.md) adds two enhanced strain modes for better distortion sensitivity at a higher cost, while [`CP4I`](../Plane/CP4I.md) uses incompatible displacements.
