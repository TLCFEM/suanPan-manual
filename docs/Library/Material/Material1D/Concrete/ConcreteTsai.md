# ConcreteTsai

Uniaxial Concrete Model Using Tsai's Equation

The `ConcreteTsai` model is a simple concrete model using Tsai's equation.

## Syntax

Depending on the number of parameters provided (8 to 11), the model can be defined in two ways.

```
material ConcreteTsai (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, compression strength, should be negative but sign insensitive
# (3) double, tension strength, should be positive but sign insensitive
# (4) double, MC
# (5) double, NC
# (6) double, MT
# (7) double, NT
# (8) double, middle point, typical: 0.2
# (9) double, strain at compression strength, typical: -2E-3
# (10) double, strain at tension strength, typical: 1E-4
# [11] double, density, default: 0.0
```

```
material ConcreteTsai (1) (2) (3) (4) (5) [6] [7] [8] [9]
# (1) int, unique material tag
# (2) double, compression strength, should be negative but sign insensitive
# (3) double, tension strength, should be positive but sign insensitive
# (4) double, M
# (5) double, N
# (6) double, middle point, typical: 0.2
# (7) double, strain at compression strength sign insensitive, typical: -2E-3
# (8) double, strain at tension strength sign insensitive, typical: 1E-4
# [9] double, density, default: 0.0
```

## History Variable Layout

Since it is derived from the [`SimpleHysteresis`](../Hysteresis/SimpleHysteresis.md) model, they share the same history
variable layout.

## Remarks

1. The middle point parameter represents the size of hysteresis loop, valid values range from 0 to 1 (ends not
   recommended).
2. There is no additional consideration for small loops, which is available in [`ConcreteCM`](ConcreteCM.md).

## Usage

```
material ConcreteTsai 1 30 20 2 2 2 2 .8 2E-3 2E-3
materialTest1D 1 1E-4 50 100 120 140 160 180
exit
```

![example one](ConcreteTsai.EX1.svg)

```
material ConcreteTsai 1 30 20 2 2 2 2 .1 2E-3 2E-3
materialTest1D 1 1E-4 50 100 120 140 160 180
exit
```

![example two](ConcreteTsai.EX2.svg)
