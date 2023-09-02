# Degradation

The uniaxial degradation model can be implemented separately from the intact material model if the degradation model
only depends on the input strain history or the output stress and stiffness.

## Stress

The general expression of a degradation model can be expressed as

$$
\sigma=D\bar{\sigma}=(1-d)\bar{\sigma},
$$

where $$D$$ and $$d$$ are degradation factors, $$\bar\sigma$$ is the stress of the intact material model.
It is often called the effective stress.
Whether to use $$D$$ or $$(1-d)$$ relies on the specific definition of degradation.
Here we focus on the first expression.

## Stiffness

The stiffness can be expressed by applying the chain rule.

### Strain Dependent Degradation

Assuming the degradation factor depends on the strain history, namely, $$D=D(\varepsilon_{max})$$.
In which $$\varepsilon_{max}$$ is the maximum strain of the whole loading history.

Where damage evolution is activated, the stiffness can be expressed as

$$
K=\dfrac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}=\dfrac{\partial{}D}{\partial\varepsilon}\bar\sigma+D\dfrac{\partial\bar\sigma}{\partial\varepsilon}=\dfrac{\partial{}D}{\partial\varepsilon}\bar\sigma+D\bar{K}
$$

where $$\bar{K}$$ is the effective stiffness of the intact material model.

### Stress Depedent Degradation

Assuming the degradation factor depends on the strain history, namely, $$D=D(\bar{\sigma}_{max})$$.
In which $$\bar{\sigma}_{max}$$ is the maximum effective stress of the whole loading history.

Where damage evolution is activated, the stiffness can be expressed as

$$
K
=\dfrac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}
=\dfrac{\partial{}D}{\partial\bar{\sigma}}\dfrac{\partial\bar\sigma}{\partial\varepsilon}\bar{\sigma}+D\dfrac{\partial\bar\sigma}{\partial\varepsilon}
=\left(\dfrac{\partial{}D}{\partial\bar{\sigma}}\bar{\sigma}+D\right)\bar{K}
$$

where $$\bar{K}$$ is the effective stiffness of the intact material model.

## Computation Procedure

In general, the computation procedure of a degradation model can be listed as follows.

1. input trial strain and trial strain rate if required
2. call the associated intact material model to compute the intact stress and stiffness
3. calculate $$D$$ and $$\dfrac{\partial{}D}{\partial{}\varepsilon}$$ accordingly and update history variables if any
4. update trial stress and trial stiffness

## Caveats

Such a formulation is only valid for the damage models that do not depend on plasticity history.
