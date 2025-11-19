# Material2D

All 2D material models support the following basic output types.

| variable label | physical meaning                    |
| -------------- | ----------------------------------- |
| SP             | principal stress components         |
| EP             | principal strain components         |
| EEP            | principal elastic strain components |
| PEP            | principal plastic strain components |

Depending on the specific material model, additional output types may be available.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layout.
