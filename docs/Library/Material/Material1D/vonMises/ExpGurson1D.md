# ExpGurson1D

Extended Gurson Void Growth Model

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

## Theory

The yield function, the associated flow rule and the damage evolution are those of [`NonlinearGurson1D`](NonlinearGurson1D.md).
This model only specifies the matrix hardening law.

The normalised matrix yield stress $$k=\sigma_y/\sigma_{y0}$$ is obtained from the implicit relation

$$
k=\left(k+\dfrac{3G}{\sigma_{y0}}\varepsilon_m^p\right)^n,
$$

where $$G=E/[2(1+\nu)]$$ is the shear modulus and $$\varepsilon_m^p$$ is the matrix equivalent plastic strain.
The exponent $$n$$ is clamped to at most unity in the constructor.
Solving this relation by Newton iteration gives the derivative required by the return mapping,

$$
\dfrac{\mathrm{d}\sigma_y}{\mathrm{d}\varepsilon_m^p}=\sigma_{y0}\,\dfrac{m\,c}{1-m},\qquad c=\dfrac{3G}{\sigma_{y0}},\qquad m=n\left(k+c\varepsilon_m^p\right)^{n-1}.
$$

At zero plastic strain $$k=1$$, so the initial matrix yield stress equals the input parameter $$\sigma_{y0}$$.

!!! warning "implementation limitation"
    The implicit relation $k=(k+c\varepsilon_m^p)^n$ is not the usual explicit power-law hardening form.
    It is solved locally by Newton iteration with a cap of 20 iterations.
    If the iteration fails, the code prints an error and falls back to $k=1$ with the derivative evaluated as $nc/(1-n)$.
    At $n=1$ that derivative is singular.

## Syntax

```text title="ExpGurson1D"
material ExpGurson1D (1) (2) (3) (4) (5) [6] [7] [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, yield stress
# (5) double, n
# [6] double, q1, default: 1.0
# [7] double, q2, default: 1.0
# [8] double, fn, default: 0.0
# [9] double, sn, default: 1.0
# [10] double, en, default: 0.0
# [11] double, density, default: 0.0
```

## Remarks

All numerical inputs are optional and default to $$E=200$$, $$\nu=0.3$$, $$\sigma_y=0.4$$, $$n=0.2$$, $$q_1=1$$, $$q_2=1$$, $$f_N=0$$, $$s_N=1$$, $$\varepsilon_N=0$$ and zero density.
The exponent should satisfy $$0<n<1$$; values above unity are clamped to one, where the derivative above becomes singular.
The parameters $$q_1$$, $$q_2$$, $$f_N$$, $$s_N$$ and $$\varepsilon_N$$ have the same meaning as in [`NonlinearGurson1D`](NonlinearGurson1D.md).
A nonzero initial void fraction can be set with the [`initial`](../../../../Collection/Define/initial.md) `material history` command.
The void fraction can be recorded with the `VF` output type.
For an arbitrary user-defined matrix hardening law use [`CustomGurson1D`](CustomGurson1D.md).

## References

1. A. L. Gurson, Continuum theory of ductile rupture by void nucleation and growth, Part I: yield criteria and flow rules for porous ductile media, *Journal of Engineering Materials and Technology* 99 (1977) 2--15, [doi:10.1115/1.3443401](https://doi.org/10.1115/1.3443401).
2. V. Tvergaard and A. Needleman, Analysis of the cup-cone fracture in a round tensile bar, *Acta Metallurgica* 32 (1984) 157--169, [doi:10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X).
