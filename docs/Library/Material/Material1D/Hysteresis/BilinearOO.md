# BilinearOO

Bilinear Origin Oriented Model

## Theory

The [SimpleHysteresis](SimpleHysteresis.md) framework supplies the branch logic, and this model supplies a bilinear backbone on each side.
For the tension side the backbone is

$$
\sigma=E\varepsilon\quad(\varepsilon\le\varepsilon_y^+),\qquad
\sigma=\sigma_y^++E_h^+(\varepsilon-\varepsilon_y^+)\quad(\varepsilon>\varepsilon_y^+),
$$

where $$\varepsilon_y^+=\sigma_y^+/E$$ and $$E_h^+$$ is the hardening modulus.
The compression backbone is the mirror expression with negative strain and negative yield stress.
The input hardening argument is a ratio, so the code sets $$E_h=rE$$.
An origin-oriented rule unloads and reloads toward the origin, so the residual strain after unloading to zero stress is zero.
The residual functions of the origin-oriented base implement this by returning zero.
The inner branches therefore connect the last tension and compression reversal points through the origin, giving the pinched, stiffness-degrading shape visible in the example.
The stress is clamped to zero when evaluation of the wrong-sign backbone would give a stress of the wrong sign, and the tangent is then set to a near-zero value.
For the peak-oriented counterpart in which unloading follows the initial elastic slope to a nonzero residual strain, see [BilinearPO](BilinearPO.md).

!!! info "deviation from theory"
    The stress is forced to zero whenever a backbone would give a stress of the wrong sign, and the tangent is then set to $$10^{-10}$$.
    This clipping prevents a backbone from crossing the strain axis and is not part of an ideal bilinear plasticity formulation.

## Syntax

For symmetric response between compression and tension,

```text title="BilinearOO"
material BilinearOO (1) (2) (3) (4) [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield strain
# (4) double, hardening ratio
# [5] double, density, default: 0.0
```

For asymmetric response,

```
material BilinearOO (1) (2) (3) (4) (5) (6) [7]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, tension yield strain
# (4) double, tension hardening ratio
# (5) double, compression yield strain
# (6) double, compression hardening ratio
# [7] double, density, default: 0.0
```

## History Variable Layout

Since it is derived from the [`SimpleHysteresis`](../Hysteresis/SimpleHysteresis.md) model, it shares the same history variable layout.

## Remarks

- The input yield quantities are strains, not stresses, and both the elastic modulus and the yield strains are converted to absolute values.
- The hardening arguments are ratios with respect to $$E$$, so the example value 0.02 corresponds to a post-yield modulus of $$0.02E$$.
- In the asymmetric form the compression yield strain is stored as a negative value and its hardening ratio may also be negative, which produces a softening post-yield compression branch.
- The model is rate independent and has no degradation or pinching parameters beyond the origin-oriented rule itself.
- The state is stored in the eight history variables of [SimpleHysteresis](SimpleHysteresis.md), and there are no parameters for isotropic hardening.
- Use it with one-dimensional truss or beam elements, and prefer [MultilinearOO](MultilinearOO.md) when the backbone is known as a table of points.

## Example

### Symmetric Response

```
material BilinearOO 1 2E4 1E-3 .02
materialTest1D 1 1E-4 50 100 150 200 250 300 150
```

![example one](BilinearOO.EX1.svg)

### Asymmetric Response

```
material BilinearOO 1 2E4 1E-3 .02 2E-3 -.05
materialTest1D 1 1E-4 50 100 150 200 250 300 150
```

![example two](BilinearOO.EX2.svg)

## References

- Clough, R. W. and Johnston, S. B. (1966), "Effect of stiffness degradation on earthquake ductility requirements", Report 66-16, University of California, Berkeley.
- Ibarra, L. F., Medina, R. A. and Krawinkler, H. (2005), "Hysteretic models that incorporate strength and stiffness deterioration", Earthquake Engineering and Structural Dynamics, 34(12), 1489-1511, doi:10.1002/eqe.495.
