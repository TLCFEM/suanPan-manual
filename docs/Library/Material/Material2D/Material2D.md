# Material2D

All 2D material models support the following basic output types.

| variable label | physical meaning                              |
|----------------|-----------------------------------------------|
| S11            | $$\sigma_{11}$$                               |
| S12            | $$\sigma_{12}$$                               |
| S22            | $$\sigma_{22}$$                               |
| E11            | $$\varepsilon_{11}$$                          |
| E12            | $$\varepsilon_{12}$$                          |
| E22            | $$\varepsilon_{22}$$                          |
| SP             | all principal stress components               |
| EP             | all principal strain components               |

Depending on the specific material model, additional output types may be available.

The history vector is a vector of variadic length that stores the necessary history variables for the material model.
Different material models may have different history variable storage layout.
