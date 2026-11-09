This section contains all available material models.

!!! info "reference book"
    The theoretical formulations of most models are provided in the reference book [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook).
    The book may be consulted for further details and insights.

There are mainly two categories: 1D and 3D material models.

Wrappers of various types are provided to allow one to wrap one material model into another that can be used
in a different context.

All material models support the following basic output types.

| variable label | physical meaning              |
|----------------|-------------------------------|
| S              | all stress components         |
| E              | all strain components         |
| EE             | all elastic strain components |
| PE             | all plastic strain components |
| HIST           | history vector                |
| YF             | yield flag                    |
