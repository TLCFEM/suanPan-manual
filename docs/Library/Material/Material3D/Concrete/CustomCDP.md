# CustomCDP

The CDP Model With Custom Backbones

The formulation is identical to that of the `CDP` model.

User should provide the backbones and damage evolutions via expressions.

## Syntax

```text
material CustomCDP (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11]
# (1) int, unique material tag
# (2) int, tension expression tag
# (3) int, compression expression tag
# (4) double, elastic modulus
# (5) double, poisson's ratio
# (6) double, normalized crack energy (+)
# (7) double, normalized crush energy (+)
# [8] double, dilatancy parameter, default: 0.2
# [9] double, biaxial compression strength ratio, default: 1.16
# [10] double, stiffness recovery ratio, default: 0.5
# [11] double, density, default: 0
```

## Restrictions

1. The expressions should take one input argument, the damage variable, $$\kappa$$.
   The $$\kappa$$ is different from the degradation denoted as $$d$$.
   The output should have a size of six.
2. The normalized energy should be provided, which is used to generate objective results.
   It is typically around the size of the area under the curve.
3. The output consists of six components, which are explained in the following.

The expression shall generate six numbers based on the input $$\kappa$$:

1. $$d$$: the damage degradation index
2. $$f$$: the final stress: $$(1-d)\bar{f}$$
3. $$\bar{f}$$: the effective stress $$f/(1-d)$$
4. $$\mathrm{d}~d$$: derivative of $$d$$
5. $$\mathrm{d}~f$$: derivative of $$f$$
6. $$\mathrm{d}~\bar{f}$$: derivative of $$\bar{f}$$

The $$\kappa$$ ranges from 0 to 1.

The damage degradation index $$d$$ shall satisfy: $$d(0)=0$$ and $$d(1)=1$$.

The $$f$$ is the actual stress observed as the final output of the model.

By following these rules imposed, users can implement any custom backbone and damage evolution.

Further explanation of the curves can be seen in
[10.1061/(ASCE)0733-9399(1998)124:8(892)](https://doi.org/10.1061/(ASCE)0733-9399(1998)124:8(892))
