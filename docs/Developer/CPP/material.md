# Material

## Things to Know

1. There is no need to write wrappers. Various wrappers are available to wrap 3D material models for 1D and 2D
   applications.
2. Unless the 2D material model is formulated directly in the 2D space, for example the plane stress space (such as the
   Barlat-Lian model), developers are not encouraged to write any 2D versions of 3D models.

## Main Tasks of a Material Model

The material model is often associated with the integration point to compute the material response. As a general
purposed computation framework, in general, most material models are not tied to any specific element types.

The main task of a material model is to compute the response based on the input(s). The input may be displacement,
strain, velocity, strain rate, etc. The corresponding response could be force, stress and stiffness.

Hence, the associated element would call the material model to pass, for example, the trial strain to update the trial
state. The material model shall compute the response of the trial state based on current state and stored history
variables.

## Abstraction

The abstraction of the `Material`class is given in the `MaterialBase` class.

## Data Storage

All data is stored in a `struct` named as `MaterialData`.

```cpp
struct MaterialData {
 const double tolerance = 1E-14;
 const double density = 0.; // density
 const MaterialType material_type = MaterialType::D0;

 vec current_strain;      // current status
 vec current_strain_rate; // current status
 vec current_stress;      // current status
 vec current_stress_rate; // current status

 vec trial_strain;      // trial status
 vec trial_strain_rate; // trial status
 vec trial_stress;      // trial status
 vec trial_stress_rate; // trial status

 vec incre_strain;      // incremental status
 vec incre_strain_rate; // incremental status
 vec incre_stress;      // incremental status
 vec incre_stress_rate; // incremental status

 vec initial_history; // initial status
 vec current_history; // current status
 vec trial_history;   // trial status

 mat initial_stiffness; // stiffness matrix
 mat current_stiffness; // stiffness matrix
 mat trial_stiffness;   // stiffness matrix

 mat initial_damping; // damping matrix
 mat current_damping; // damping matrix
 mat trial_damping;   // damping matrix
};
```

Two states are stored. The current state is the converged state while the trial state should be updated for each
iteration. The difference between two states is also stored, given that some material models is formulated based on an
incremental form.

The variable `initial_history` can be used to assign initial conditions. A detailed layout shall be provided in the
corresponding manual page.

***It is not compulsory to use pre-defined variables. It is possible to use user-defined variables to manage states.
However, several methods shall be overridden, which makes codes longer.***

***To save memory, it is recommended to reset pre-defined variables during the initialization if user-defined variables
are used. Details will be covered in the discussion of the corresponding methods.***

## Pure Virtual Methods

Some methods are labelled as pure virtual methods, meaning that they need to be overridden in the derived classes.

```cpp
 virtual void initialize(const shared_ptr<DomainBase>& = nullptr) = 0; // for initialization of the model

 virtual unique_ptr<Material> get_copy() = 0; // to get a deep copy for local usage

 virtual int clear_status() = 0; // state control
 virtual int commit_status() = 0; // state control
 virtual int reset_status() = 0; // state control
```

Apart from those five methods, the updater shall be overridden as well. Two methods are defined. The first one accepts
trial strain as input. **This method has no default behaviour, so it needs to be implemented in all derived classes
otherwise it throws an exception.**

```cpp
 virtual int update_trial_status(const vec&);
```

The second one accepts trial strain and trial strain rate as inputs. By default, this method calls the above method with
trial strain. If the material model is rate independent, this method can be left unchanged.

```cpp
 virtual int update_trial_status(const vec&, const vec&);
```

Some element models may call the material model with increments. The according methods are defined as well.

```cpp
 virtual int update_incre_status(const vec&);
 virtual int update_incre_status(const vec&, const vec&);
```

By default, these two methods compute the trial state by adding increments to the current state and call the
corresponding `update_trial_status()` method.

For 1D material models, often the trial strain (rate) is directly stored in a scalar. So the scalar versions of the
above four methods are defined.

