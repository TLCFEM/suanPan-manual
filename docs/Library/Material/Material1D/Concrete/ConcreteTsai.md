# ConcreteTsai

Uniaxial Concrete Model Using Tsai's Equation

The `ConcreteTsai` model is a simple concrete model using Tsai's equation.

## References

1. [10.1061/(ASCE)0733-9445(1988)114:9(2133)](https://doi.org/10.1061/(ASCE)0733-9445(1988)114:9(2133))

The backbone is governed by a normalized function which is controlled by two parameters $$m$$ and $$n$$.

<iframe src="https://www.desmos.com/calculator/l5lebk1toq?embed" width="800" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

## Syntax

```
material ConcreteTsai (1) (2) (3) (4) (5) (6) (7) (8) (9) [10]
# (1) int, unique material tag
# (2) double, elastic modulus, E
# (3) double, compression strength, should be negative but sign insensitive, f_c
# (4) double, tension strength, should be positive but sign insensitive, f_t
# (5) double, NC
# (6) double, NT
# (7) double, middle point, typical: 0.2
# (8) double, strain at compression strength, \varepsilon_c, typical: -2E-3
# (9) double, strain at tension strength, \varepsilon_t, typical: 1E-4
# [10] double, density, default: 0.0
```

## History Variable Layout

Since it is derived from the [`SimpleHysteresis`](../Hysteresis/SimpleHysteresis.md) model, they share the same history
variable layout.

## Remarks

1. The middle point parameter represents the size of hysteresis loop, valid values range from 0 to 1 (ends not
   recommended).
2. There is no additional consideration for small loops, which is available in [`ConcreteCM`](ConcreteCM.md).

The parameter $$m$$ defined in the reference.
But it is not explicitly exposed in order to eliminate inconsistent elastic modulus in compression and tension.
It is, instead, computed internally based on the given strains at compression and tension strength.

Note the magnitude of the strain at compression/tension strength has to be greater than the 'elastic strain' computed by the corresponding strength divided by the elastic modulus.

$$
|\varepsilon_c|>\dfrac{|f_c|}{E},\\
|\varepsilon_t|>\dfrac{|f_t|}{E}.
$$

This ensures the corresponding parameter $$m$$ is always greater than 1, which is required by the model.

## Usage

```
material ConcreteTsai 1 3E4 30 20 2 2 .8 2E-3 2E-3
materialTest1D 1 1E-4 50 100 120 140 160 180
exit
```

![example one](ConcreteTsai.EX1.svg)

```
material ConcreteTsai 1 3E4 30 20 2 2 .1 2E-3 2E-3
materialTest1D 1 1E-4 50 100 120 140 160 180
exit
```

![example two](ConcreteTsai.EX2.svg)
