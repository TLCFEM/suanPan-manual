# ExpCC

Exponential Hardening Cam-Clay Model

This hardening law is identical to the one documented in the ABAQUS manual (4.4.3).

## Background

Critical state soil mechanics describes a saturated soil in terms of the effective stress $\boldsymbol\sigma'=\boldsymbol\sigma+u\boldsymbol I$, where $u$ is the pore pressure.
For isotropic compression the specific volume $v=1+e$ decreases linearly with $\ln p'$ along the virgin consolidation line $v=N-\lambda\ln p'$ and recovers along the swelling line $v=v_\kappa-\kappa\ln p'$, with $\lambda>\kappa>0$.
Continued shearing drives the soil towards the critical state line $v=\Gamma-\lambda\ln p'$ and $q=Mp'$, where both the volume and the stress ratio become constant.
The parameter $\Gamma$ is the specific volume on the critical state line at $p'=1$ unit of stress, $N$ is the corresponding intercept of the virgin consolidation line, and $M$ is the slope of the critical state line.
For triaxial compression $q=\sigma'_1-\sigma'_3$ and $M=6\sin\phi'/(3-\sin\phi')$, while triaxial extension gives $M=6\sin\phi'/(3+\sin\phi')$.
The overconsolidation ratio $OCR=p'_c/p'$ compares the preconsolidation pressure with the current mean effective stress and determines on which side of critical the soil starts.
The modified Cam-Clay yield surface is the ellipse $q^2=M^2p'(p'_c-p')$, which passes through the origin and reaches its maximum at the critical state $p'=p'_c/2$ and $q=Mp'_c/2$.
When $p_t=0$ and $\beta=1$, the preconsolidation pressure is $p'_c=2a$, so the hardening variable $a$ directly measures the size of the yield surface.
With associated flow, states on the dry side of critical compact and harden, while states on the wet side dilate and soften until the critical state is reached.
The original Cam-Clay of Schofield and Wroth uses a logarithmic spiral yield locus, and Roscoe and Burland introduced the ellipse used here.

## Hardening

The hardening function is defined as

$$
a=a_0\exp\left(\left(1+e_0\right)\dfrac{1-\alpha}{\lambda-\kappa\alpha}\right),
$$

where $$e_0$$ is the initial void ratio, $$\lambda$$ and $$\kappa$$ are material constants.

If experimental data is available, $$a_0$$ can be determined as

$$
a_0=\dfrac{1}{2}\exp\left(\dfrac{e_1-e_0-\kappa\ln{}p_0}{\lambda-\kappa}\right)
$$

where $$p_0$$ is the initial value of the equivalent pressure stress and $$e_1$$ is the intercept of the virgin consolidation line with the void ratio axis in a plot of void ratio versus equivalent pressure stress.

### Relation to the void ratio laws

The exponential form follows from integrating $de=-\lambda\,d(\ln p')$ along the virgin compression line and using the elastic swelling relation to eliminate the current void ratio.
In terms of the logarithmic volumetric plastic strain the source evaluates
$$
a(\alpha)=a_0\exp\left[(1+e_0)\frac{1-\alpha}{\lambda-\kappa\alpha}\right].
$$
Differentiating gives the closed-form derivative used by the local Newton iteration,
$$
\frac{\mathrm da}{\mathrm d\alpha}=a(\alpha)\frac{(1+e_0)(\kappa-\lambda)}{(\lambda-\kappa\alpha)^2}.
$$
The ABAQUS theory guide writes the same law in terms of $J^{\mathrm{pl}}=\exp(\varepsilon_v^{\mathrm{pl}})$ rather than the logarithmic strain itself.
Since suanPan substitutes $\alpha$ directly for $J^{\mathrm{pl}}$, the exponential factor at $\alpha=0$ is $\exp[(1+e_0)/\lambda]$ rather than one.
The argument `(7)` is therefore a scaling prefactor in this implementation, and the initial half-width is $a(0)=a_0\exp[(1+e_0)/\lambda]$.
The shipped example uses $a_0=0.02$, $e_0=0.889$, $\lambda=0.174$ and $\kappa=0.026$, which gives an initial half-width of about $10^3$ in the stress units of that model.

!!! info "deviation from theory"
    The hardening law substitutes the logarithmic volumetric plastic strain $\alpha$ where the reference formulation uses the plastic volume ratio $J^{\mathrm{pl}}=\exp(\varepsilon_v^{\mathrm{pl}})$.
    The value supplied as $a_0$ is not the initial yield-surface half-width unless it is reduced by $\exp[-(1+e_0)/\lambda]$.

## Syntax

```text title="ExpCC"
material ExpCC (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, beta, controls compression side shape
# (5) double, m, slope of CSL
# (6) double, p_t, initial tension strength
# (7) double, a_0, initial a_0
# (8) double, e_0, initial void ratio
# (9) double, lambda
# (10) double, kappa
# [11] double, density, default: 0.0
```

## Usage

* `(2)` and `(3)` define constant isotropic elasticity, `(4)` is $\beta$, `(5)` is $M$, and `(6)` is the tensile intercept $p_t$.
* `(8)` is the initial void ratio $e_0$, `(9)` is the compression index $\lambda$ and `(10)` is the recompression index $\kappa$, with $\lambda>\kappa>0$ and typically $\kappa/\lambda$ between 0.1 and 0.3.
* For $\beta=1$ and $p_t=0$ a desired initial preconsolidation pressure $p'_{c0}$ is obtained with $a_0=(p'_{c0}/2)\exp[-(1+e_0)/\lambda]$.
* The slope $M$ can be estimated from the triaxial compression friction angle as $M=6\sin\phi'/(3-\sin\phi')$.
* The parser takes absolute values of all nine material parameters, so negative input values cannot be used to encode softening or tension.
* The volumetric plastic strain is negative in compression, so $a$ increases as the soil is compressed and the yield surface expands.
* Use `set symm_mat 0` with this model because the consistent tangent returned by the return mapping is not generally symmetric.
* Use three-dimensional solid elements such as [C3D8](../../../../Element/Cube/C3D8.md), or the [`PlaneStrain`](../../../Wrapper/PlaneStrain.md) wrapper for a plane-strain analysis.

!!! warning "implementation limitation"
    The elastic part is constant isotropic elasticity rather than the stress-dependent porous elasticity of classical Cam-Clay, so the bulk modulus does not increase with compression and the swelling line is not reproduced by the elastic predictor.

## References

1. On the Generalised Stress-Strain Behaviour of 'Wet' Clay
2. [ISBN 978-0-641-94048-4](https://search.worldcat.org/search?q=bn:9780641940484)
3. [ISBN 978-0-521-33782-3](https://search.worldcat.org/search?q=bn:9780521337823)
4. [Critical state models](https://search.worldcat.org/search?q=ti:Critical+state+models)