```cpp
 int update_incre_status(double);
 int update_incre_status(double, double);
 int update_trial_status(double);
 int update_trial_status(double, double);
```

By default, these methods wrap the input scalars into `vec` variables and call the corresponding vector versions of
these methods. If there is no special considerations, these four methods do not need to be overridden.

## Material In Details

### Initialization

The initialization procedure is performed before the analysis. The main task is to formulate for example the initial
stiffness, initialize the corresponding history variables (if any), etc. The pointer of the domain that the current
material model is defined in is sent to the initialization method in case of any other resources are required by the
current material model.

As the material model is the bottom layer of FEA, most models are independent of other components of the problem domain.

The following is an example from the `NonlinearJ2` class.

```cpp
void NonlinearJ2::initialize(const shared_ptr<DomainBase>&) {
 trial_stiffness = current_stiffness = initial_stiffness = tensor::isotropic_stiffness(elastic_modulus, poissons_ratio);

 initialize_history(7);
}
```

In this method, the initial/current/trial stiffness matrix is set to the isotropic elastic matrix by calling the
function `tensor::isotropic_stiffness` with elastic modulus and Poisson's ratio.

Then the history variables are initialized. A scalar (accumulated plastic strain) and a six-component vector (back
stress) are required so the total size of history variables is 7.

***It shall be noted that, if the model is designed to support nonzero initial history, viz., initial conditions,
history variables cannot be initialized by directly call the `zeros()` method. The method `initialize_history()` shall
be called instead. This method checks if the initial history is set. If yes, the initial condition will be retained.***

By default, strain, stress and stiffness will be initialized in the base class implementation of `initialize()`. If any
of those variables are not used, it is possible to reset them to save memory in the derived implementation
of `initialize()`.

### Copier

By implementing the copy constructor (if necessary), the copier can be written in one line. Each integration point needs
a material object for local use.

```cpp
unique_ptr<Material> DerivedClassName::get_copy() { return make_unique<DerivedClassName>(*this); }
```

### State Control

Although when the built-in variables are used, the state control methods can be implemented in a universal approach. For
example,

```cpp
int Material::clear_status() {
 if(!current_strain.is_empty()) current_strain.zeros();
 if(!current_strain_rate.is_empty()) current_strain_rate.zeros();
 if(!current_stress.is_empty()) current_stress.zeros();

 if(!trial_strain.is_empty()) trial_strain.zeros();
 if(!trial_strain_rate.is_empty()) trial_strain_rate.zeros();
 if(!trial_stress.is_empty()) trial_stress.zeros();

 if(initial_history.is_empty()) {
  if(!current_history.is_empty()) current_history.zeros();
  if(!trial_history.is_empty()) trial_history.zeros();
 } else trial_history = current_history = initial_history;

 if(!initial_stiffness.is_empty()) trial_stiffness = current_stiffness = initial_stiffness;

 return SUANPAN_SUCCESS;
}

int Material::commit_status() {
 if(!trial_strain.is_empty()) current_strain = trial_strain;
 if(!trial_strain_rate.is_empty()) current_strain_rate = trial_strain_rate;
 if(!trial_stress.is_empty()) current_stress = trial_stress;
 if(!trial_history.is_empty()) current_history = trial_history;
 if(!trial_stiffness.is_empty()) current_stiffness = trial_stiffness;

 return SUANPAN_SUCCESS;
}

int Material::reset_status() {
 if(!trial_strain.is_empty()) trial_strain = current_strain;
 if(!trial_strain_rate.is_empty()) trial_strain_rate = current_strain_rate;
 if(!trial_stress.is_empty()) trial_stress = current_stress;
 if(!trial_history.is_empty()) trial_history = current_history;
 if(!trial_stiffness.is_empty()) trial_stiffness = current_stiffness;

 return SUANPAN_SUCCESS;
}
```

Developers can still choose to manage state variables by them own. Similar to elements, all state updates, including all
history variables, shall only happen in the `update_trial_status()` method to keep a simple and clean structure.