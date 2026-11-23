# DafaliasManzari

The modified Dafalias--Manzari sand model.

The original model [10.1061/(ASCE)0733-9399(2004)130:6(622)](https://doi.org/10.1061/(ASCE)0733-9399(2004)130:6(622)) is modified slightly.
Readers can also refer to the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf) for details on the theory.

The modifications can be summarised as follows.

1. The continuum mechanics convention (tension positive) is used.
   All volumetric strain and hydrostatic stress related quantities shall flip their signs.
2. The Lode angle dependency is removed, which is equivalent to setting $$c=1$$ in Eq. (19).
3. Constants such as $$2/3$$ and $$\sqrt{2/3}$$ are removed.
   They can be combined with the model parameters.
4. The hardening related parameter $$h$$ as defined in Eq. (24) causes numerical issues under small cyclic loads.
   Hence, it is changed to a similar form.

!!! info "deviation from theory"
    The published model uses a compression-positive convention and a Lode-angle function $$g(\theta,c)$$ with $$c$$ the ratio of the critical stress ratio in extension to that in compression.
    This implementation uses the tension-positive convention, drops the Lode-angle dependence (equivalent to $$c=1$$), and absorbs the factors $$2/3$$ and $$\sqrt{2/3}$$ into the input parameters.
    The hardening modulus is modified to an exponential form to avoid the singularity of the published $$1/[(\mathbf\alpha-\mathbf\alpha_{in}):\mathbf n]$$ expression under small load reversals.

**The algorithm is correct but the theory needs validation.**
**Your collaboration would be much appreciated.**

## Syntax

```text title="DafaliasManzari"
material DafaliasManzari (1) (2-18) [19]
# (1) int, unique material tag
# (2) double, reference shear modulus G_0 ==> 125
# (3) double, Poisson's ratio \nu
# (4) double, \alpha^c ==> 1.5
# (5) double, slope of critical state line \lambda_c ==> 0.02
# (6) double, initial void ratio e_0
# (7) double, exponent \xi ==> 0.7
# (8) double, initial yield surface size m ==> 0.01
# (9) double, hardening constant h_0
# (10) double, hardening constant h_1 ==> 0.1
# (11) double, hardening constant c_h ==> 0.9
# (12) double, n^b ==> 1.1
# (13) double, dilatancy constant A_0 ==> -0.7
# (14) double, n^d ==> 3.5
# (15) double, z_{max} ==> 4
# (16) double, c_z ==> 600
# (17) double, atmospheric pressure p_{at} ==> -130
# (18) double, threshold G_r ==> 0.1
# [19] double, density, default: 0.0
```

## Theory

### Hyperelasticity

The hyperelastic response is defined as

$$
G=G_0\dfrac{\left(2.97-e\right)^2}{1+e}\sqrt{pp_{at}},\qquad K=\dfrac{2}{3}\dfrac{1+\nu}{1-2\nu}G.
$$

To improve numerical stability, $$G$$ is bounded by $$G_rG_0|p_{at}|$$ where $$G_r$$ is a constant that can be chosen as for example $$0.1$$.
This is equivalent to defining an elastic response for $$|p|<0.01|p_{at}|$$.

The void ratio can be associated with strain so that

$$
e=e_0+\left(1+e_0\right)\mathrm{tr~}{\varepsilon^{tr}}.
$$

The strain increment can be decomposed into elastic and plastic parts.

$$
\mathbf{\varepsilon}^{tr}=\mathbf{\varepsilon}_n+\Delta\mathbf{\varepsilon}=\mathbf{\varepsilon}_
n+\Delta\mathbf{\varepsilon}^{e}+\Delta\mathbf{\varepsilon}^{p}.
$$

As such, the stress increment can be expressed accordingly,

$$
\mathbf{\sigma}=\mathbf{\sigma}_n+\Delta\mathbf{\sigma}=\mathbf{\sigma}_n+2G\left(
\Delta{}\mathbf{e}-\Delta{}\mathbf{e}^{p}\right)+K\left(\Delta\varepsilon_v-\Delta\varepsilon_v^p\right)\mathbf{I}.
$$

In deviatoric and spherical components,

$$
\mathbf{\sigma}=\mathbf{s}+p\mathbf{I},\\ p=p_n+K\left(\Delta\varepsilon_v-\Delta\varepsilon_v^p\right),\\
\mathbf{s}=\mathbf{s}_n+2G\left(\Delta{}\mathbf{e}-\Delta{}\mathbf{e}^{p}\right),
$$

with

$$
\Delta\mathbf{\varepsilon}=\Delta{}\mathbf{e}+\dfrac{1}{3}\Delta\varepsilon_v\mathbf{I},
$$

where $$\mathbf{s}=\mathrm{dev~}{\mathbf{\sigma}}$$ is the deviatoric stress, $$p=\dfrac{1}{3}\mathrm{tr~}{\mathbf{\sigma}}$$ is the hydrostatic stress.

### Critical State

The critical state parameter is chosen as

$$
\psi=e-e_0+\lambda_c\left(\dfrac{p}{p_{at}}\right)^\xi.
$$

The dilatancy surface is defined as

$$
\alpha^d=\alpha^c\exp\left(n^d\psi\right).
$$

The bounding surface is defined as

$$
\alpha^b=\alpha^c\exp\left(-n^b\psi\right).
$$

### Yield Function

A wedge-like function is chosen to be the yield surface.

$$
F=\big|\mathbf{s}+p\mathbf{\alpha}\big|+mp=\big|\mathbf{\eta}\big|+mp,
$$

where $$\alpha$$ is the so-called back stress ratio and $$m$$ characterises the size of the wedge.
For simplicity, $$m$$ is assumed to be a constant in this model.

