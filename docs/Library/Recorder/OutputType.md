# Output Type

Currently, the available types of output variables are listed as follows.

Please note, in principle, it is possible to define any types on any recorders, but if the target recorder does not 
support the type, trivial/empty values will be returns. If saving recorder does not create any files on the disk, 
meaning that the output type is not available for the target object. For example, recording strain/stress `E`/`S` 
values of any nodes is not possible and will lead to no output.

The complete support list is still under development. In principle, basic types such as 
displacement/velocity/acceleration are available for nodes. For elemental response, generally stress/strain and 
their components are available. Some output types are only supported by certain elements. Please feel free to open 
an issue if you need more information.

| variable label | physical meaning                                                        |
|----------------|-------------------------------------------------------------------------|
| A              | all acceleration components                                             |
| A1             | acceleration along DoF 1                                                |
| A2             | acceleration along DoF 2                                                |
| A3             | acceleration along DoF 3                                                |
| A4             | acceleration along DoF 4                                                |
| A5             | acceleration along DoF 5                                                |
| A6             | acceleration along DoF 6                                                |
| AR             | rotation acceleration components                                        |
| AR1            | rotation acceleration along DoF 1                                       |
| AR2            | rotation acceleration along DoF 2                                       |
| AR3            | rotation acceleration along DoF 3                                       |
| AT             | translation acceleration                                                |
| AXIAL          | axial force                                                             |
| DC             | compressive damage defined in CDP model                                 |
| DT             | tension damage defined in CDP model                                     |
| E              | all strain components                                                   |
| E11            | $$\varepsilon_{11}$$                                                    |
| E12            | $$\varepsilon_{12}$$                                                    |
| E13            | $$\varepsilon_{13}$$                                                    |
| E22            | $$\varepsilon_{22}$$                                                    |
| E23            | $$\varepsilon_{23}$$                                                    |
| E33            | $$\varepsilon_{33}$$                                                    |
| ED             | damper strain defined in Maxwell model                                  |
| EE             | all elastic strain components                                           |
| EE11           | $$\varepsilon^e_{11}$$                                                  |
| EE12           | $$\varepsilon^e_{12}$$                                                  |
| EE13           | $$\varepsilon^e_{13}$$                                                  |
| EE22           | $$\varepsilon^e_{22}$$                                                  |
| EE23           | $$\varepsilon^e_{23}$$                                                  |
| EE33           | $$\varepsilon^e_{33}$$                                                  |
| EEEQ           | equivalent elastic strain                                               |
| EEP            | all principal elastic strain components                                 |
| EEP1           | principal elastic strain component 1                                    |
| EEP2           | principal elastic strain component 2                                    |
| EEP3           | principal elastic strain component 3                                    |
| EEQ            | equivalent strain                                                       |
| EINT           | interpolation parameters of the strain field defined in (S)GCMQ element |
| EP             | all principal strain components                                         |
| EP1            | principal strain component 1                                            |
| EP2            | principal strain component 2                                            |
| EP3            | principal strain component 3                                            |
| ES             | spring strain                                                           |
| HYDRO          | hydrostatic stress                                                      |
| K              | stiffness matrix                                                        |
| KAPPAC         | $$\kappa_c$$ defined in CDP model                                       |
| KAPPAP         |                                                                         |
| KAPPAT         | $$\kappa_t$$ defined in CDP model                                       |
| KE             | kinetic energy                                                          |
| LITR           | location iteration                                                      |
| M              | mass matrix                                                             |
| MISES          | von Mises stress                                                        |
| MOMENT         | section moment                                                          |
| MOMENTUM       | system momentum vector                                                  |
| MOMENTUMX      | nodal/global momentum component 1                                       |
| MOMENTUMY      | nodal/global momentum component 2                                       |
| MOMENTUMZ      | nodal/global momentum component 3                                       |
| MOMENTUMRX     | nodal/global momentum component 4                                       |
| MOMENTUMRY     | nodal/global momentum component 5                                       |
| MOMENTUMRZ     | nodal/global momentum component 6                                       |
| NL             |                                                                         |
| NMISES         | averaged von Mises stress on element level                              |
| PE             | all plastic strain components                                           |
| PE11           | $$\varepsilon^p_{11}$$                                                  |
| PE12           | $$\varepsilon^p_{12}$$                                                  |
| PE13           | $$\varepsilon^p_{13}$$                                                  |
| PE22           | $$\varepsilon^p_{22}$$                                                  |
| PE23           | $$\varepsilon^p_{23}$$                                                  |
| PE33           | $$\varepsilon^p_{33}$$                                                  |
| PEEQ           | equivalent plastic strain                                               |
| PEP            | all principal plastic strain components                                 |
| PEP1           | principal plastic strain component 1                                    |
| PEP2           | principal plastic strain component 2                                    |
| PEP3           | principal plastic strain component 3                                    |
| REBARE         | rebar strain                                                            |
| REBARS         | rebar stress                                                            |
| RESULTANT      | all resultant forces                                                    |
| RF             | all reaction force components                                           |
| RF1            | reaction force along DoF 1                                              |
| RF2            | reaction force along DoF 2                                              |
| RF3            | reaction force along DoF 3                                              |
| RM             | all reaction moment components                                          |
| RM1            | reaction moment along DoF 1                                             |
| RM2            | reaction moment along DoF 2                                             |
| RM3            | reaction moment along DoF 3                                             |
| RT             | all translational reaction moment components                            |
| DF             | all nodal damping force components                                      |
| DF1            | damping force along DoF 1                                               |
| DF2            | damping force along DoF 2                                               |
| DF3            | damping force along DoF 3                                               |
| DM1            | damping force along DoF 4                                               |
| DM2            | damping force along DoF 5                                               |
| DM3            | damping force along DoF 6                                               |
| IF             | all nodal inertial force components                                     |
| IF1            | inertial force along DoF 1                                              |
| IF2            | inertial force along DoF 2                                              |
| IF3            | inertial force along DoF 3                                              |
| IM1            | inertial force along DoF 4                                              |
| IM2            | inertial force along DoF 5                                              |
| IM3            | inertial force along DoF 6                                              |
| S              | all stress components                                                   |
| S11            | $$\sigma_{11}$$                                                         |
| S12            | $$\sigma_{12}$$                                                         |
| S13            | $$\sigma_{13}$$                                                         |
| S22            | $$\sigma_{22}$$                                                         |
| S23            | $$\sigma_{23}$$                                                         |
| S33            | $$\sigma_{33}$$                                                         |
| SD             | damper stress                                                           |
| SE             | strain energy                                                           |
| SHEAR          | section shear force                                                     |
| SINT           | interpolation parameters of the stress field defined in (S)GCMQ element |
| SINV           |                                                                         |
| SP             | all principal stress components                                         |
| SP1            | principal stress component 1                                            |
| SP2            | principal stress component 2                                            |
| SP3            | principal stress component 3                                            |
| SS             | spring stress defined in Maxwell model                                  |
| TORSION        |                                                                         |
| TRESC          | Tresca stress                                                           |
| U              | all displacement components                                             |
| U1             | displacement along DoF 1                                                |
| U2             | displacement along DoF 2                                                |
| U3             | displacement along DoF 3                                                |
| U4             | displacement along DoF 4                                                |
| U5             | displacement along DoF 5                                                |
| U6             | displacement along DoF 6                                                |
| UR             | all rotational displacement components                                  |
| UR1            | rotational displacement along DoF 1                                     |
| UR2            | rotational displacement along DoF 2                                     |
| UR3            | rotational displacement along DoF 3                                     |
| UT             | all translational displacement components                               |
| V              | all velocity components                                                 |
| V1             | velocity along DoF 1                                                    |
| V2             | velocity along DoF 2                                                    |
| V3             | velocity along DoF 3                                                    |
| V4             | velocity along DoF 4                                                    |
| V5             | velocity along DoF 5                                                    |
| V6             | velocity along DoF 6                                                    |
| VD             | damper velocity defined in Maxwell model                                |
| VF             | void fraction defined in Gurson related models                          |
| VR             | all angular velocity components                                         |
| VR1            | angular velocity along DoF 1                                            |
| VR2            | angular velocity along DoF 2                                            |
| VR3            | angular velocity along DoF 3                                            |
| VS             |                                                                         |
| VT             |                                                                         |
