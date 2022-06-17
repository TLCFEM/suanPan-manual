# Material1D

All uniaxial material models support the following basic output types.

| variable label | physical meaning |
|----------------|------------------|
| S, S11         | uniaxial stress  |
| E, E11         | uniaxial strain  |
| EE             | elastic strain   |
| PE             | plastic strain   |
| HIST           | history vector   |

Depending on the specific material model, additional output types may be available.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layout.
