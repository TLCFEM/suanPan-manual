# material

Passing CPP objects to/from libraries may have stability issues. The strong coupling between main executable and library
results in users have to make sure both executable and library are compiled with the same compiler of the same version.
This does not sound nice.

A C type interface is more stable. The C interface of material models is implemented via a common function with a
trailing `_handler`. The function takes a pointer to `ExternalMaterialData` structure with plain PODs as input argument
and operates on that based on the operation indicated by a pointer to an integer. If the material model has a name
of `samplemat`, then the signature will be

```cpp
SUANPAN_EXPORT void samplemat_handler(ExternalMaterialData* data, int* info);
```

## Communication Convention

On entry, based on different values of `*info`, a set of different operations need to be done and the corresponding
results need to be stored in `*data`. The structure of `*data` would be explained later, we focus on `*info` in this
section.

In general, two states should be managed in the material model. The current state stores converged variables from the
last converged time step. The trial state stores updated variables based on trial strain, trial strain rate, etc. This
state may or may not be the converged state, thus may or may not be kept in an incremental setup.

| value | operation                                                                  |
|-------|----------------------------------------------------------------------------|
| 0     | allocate memory, initialise variables based on parameters defined by users |
| 1     | deallocate memory that is previously allocated in operation `*info=0`      |
| 2     | update material state based on new trial strain only                       |
| 3     | update material state based on new trial strain and new trial strain rate  |
| 4     | commit trial state to current state                                        |
| 5     | reset trial state to current state                                         |
| 6     | clear both current and trial state to zero                                 |
| 7     | validate if the model parameters are legal                                 |

Some remarks to explain those operations.

1. In operation `*info=0`, memory shall be allocated to store two states and other relevant variables. Since it is not
   known to the main executable how large the memory is required, this has to be done by the library using whatever
   methods to allocate.
2. In operation `*info=2`, trial state is updated based on trial strain and current state (as an incremental form is
   implemented). This operation will be called in a static analysis, or by elements that only computes strains. Before
   calling this operation, the trial strain will be written to the corresponding location of allocated memory some place
   defined in `*data`.
3. In operation `*info=3`, trial state is updated based on trial strain, trial strain rate and current state (as an
   incremental form is implemented). This operation will be called by elements that computes both strains and strain
   rates and pass them to material models. Often, the resulting stiffness and damping matrices shall be computed. Before
   calling this operation, the trial strain and the trial strain rate will be written to the corresponding location of
   allocated memory some place defined in `*data`.
4. In operation `*info=4`, we simply overwrite current state with trial state as the trial state now converges after
   several iterations.
5. In operation `*info=5`, when this operation is called, convergence is not met, so we overwrite trial state with
   current state and update the system with a smaller increment of (pseudo) time.
6. In operation `*info=6`, all state variables and history variables shall be reverted to initial (potential zero)
   state.
7. In operation `*info=7`, all model parameters shall be checked to see if a proper material model can be defined. This
   cannot be done in the main executable although the command is processed in the main executable, in which all
   parameters will be read as double inputs and stored in a raw double array in `*data`.

In a typical analysis flow, `*info=0` will be called first to initialise memory, then `*info=7` will be called to valid
parameters. If it fails, `*info=1` will be called. Otherwise, either `*info=2` or `*info=3` will be called to update
states, followed by appropriate remaining operations.

For any material models, developers must provide implementations of the above eight operations. Whether those
implementations are combined with the exported handler or wrapped in separate functions is left to developers to decide.

On exit, `*info=0` indicates the operation succeeds and no error has been reported, it can be set to other values to
terminate analysis.

## Data Layout

The `ExternalMaterialData` structure has the following definition.

```cpp
struct ExternalMaterialData {
 unsigned size = 0;          // indicate the dimension of material
 unsigned constant_size = 0; // indicate the number of constants

 int c_strain = -1;      // current status
 int c_strain_rate = -1; // current status
 int c_stress = -1;      // current status

 int t_strain = -1;      // trial status
 int t_strain_rate = -1; // trial status
 int t_stress = -1;      // trial status

 int c_history = -1;   // current status
 int c_stiffness = -1; // stiffness matrix
 int c_damping = -1;   // damping matrix

 int t_history = -1;   // trial status
 int t_stiffness = -1; // stiffness matrix
 int t_damping = -1;   // damping matrix

 int i_history = -1;   // initial status
 int i_stiffness = -1; // stiffness matrix
 int i_damping = -1;   // damping matrix

 double density = 0.;

 double* pool = nullptr;     // stores states, should be allocated by dll
 double* constant = nullptr; // stores model constants, should be allocated by main exe
};
```

