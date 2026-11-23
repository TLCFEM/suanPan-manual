# ParabolicCC

Parabolic Hardening Modified Cam-Clay Model

## Background

`ParabolicCC` shares the yield surface, flow rule and integration algorithm of [`NonlinearCamClay`](NonlinearCamClay.md) and differs only in the hardening law.
The parabolic law depends on the square of the volumetric plastic strain and is therefore symmetric in compression and dilation, which is a mathematical convenience rather than a representation of soil physics.

## Theory

This model defines a parabolic hardening rule for $$a(\alpha)$$, which is a non-negative function.

$$
a(\alpha)=a_0+H\alpha^2\ge0,
$$

in which $$H$$ is the hardening modulus; note that $$\alpha=\varepsilon_p=\varepsilon_1+\varepsilon_2+\varepsilon_3$$ is the volumetric plastic strain.

The hardening modulus could be either positive or negative.

**This hardening rule does not imply any physical soil behavior.**

### Implementation of the hardening law

The source evaluates $$a(\alpha)=a_0+H\alpha^2$$ with derivative $$\mathrm da/\mathrm d\alpha=2H\alpha$$.
For a negative hardening modulus the function is clamped to zero, together with its derivative, once $$|\alpha|>\sqrt{a_0/|H|}$$.
The clamp prevents the quadratic term from driving $$a$$ negative and inverting the yield surface.
For a positive hardening modulus there is no clamp, so $$a$$ grows without bound as volumetric plastic strain accumulates.

!!! info "deviation from theory"
    The quadratic law is symmetric in $$\alpha$$, so it hardens or softens in the same way under compression and dilation.
    Real soils harden under compaction and soften under dilation, which cannot be represented by this single even function.

## Syntax

```text title="ParabolicCC"
material ParabolicCC (1) (2) (3) (4) (5) (6) (7) (8) [9]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, beta, controls compression side shape
# (5) double, m, slope of CSL
# (6) double, p_t, initial tension strength
# (7) double, a_0, initial a_0
# (8) double, H, slope of hardening function
# [9] double, density, default: 0.0
```

## Remarks

* The first six arguments are the elastic modulus, Poisson's ratio, $$\beta$$, $$M$$, $$p_t$$ and $$a_0$$ as defined on the [`NonlinearCamClay`](NonlinearCamClay.md) page.
* The slope $$H$$ has units of stress per unit volumetric strain squared, and $$a_0$$ has units of stress.
* Because the law depends on $$\alpha^2$$, it grows for both compression and dilation when $$H>0$$, which is not the behaviour of a real soil.
* A negative $$H$$ produces softening followed by a complete loss of the yield surface once the strain magnitude exceeds $$\sqrt{a_0/|H|}$$.
* Use `set symm_mat 0` because the consistent tangent is not generally symmetric.
* For a hardening law derived from the void ratio and the compression and recompression indices, use [`ExpCC`](ExpCC.md).

## References

1. On the Generalised Stress-Strain Behaviour of 'Wet' Clay
2. [ISBN 978-0-641-94048-4](https://search.worldcat.org/search?q=bn:9780641940484)
3. [ISBN 978-1-932159-75-2](https://search.worldcat.org/search?q=bn:9781932159752)