By denoting $$\mathbf{\eta}=\mathbf{s}+p\mathbf{\alpha}$$, the directional unit tensor is defined as

$$
\mathbf{n}=\dfrac{\mathbf{\eta}}{\big|\mathbf{\eta}\big|}.
$$

### Flow Rule

A non-associated plastic flow is used; the corresponding flow rule is defined as follows.

$$
\Delta\mathbf{\varepsilon}^p=\gamma\left(\mathbf{n}+\dfrac{1}{3}D\mathbf{I}\right),
$$

where $$D$$ is the dilatancy parameter.

$$
D=A_d\left(\alpha^d-m-\mathbf{\alpha}:\mathbf{n}\right)=A_0\left(1+\left\langle\mathbf{z}:
\mathbf{n}\right\rangle\right)\left(\alpha_d-m-\mathbf{\alpha}:\mathbf{n}\right).
$$

Due to the change of sign convention, a negative $$D$$ gives contractive response, thus $$A_0$$ often needs to be negative.

### Hardening Rule

The evolution rate of the back stress ratio $$\mathbf{\alpha}$$ is defined in terms of a proper distance measure from the bounding surface,

$$
\Delta\mathbf{\alpha}=\gamma{}h\left(\left(\alpha^b-m\right)\mathbf{n}-\mathbf{\alpha}\right),
$$

where $$h$$ controls the hardening rate,

$$
h=b_0\exp\left(h_1\left(\mathbf{\alpha}_{in}-\mathbf{\alpha}\right):\mathbf{n}\right).
$$

The parameter $$b_0$$ is defined as a function of current state,

$$
b_0=G_0h_0\left(1-c_he\right)\sqrt{\dfrac{p_{at}}{p}}.
$$

$$\mathbf{\alpha}_{in}$$ is updated whenever load reversal occurs.

### Fabric Effect

The fabric tensor changes when $$\Delta\varepsilon^p_v$$ is positive,

$$
\Delta\mathbf{z}=c_z\left\langle\Delta\varepsilon^p_v\right\rangle\left(z_m\mathbf{n}-\mathbf{z}\right).
$$

!!! info "deviation from theory"
    With the tension-positive convention the source evaluates this increment as $$\Delta\mathbf z=c_z\gamma D\left(z_m\mathbf n-\mathbf z\right)$$ for positive dilatancy $$D$$, since $$\Delta\varepsilon^p_v=\gamma D$$.
    This is the sign-reversed counterpart of the compression-positive expression published by Dafalias and Manzari.

### Parameter summary

- $G_0$ and $\nu$ set the small-strain elastic stiffness through $G=G_0(2.97-e)^2/(1+e)\sqrt{|pp_{at}|}$ and $K=2(1+\nu)G/[3(1-2\nu)]$.
- $\alpha^c$ is the critical-state stress ratio, $\lambda_c$ and $\xi$ define the critical-state line, and $e_0$ is the initial void ratio.
- $m$ is the small yield-surface size in stress-ratio space, $h_0$, $h_1$ and $c_h$ control the hardening rate, and $n^b$ and $n^d$ set the distances to the bounding and dilatancy surfaces.
- $A_0$ is the dilatancy constant and is normally negative in this sign convention, $n^d$ controls its state dependence, and $z_{max}$ and $c_z$ control the fabric contribution.
- $p_{at}$ is the atmospheric pressure used for normalisation and is entered as a negative number, and $G_r$ is the fraction of $G_0|p_{at}|$ used as the lower bound on the shear modulus.

!!! warning "implementation limitation"
    A tensile or near-zero trial pressure makes the yield surface undefined, so the implementation caps the response at zero mean stress and returns a deviatoric-only stress with the floor shear modulus $$G_rG_0|p_{at}|$$.
    No tensile strength or cap surface is available for sand in this model.

## Remarks

- The parser defaults are $G_0=125$, $\nu=0.05$, $\alpha^c=1.25$, $\lambda_c=0.02$, $e_0=0.9$, $\xi=0.7$, $m=0.01$, $h_0=7$, $h_1=0.1$, $c_h=0.9$, $n^b=1.1$, $A_0=-0.7$, $n^d=3.5$, $z_{max}=4$, $c_z=600$, $p_{at}=-130$ and $G_r=0.2$.
- Most input arguments are converted to absolute values in the constructor; only the dilatancy constant $A_0$ keeps its sign and $p_{at}$ is forced negative.
- The parameter set was calibrated for Toyoura sand and is often reused for other sands, with $m$, $h_0$, $c_h$, $n^b$ and $n^d$ commonly treated as constants.
- The Lode-angle dependence of the original model is absent, so true triaxial stress states are approximated by a circular deviatoric section.
- The state parameter is computed from the void ratio obtained from the trace of the total strain, so large strains or large volumetric errors directly affect the dilatancy and bounding surfaces.
- For a simpler bounding-surface sand model without fabric effects use [`SimpleSand`](SimpleSand.md).

!!! warning "implementation limitation"
    The values annotated with `==>` in the syntax block are illustrative and are not the parser defaults.
    In particular the constructor uses $$\alpha^c=1.25$$ rather than $$1.5$$ and $$G_r=0.2$$ rather than $$0.1$$.

## References

1. Dafalias, Y. F. and Manzari, M. T. (2004) Simple plasticity sand model accounting for fabric change effects, Journal of Engineering Mechanics, 130(6), 622--634, [10.1061/(ASCE)0733-9399(2004)130:6(622)](https://doi.org/10.1061/(ASCE)0733-9399(2004)130:6(622)).
2. Manzari, M. T. and Dafalias, Y. F. (1997) A two-surface plasticity model for sand, Geotechnique, 47(2), 255--272.
