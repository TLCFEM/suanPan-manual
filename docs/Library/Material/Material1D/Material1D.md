# Material1D

In additional to the default output types supported by all materials, all uniaxial material models support the following basic output types.

| variable label | physical meaning         |
| -------------- | ------------------------ |
| SP             | principle stress         |
| EP             | principle strain         |
| EEP            | principle elastic stress |
| PEP            | principle plastic strain |

All principle values are identical to the normal ones for uniaxial material models.

Depending on the specific material model, additional output types may be available.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layout.
