This section contains all available material models.

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
