# Output Type

Currently, the available types of output variables are listed as follows.

Please note, in principle, it is possible to define any types on any recorders, but if the target recorder does not 
support the type, trivial/empty values will be returned. If saving recorder does not create any files on the disk, 
meaning that the output type is not available for the target object. For example, recording strain/stress `E`/`S` 
values of any nodes is not possible and will lead to no output.

The complete support list is still under development. In principle, basic types such as 
displacement/velocity/acceleration are available for nodes. For elemental response, generally stress/strain and 
their components are available. Certain elements only support some output types. Please feel free to open 
an issue if you need more information.

## General Node Quantities

| variable label | physical meaning                     |
|----------------|--------------------------------------|
| U              | all displacement components          |
| U1             | displacement along DoF 1             |
| U2             | displacement along DoF 2             |
| U3             | displacement along DoF 3             |
| U4             | displacement along DoF 4             |
| U5             | displacement along DoF 5             |
| U6             | displacement along DoF 6             |
| UR1            | rotational displacement along DoF 1  |
| UR2            | rotational displacement along DoF 2  |
| UR3            | rotational displacement along DoF 3  |
| V              | all velocity components              |
| V1             | velocity along DoF 1                 |
| V2             | velocity along DoF 2                 |
| V3             | velocity along DoF 3                 |
| V4             | velocity along DoF 4                 |
| V5             | velocity along DoF 5                 |
| V6             | velocity along DoF 6                 |
| VR1            | angular velocity along DoF 1         |
| VR2            | angular velocity along DoF 2         |
| VR3            | angular velocity along DoF 3         |
| A              | all acceleration components          |
| A1             | acceleration along DoF 1             |
| A2             | acceleration along DoF 2             |
| A3             | acceleration along DoF 3             |
| A4             | acceleration along DoF 4             |
| A5             | acceleration along DoF 5             |
| A6             | acceleration along DoF 6             |
| AR1            | rotation acceleration along DoF 1    |
| AR2            | rotation acceleration along DoF 2    |
| AR3            | rotation acceleration along DoF 3    |
| MM             | momentum                             |
| MM1            | nodal/global momentum component 1    |
| MM2            | nodal/global momentum component 2    |
| MM3            | nodal/global momentum component 3    |
| MM4            | nodal/global momentum component 4    |
| MM5            | nodal/global momentum component 5    |
| MM6            | nodal/global momentum component 6    |
| MMR1           | nodal/global momentum component 4    |
| MMR2           | nodal/global momentum component 5    |
| MMR3           | nodal/global momentum component 6    |
| RF             | all reaction force components        |
| RF1            | reaction force along DoF 1           |
| RF2            | reaction force along DoF 2           |
| RF3            | reaction force along DoF 3           |
| RF4            | reaction force along DoF 4           |
| RF5            | reaction force along DoF 5           |
| RF6            | reaction force along DoF 6           |
| RM1            | reaction moment along DoF 1          |
| RM2            | reaction moment along DoF 2          |
| RM3            | reaction moment along DoF 3          |
| DF             | all nodal damping force components   |
| DF1            | damping force along DoF 1            |
| DF2            | damping force along DoF 2            |
| DF3            | damping force along DoF 3            |
| DF4            | damping force along DoF 4            |
| DF5            | damping force along DoF 5            |
| DF6            | damping force along DoF 6            |
| DM1            | damping force along DoF 4            |
| DM2            | damping force along DoF 5            |
| DM3            | damping force along DoF 6            |
| IF             | all nodal inertial force components  |
| IF1            | inertial force along DoF 1           |
| IF2            | inertial force along DoF 2           |
| IF3            | inertial force along DoF 3           |
| IF4            | inertial force along DoF 4           |
| IF5            | inertial force along DoF 5           |
| IF6            | inertial force along DoF 6           |
| IM1            | inertial force along DoF 4           |
| IM2            | inertial force along DoF 5           |
| IM3            | inertial force along DoF 6           |
| GDF            | all global damping force components  |
| GDF1           | global damping force along DoF 1     |
| GDF2           | global damping force along DoF 2     |
| GDF3           | global damping force along DoF 3     |
| GDF4           | global damping force along DoF 4     |
| GDF5           | global damping force along DoF 5     |
| GDF6           | global damping force along DoF 6     |
| GDM1           | global damping force along DoF 4     |
| GDM2           | global damping force along DoF 5     |
| GDM3           | global damping force along DoF 6     |
| GIF            | all global inertial force components |
| GIF1           | global inertial force along DoF 1    |
| GIF2           | global inertial force along DoF 2    |
| GIF3           | global inertial force along DoF 3    |
| GIF4           | global inertial force along DoF 4    |
| GIF5           | global inertial force along DoF 5    |
| GIF6           | global inertial force along DoF 6    |
| GIM1           | global inertial force along DoF 4    |
| GIM2           | global inertial force along DoF 5    |
| GIM3           | global inertial force along DoF 6    |