The unsigned integers are used to indicate the sizes. For 1D, 2D and 3D problems, `size` should be `1`, `3` and `6`.
The `constant` pointer points to the head of model parameters.

The integers are indices used to indicate the location of the first element of the corresponding variable in `pool`. A
negative value `-1` means the corresponding variable is not used by the model. For a 3D trial strain, it will be stored
in the continuous memory from `pool[t_strain]` to `pool[t_strain+6]`.

During initialisation (`*info=0`), some positive values shall be assigned if the target variable will be used in the
model, otherwise, leave it as `-1`. The `pool` shall be allocated with whatever size required. `*pool` stores not only
mandatory state variables, it can further store additional history variables manages by the model itself.

## Example

Here we present a simple uniaxial elastic material example. For the full code, please check the
file `Developer/Material/ElasticExternal.cpp`.

### The Handler

Although it is a C style interface, CPP syntax can be used. Each operation is wrapped in separate functions.

```cpp
SUANPAN_EXPORT void elasticexternal_handler(ExternalMaterialData* data, int* info) {
 if(0 == *info) allocate_material(data, info);
 else if(1 == *info) deallocate_material(data, info);
 else if(2 == *info) static_update(data, info);
 else if(3 == *info) dynamic_update(data, info);
 else if(4 == *info) commit(data, info);
 else if(5 == *info) reset(data, info);
 else if(6 == *info) clear(data, info);
 else if(7 == *info) validate(data, info);
 else {
  suanpan_error("unknown flag received.\n");
  *info = -1;
 }
}
```

### Allocation

Since it is a uni-axial elastic material, `size` should be one. Strain, stress and stiffness related variables are used,
the rest can remain unused. We arrange the data in the following layout.

| index     | value             |
|-----------|-------------------|
| `pool[0]` | current strain    |
| `pool[1]` | trial strain      |
| `pool[2]` | current stress    |
| `pool[3]` | trial stress      |
| `pool[4]` | initial stiffness |
| `pool[5]` | current stiffness |
| `pool[6]` | trial stiffness   |

No history variables are involved in this elastic material model. The `pool` can be allocated by `new double[7]` and
filled with zeros. Then elastic modulus, which is assumed to be the first model parameter (`constant[0]`), is copied to
stiffness.

The density shall be handled as well. If there are more than one model parameter, the second is assumed to be density.

```cpp
void allocate_material(ExternalMaterialData* data, int* info) {
 data->size = 1;

 data->c_strain = 0;
 data->t_strain = 1;
 data->c_stress = 2;
 data->t_stress = 3;
 data->i_stiffness = 4;
 data->c_stiffness = 5;
 data->t_stiffness = 6;

 data->pool = new double[7];

 if(nullptr == data->pool) *info = -1;

 for(auto I = 0; I < 7; ++I) data->pool[I] = 0.;

 data->pool[data->c_stiffness] = data->pool[data->t_stiffness] = data->pool[data->i_stiffness] = data->constant[0];

 if(data->constant_size > 1) data->density = data->constant[1];
}
```

With such a definition, the command used to define such a model is

```
material ElasticExternal (1) (2) [3]
# (1) int, unique material tag
# (2) double, elastic modulus
# [3] double, density, default: 0.0
```

### Deallocation

The `pool` needs to be deallocated.

```cpp
void deallocate_material(ExternalMaterialData* data, int* info) {
 delete[] data->pool;

 *info = 0;
}
```

### Update Based On Strain

No local iteration is required to update state, thus stress can always be computed by multiply strain with elastic
modulus, which is

$$
\sigma^{n}=E~\varepsilon^{n}
$$

For complex models, alias can be used to simplify code.

```cpp
void static_update(ExternalMaterialData* data, int* info) {
 data->pool[data->t_stress] = data->pool[data->t_stiffness] * data->pool[data->t_strain];

 *info = 0;
}
```

### State Manipulation

It is straightforward.

```cpp
void commit(ExternalMaterialData* data, int* info) {
 data->pool[data->c_strain] = data->pool[data->t_strain];
 data->pool[data->c_stress] = data->pool[data->t_stress];

 *info = 0;
}

void reset(ExternalMaterialData* data, int* info) {
 data->pool[data->t_strain] = data->pool[data->c_strain];
 data->pool[data->t_stress] = data->pool[data->c_stress];

 *info = 0;
}

void clear(ExternalMaterialData* data, int* info) {
 data->pool[data->c_strain] = data->pool[data->t_strain] = 0.;
 data->pool[data->c_stress] = data->pool[data->t_stress] = 0.;

 *info = 0;
}
```

### Validation

For this model, there should be at least one model parameter.

```cpp
void validate(ExternalMaterialData* data, int* info) {
 *info = 0 == data->constant_size ? -1 : 0;
}
```
