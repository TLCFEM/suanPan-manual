# DC3D4

* Number of Nodes: 4
* Number of DoFs: 4 (Translation, Translation, Translation, Damage)
* DoF Label: U1, U2, U3, DAMAGE

## Theory

`DC3D4` is the phase-field fracture version of the four-node tetrahedron [C3D4](C3D4.md).
Each node carries three translational DoFs and one damage DoF, so the element has sixteen DoFs in total.
It follows the variational phase-field fracture model described in detail in [DC3D8](DC3D8.md), with the damage field interpolated by the same linear barycentric functions as the displacement field.

The crack surface is regularised by the functional $\Gamma_l(d)=\int_\Omega\left[\dfrac{d^2}{2l}+\dfrac{l}{2}|\nabla d|^2\right]\mathrm d\Omega$, where $d\in[0,1]$ is the damage field and $l$ is the characteristic length.
The elastic energy is degraded by $g(d)=\min\{1,(1-d)^2+\epsilon\}$, and the driving force is the history field $H$, the running maximum of $\frac12\mathbf\varepsilon:\mathbf\sigma$.
The discrete damage block is $\mathbf K_{dd}=\int_\Omega\left[(2H+G_c/l)\mathbf N^{\mathrm T}\mathbf N+G_c l\,(\nabla\mathbf N)^{\mathrm T}\nabla\mathbf N\right]\mathrm d\Omega$, with $G_c$ the energy release rate.

The tetrahedral element uses one integration point at the centroid, so all fields are constant over the element.
If the characteristic-length argument is negative, the implementation sets $l=2\sqrt[3]{V}$ from the element volume $V$.

!!! info "deviation from theory"
    The automatic length is twice the cube root of the element volume, whereas the hexahedral [DC3D8](DC3D8.md) uses $\sqrt[3]{V}$, so the two variants regularise the crack over different widths for the same element size.

## Syntax

```text title="DC3D4"
element DC3D4 (1) (2...5) (6) (7) (8)
# (1) int, unique element tag
# (2...5) int, four corner nodes with conventional order
# (6) int, material tag
# (7) double, characteristic length
# (8) double, energy release rate
```

## Remarks

The material tag must refer to a 3D material that supplies stress and tangent, while the damage evolution is governed by the element.
The energy release rate is the argument after the characteristic length and should be positive for a meaningful crack driving force.
A negative characteristic length triggers the automatic value $2\sqrt[3]{V}$, so the element size controls the regularised crack width.
`DC3D4` uses a staggered update in which the history field is frozen at its committed value while the damage equation is solved.
No tension-compression split is applied to the energy that drives damage in this implementation.

!!! info "deviation from theory"
    Unlike the standard Miehe formulation, the history field is driven by the full $\frac12\mathbf\varepsilon:\mathbf\sigma$ without a tensile-compressive split, so compressive straining can also grow damage.

## Variants

`DC3D4M` is the monolithic counterpart and is registered as `new_dc3d4<true>` in the element parser.
It accepts the same arguments as `DC3D4`: `element DC3D4M (1) (2...5) (6) (7) (8)` reads the element tag, four node tags, material tag, characteristic length and energy release rate.
Unlike `DC3D4`, it updates the history field to the trial value and adds the displacement-damage coupling blocks to the tangent, so displacement and damage are solved simultaneously.
For the hexahedral counterpart see [DC3D8](DC3D8.md) and its monolithic alias `DC3D8M`.

## References

1. [10.1002/nme.2861](https://doi.org/10.1002/nme.2861)
