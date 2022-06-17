# Material3D

All 3D material models support the following basic output types.

| variable label | physical meaning                |
|----------------|---------------------------------|
| S              | all stress components           |
| S11            | $$\sigma_{11}$$                 |
| S12            | $$\sigma_{12}$$                 |
| S13            | $$\sigma_{13}$$                 |
| S22            | $$\sigma_{22}$$                 |
| S23            | $$\sigma_{23}$$                 |
| S33            | $$\sigma_{33}$$                 |
| E              | all strain components           |
| E11            | $$\varepsilon_{11}$$            |
| E12            | $$\varepsilon_{12}$$            |
| E13            | $$\varepsilon_{13}$$            |
| E22            | $$\varepsilon_{22}$$            |
| E23            | $$\varepsilon_{23}$$            |
| E33            | $$\varepsilon_{33}$$            |
| SP             | all principal stress components |
| SP1            | principal stress component 1    |
| SP2            | principal stress component 2    |
| SP3            | principal stress component 3    |
| EP             | all principal strain components |
| EP1            | principal strain component 1    |
| EP2            | principal strain component 2    |
| EP3            | principal strain component 3    |
| EE             | elastic strain                  |
| PE             | plastic strain                  |
| EEP            | principal elastic strain        |
| PEP            | principal plastic strain        |
| PEEP           | equivalent plastic strain       |
| HYDRO          | hydrostatic stress              |
| HIST           | history variable vector         |

Depending on the specific material model, additional output types may be available.