## General Element Quantities

| variable label | physical meaning                              |
|----------------|-----------------------------------------------|
| S              | all stress components                         |
| S11            | $$\sigma_{11}$$                               |
| S12            | $$\sigma_{12}$$                               |
| S13            | $$\sigma_{13}$$                               |
| S22            | $$\sigma_{22}$$                               |
| S23            | $$\sigma_{23}$$                               |
| S33            | $$\sigma_{33}$$                               |
| E              | all strain components                         |
| E11            | $$\varepsilon_{11}$$                          |
| E12            | $$\varepsilon_{12}$$                          |
| E13            | $$\varepsilon_{13}$$                          |
| E22            | $$\varepsilon_{22}$$                          |
| E23            | $$\varepsilon_{23}$$                          |
| E33            | $$\varepsilon_{33}$$                          |
| EE             | all elastic strain components                 |
| EE11           | $$\varepsilon^e_{11}$$                        |
| EE12           | $$\varepsilon^e_{12}$$                        |
| EE13           | $$\varepsilon^e_{13}$$                        |
| EE22           | $$\varepsilon^e_{22}$$                        |
| EE23           | $$\varepsilon^e_{23}$$                        |
| EE33           | $$\varepsilon^e_{33}$$                        |
| PE             | all plastic strain components                 |
| PE11           | $$\varepsilon^p_{11}$$                        |
| PE12           | $$\varepsilon^p_{12}$$                        |
| PE13           | $$\varepsilon^p_{13}$$                        |
| PE22           | $$\varepsilon^p_{22}$$                        |
| PE23           | $$\varepsilon^p_{23}$$                        |
| PE33           | $$\varepsilon^p_{33}$$                        |
| SP             | all principal stress components               |
| SP1            | principal stress component 1                  |
| SP2            | principal stress component 2                  |
| SP3            | principal stress component 3                  |
| EP             | all principal strain components               |
| EP1            | principal strain component 1                  |
| EP2            | principal strain component 2                  |
| EP3            | principal strain component 3                  |
| EEP            | all principal elastic strain components       |
| EEP1           | principal elastic strain component 1          |
| EEP2           | principal elastic strain component 2          |
| EEP3           | principal elastic strain component 3          |
| PEP            | all principal plastic strain components       |
| PEP1           | principal plastic strain component 1          |
| PEP2           | principal plastic strain component 2          |
| PEP3           | principal plastic strain component 3          |
| HYDRO          | hydrostatic stress                            |
| MISES          | von Mises stress                              |
| EEQ            | equivalent strain                             |
| EEEQ           | equivalent elastic strain                     |
| PEEQ           | equivalent plastic strain                     |
| HIST           | history vector                                |
| YF             | yield flag                                    |

## General Global Quantities

The following quantities are available at global level, which can be recorded using global recorders.

| variable label | physical meaning                              |
|----------------|-----------------------------------------------|
| KE             | kinetic energy                                |
| SE             | strain energy                                 |
| VE             | viscous energy                                |
| NVE            | nonviscous viscous energy                     |
| K              | stiffness matrix                              |
| M              | mass matrix                                   |
| AMP            | amplitude                                     |

## Special Quantities

The following are some special quantities that are only available for certain models.

| variable label | physical meaning                              |
|----------------|-----------------------------------------------|
| ED             | damper strain in Maxwell/Kelvin model         |
| VD             | damper strain rate in Maxwell/Kelvin model    |
| SD             | damper stress in Maxwell/Kelvin model         |
| ES             | spring strain in Maxwell/Kelvin model         |
| VS             | spring strain rate in Maxwell/Kelvin model    |
| SS             | spring stress defined in Maxwell/Kelvin model |
| DAMAGE         | damage variable in phase field models         |
| DT             | tension damage                                |
| DC             | compressive damage                            |
| PP             | pore pressure                                 |
| VF             | volume fraction in Gurson related models      |
| LITR           | location iteration in Maxwell model           |
| BEAME          | beam end deformation                          |
| BEAMS          | beam end resultant forces                     |