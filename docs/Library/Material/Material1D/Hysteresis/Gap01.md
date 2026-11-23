# Gap01

Uniaxial gap material with no compressive resistance and bilinear elastic-perfectly plastic response in tension.

## Syntax

```text title="Gap01"
material Gap01 (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield stress
# [4] double, gap strain, default: 0.0
# [5] double, density, default: 0.0
```

## Background

The material carries no stress in compression and yields at a fixed tensile stress.
On reloading from zero stress, the strain must first close the gap before tensile stress develops.
The `gap strain` `(4)` is the strain offset measured from the stress-free reference to the point where tension starts.

When the gap is closed the stress obeys

$$
\sigma=E\left(\varepsilon-\varepsilon_g-\varepsilon_r\right),\qquad 0\le\sigma\le\sigma_y,
$$

where $$E$$ is the elastic modulus, $$\sigma_y$$ the yield stress, $$\varepsilon_g$$ the gap strain and $$\varepsilon_r$$ a residual strain accumulated during previous unloading.
On unloading the residual strain is updated from the elastic intercept, $$\varepsilon_r=\varepsilon-\sigma/E-\varepsilon_g$$, so reloading from zero stress must first close the remaining gap.
The tangent modulus equals $$E$$ in the active elastic branch and zero in both the zero-stress and the yielded states.
No compression is transmitted, so the stress is clamped at zero for any negative trial value.

!!! info "deviation from theory"
    The yield cap is applied by clamping the trial stress rather than by a plastic return algorithm, so the tangent jumps directly from $$E$$ to zero at the yield stress.
    The gap offset is introduced through a stored residual strain that is updated only while unloading from a stressed state.

!!! warning "implementation limitation"
    The code detects a closed gap by comparing the current stress with zero exactly.
    Small floating-point residuals can therefore delay the re-activation of tensile stiffness.

## Remarks

The modulus, yield stress and gap strain are all converted to absolute values, so their signs do not matter.
The stress is clamped to zero in compression and to the yield stress in tension, and the tangent stiffness is zero in both clamped states.
A `gap strain` of zero, the default, gives an ordinary elastic-perfectly plastic tensile model without a gap.
The response is path dependent through the residual strain and the sign of the strain increment, even though the individual branches are simple.
The yield stress acts as a tension cap with zero tangent, so the model does not harden after yielding.
A typical application is a gap or contact in a bracing or connection assembly, modelled with a one-dimensional truss or beam element.
Calibrate $$E$$, $$\sigma_y$$ and $$\varepsilon_g$$ with `materialTest1D` before using the material in a structural model.
