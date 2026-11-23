# DC3D8

* Number of Nodes: 8
* Number of DoFs: 4 (Translation, Translation, Translation, Damage)
* DoF Label: U1, U2, U3, DAMAGE

## Theory

`DC3D8` is the phase-field fracture version of the eight-node brick [C3D8](C3D8.md).
Each node carries three translational DoFs and one DAMAGE DoF, giving 32 element DoFs.
The damage field is interpolated by the same trilinear shape functions as the displacement field, and a scalar field replaces a sharp crack surface.

The total potential energy is
$$
\Psi=\int_\Omega g(d)\psi(\mathbf\varepsilon)\,\mathrm d\Omega+G_c\int_\Omega\left[\frac{d^2}{2l}+\frac l2|\nabla d|^2\right]\mathrm d\Omega,
$$
where $\psi=\frac12\mathbf\varepsilon:\mathbf\sigma$ is the elastic energy density built from the strain and stress returned by the material, $g(d)$ is the degradation function, $G_c$ is the energy release rate and $l$ is the characteristic length.

!!! info "deviation from theory"
    The quadratic form $\frac12\mathbf\varepsilon:\mathbf\sigma$ equals the strain energy density only for a linear elastic host, whereas the element uses it as the damage driver for any 3D material so a nonlinear host is not driven by the true $\int\mathbf\sigma:\mathrm d\mathbf\varepsilon$.

The implementation uses
$$
g(d)=\min\left\{1,(1-\mathbf N\mathbf d)^2+\epsilon\right\},\qquad \epsilon=\mathrm{eps}(\mathrm{float}),
$$
where $\mathbf d$ collects the nodal damage values and $d$ is thereby limited to $[0,1]$.

!!! info "deviation from theory"
    The degradation is clamped so that the residual stiffness at $d=1$ is essentially zero rather than the finite residual stiffness used to keep the tangent nonsingular in regularised formulations.

!!! note "developer note"
    The clamp uses $\min\{1,\cdot\}$ with $\epsilon$ equal to the single-precision machine epsilon.

Irreversibility of crack growth is enforced with a history field that stores the maximum elastic energy reached at a material point.
At each integration point the trial value is $\mathcal H^\mathrm{trial}=\frac12\mathbf\varepsilon:\mathbf\sigma$, updated as $\mathcal H=\max(\mathcal H_\mathrm{old},\mathcal H^\mathrm{trial})$.
No tension-compression split of the elastic energy is applied in this implementation, so compressive straining can also increase the driving force.

!!! info "deviation from theory"
    Standard phase-field fracture models split the elastic energy into tensile and compressive parts so that compression does not drive cracking, but this element uses the full $\frac12\mathbf\varepsilon:\mathbf\sigma$ as the history-field driver, so compressive states also grow damage.

With $\mathbf N$ and $\nabla\mathbf N$ the shape functions and their physical gradients, the displacement and damage blocks are
$$
\mathbf K_{uu}=\int_\Omega g(d)\mathbf B^{\mathrm T}\mathbf D\mathbf B\,\mathrm d\Omega,\qquad
\mathbf r_u=\int_\Omega g(d)\mathbf B^{\mathrm T}\mathbf\sigma\,\mathrm d\Omega,
$$
$$
\mathbf K_{dd}=\int_\Omega\left[(2\mathcal H+G_c/l)\mathbf N^{\mathrm T}\mathbf N+G_c l\,(\nabla\mathbf N)^{\mathrm T}\nabla\mathbf N\right]\mathrm d\Omega,\qquad
\mathbf r_d=\mathbf K_{dd}\mathbf d-2\mathcal H\int_\Omega\mathbf N^{\mathrm T}\,\mathrm d\Omega.
$$
The monolithic variant `DC3D8M` adds the coupling block $\mathbf K_{ud}=-2\int_\Omega(1-d)\mathbf B^{\mathrm T}\mathbf\sigma\mathbf N^{\mathrm T}\,\mathrm d\Omega$ and its transpose, and advances $\mathcal H$ to the trial value.
The staggered `DC3D8` variant omits the coupling blocks and holds $\mathcal H$ at its committed value during the damage solve.

The element uses the $2\times2\times2$ Gauss rule.
If the characteristic-length argument is negative, the implementation sets $l=\sqrt[3]{V}$ from the element volume $V$.

## Syntax

```text title="DC3D8"
element DC3D8 (1) (2...9) (10) (11) (12)
# (1) int, unique element tag
# (2...9) int, eight corner nodes with conventional order
# (10) int, material tag
# (11) double, characteristic length
# (12) double, energy release rate
```

## Remarks

The material tag supplies the mechanical constitutive law, and no separate damage material is needed.
The characteristic length is the first numerical argument after the material tag and the energy release rate is the second.
A negative characteristic length triggers automatic sizing as $\sqrt[3]{V}$, which ties the regularised crack width directly to the element size.
`DC3D8` solves displacement and damage in a staggered fashion, whereas `DC3D8M` assembles the fully coupled tangent and solves both fields simultaneously.
Use a mesh with several elements across the expected crack width, since an under-resolved damage band gives a brittle and mesh-dependent response.
For the tetrahedral version and its monolithic alias see [DC3D4](DC3D4.md).

## References

1. [10.1002/nme.2861](https://doi.org/10.1002/nme.2861)
