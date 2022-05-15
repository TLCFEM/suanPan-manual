# Mises1D

Uniaxial General Model Using von Mises Criterion

This is an abstract class that shall be overridden.

The `Mises1D` is a general model using von Mises yielding criterion and associated flow rule. The hardening rules can be
customized.

## Theory

### Yield Function

A von Mises type yield function is used.

$$
F=|\sigma-\beta|-k
$$

### Flow Rule

The associated plasticity is assumed.

$$
\mathrm{d}\varepsilon^p=\gamma\dfrac{\partial{}F}{\partial\sigma}=\text{sign}(\sigma-\beta)~\gamma
$$

### Hardening

Both isotropic and kinematic hardening rules are employed.

#### Isotropic Hardening

A general function of accumulated plastic strain $$p$$ needs to be defined.

$$
k=k(p),
$$

where $$p=\displaystyle\int|\mathrm{d}\varepsilon^p|~\mathrm{d}t$$ is the accumulated plastic strain.

#### Kinematic Hardening

A general function of accumulated plastic strain $$p$$ needs to be defined.

$$
\beta=h(p).
$$

## Implementation

The function $$k(p)$$ and $$h(p)$$ need to be defined in the derived classes.
