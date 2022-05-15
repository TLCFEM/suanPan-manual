# Element

## Abstraction

The abstraction of the `Element` class is defined in `ElementBase` class. Readers can check that header to get an
overall picture of all methods implemented.

## Variables and Methods

The `Element` class manages two states by default: current converged state and trial state. Accordingly, several
build-in variables are defined, they are grouped in a struct. Some frequently used variables are listed as follows. A
complete list can be found in the header of `Element` class.

```cpp
struct ElementData {
 const uvec node_encoding; // node encoding
 const uvec material_tag;  // material tags
 const uvec section_tag;   // section tags

 const bool nlgeom = false; // nonlinear geometry switch

 bool update_mass = true;      // flag to indicate if update matrix
 bool update_damping = true;   // flag to indicate if update matrix
 bool update_stiffness = true; // flag to indicate if update matrix
 bool update_geometry = true;  // flag to indicate if update matrix

 uvec dof_encoding; // DoF encoding vector

 mat initial_mass;      // mass matrix
 mat initial_damping;   // damping matrix
 mat initial_stiffness; // stiffness matrix
 mat initial_geometry;  // geometry matrix

 mat trial_mass;      // mass matrix
 mat trial_damping;   // damping matrix
 mat trial_stiffness; // stiffness matrix
 mat trial_geometry;  // geometry matrix

 mat current_mass;      // mass matrix
 mat current_damping;   // damping matrix
 mat current_stiffness; // stiffness matrix
 mat current_geometry;  // geometry matrix

 vec trial_resistance;       // resistance vector
 vec current_resistance;     // resistance vector
 vec trial_damping_force;    // damping force
 vec current_damping_force;  // damping force
 vec trial_inertial_force;   // inertial force
 vec current_inertial_force; // inertial force

 vec trial_body_force;
 vec current_body_force;
 vec trial_traction;
 vec current_traction;

 mat body_force;
 mat traction;
};
```

There are some build-in methods to get nodal information. The purposes are indicated by method names. These methods are
implemented through the stored node pointers. The same functionalities can be reimplemented manually otherwise those
predefined methods are sufficient in most cases.

```cpp
mat get_coordinate(unsigned) const;

vec get_incre_displacement() const;
vec get_incre_velocity() const;
vec get_incre_acceleration() const;
vec get_trial_displacement() const;
vec get_trial_velocity() const;
vec get_trial_acceleration() const;
vec get_current_displacement() const;
vec get_current_velocity() const;
vec get_current_acceleration() const;

vec get_node_incre_resistance() const;
vec get_node_trial_resistance() const;
vec get_node_current_resistance() const;

vector<shared_ptr<Material>> get_material(const shared_ptr<DomainBase>&) const;
vector<shared_ptr<Section>> get_section(const shared_ptr<DomainBase>&) const;
```

## Constructor

The most common constructor looks like this.

```cpp
 Element(unsigned,    // tag
         unsigned,    // number of nodes
         unsigned,    // number of dofs
         uvec&&,      // node encoding
         uvec&&,      // material tags
         bool,        // nonlinear geometry switch
         MaterialType // material type for internal check
 );
```

Some elements are based on sections while some elements are based on integration points that are directly tied to
material models. The above is the constructor used for material based elements. The number of nodes and the number of
DoFs per node shall be passed to `Element` class so that the connected nodes can be correctly initialized, as well as
all related matrices. Either material tags or section tags shall be passed to define the element. During initialization,
if no proper material/section tag is provided, the target element will be disabled. Also, the associated
material/section model will be checked if the dimension matches. The nonlinear geometry switch allows the nonlinear
version to be implemented in the same class.

There are some other constructors. The following one can be used to define elements that depend on node groups (a number
of nodes organized in groups).

```cpp
 Element(unsigned, // tag
         unsigned, // number of dofs
         uvec&&    // group encoding
 );
```

And the following one defines elements that require information of other elements.

```cpp
 Element(unsigned, // tag
         unsigned, // number of dofs
         unsigned, // other element tag
         unsigned  // node tag
 );
```

The initialization is able to handle these different types of elements.

## Initialization

Any derived element class shall implement the initializer.

```cpp
virtual void initialize(const shared_ptr<DomainBase>&) = 0;
```

This method takes a `DomainBase` pointer that allows the target element to acquire material/section objects and/or other
necessary information to initialize the element. A better illustration can be seen in an example element implementation.
For the moment, we only need to know this must be overridden.

The `Element` class itself provides an initializer to initialise common variables.

```cpp
void initialize_base(const shared_ptr<DomainBase>&) override final;
```

A number of tasks are performed in the default initialization.

1. Check if all involved nodes are active, if not, the element will be disabled.
2. Check the current number of DoFs of each involved node, if it is smaller than that required by the current element,
   then reset it.
3. Check if there is a valid and active material/section model based on the corresponding tag provided in the
   constructor, if not, the element will be disabled.
4. On the second run, check again if all nodes are active, if not, the element will be disabled.

## General Procedure

The main task of an element is to provide force response based on the trial nodal displacements. In the meantime, the
corresponding matrices such as tangent stiffness, or tangent modulus in 1D case, shall be provided.

The only entrance to update an element is the method `update_status()`. All trial state associated variables shall be
updated in this method. Then several getters are available to return the corresponding variables. This is the default
strategy adopted by all existing elements. However, there are other options. For some solvers, the number of calls to
get, for example, trial resistance would be multiples of that to get tangent stiffness. For some algorithms, tangent
stiffness matrix will only be assembled in the first iteration of each sub-step. In this case, it would be unnecessary
to update trial stiffness in each call of `update_status()`, rather, it can be implemented in the
getter `get_trial_stiffness()` to minimize the computational cost. This is not chosen by default to simplify the
development. Please check the following section for details.

## Two Paths

### If You Decide To Use Predefined Variables

The predefined variables are sufficient to manage element state in most cases. If so, only four methods shall be
implemented.

```cpp
virtual int update_status() = 0; // update trial
virtual int clear_status() = 0;  // clear both trial and current
virtual int commit_status() = 0; // commit trial to current
virtual int reset_status() = 0;  // reset trial to current
```

The latter three manage states. Normally it is necessary to call the corresponding methods in all related
material/section models if the implemented element itself does not store history variables. As the name suggests, we
need to update the trial state in the first method. A general procedure would be:

1. obtain nodal displacement/velocity vector by calling for example `get_trial_displacement()`,
2. compute strain at each integration point,
3. update material models using new trial strains,
4. get material response and form element resistance and stiffness matrix. If necessary, mass/damping matrix shall be
   updated according to the new trial state.

### If You Decide To Manage States In Your Way

In this case, probably all build-in variables won't be used. To manage states, following additional methods shall be
overridden.

```cpp
virtual const vec& get_trial_resistance() const;
virtual const vec& get_current_resistance() const;

virtual const mat& get_trial_mass() const;
virtual const mat& get_trial_damping() const;
virtual const mat& get_trial_stiffness() const;
virtual const mat& get_trial_geometry() const;
virtual const mat& get_trial_secant() const;

virtual const mat& get_current_mass() const;
virtual const mat& get_current_damping() const;
virtual const mat& get_current_stiffness() const;
virtual const mat& get_current_geometry() const;
virtual const mat& get_current_secant() const;

virtual const mat& get_initial_mass() const;
virtual const mat& get_initial_damping() const;
virtual const mat& get_initial_stiffness() const;
virtual const mat& get_initial_geometry() const;
virtual const mat& get_initial_secant() const;
```

As a general guideline, here are some conventions to follow:

1. It is not recommended using the second approach, that is, managing internal variables at derived class level, unless
   all methods are carefully implemented.
2. All state updates, including all history variables, shall only happen in the `update_status()` method, as all get
   methods are declared as `const`.
3. It is sometimes useful to update trial strain related variables only in `update_status()` and compute responses in
   the corresponding getters. In that case, a `const_cast` is required. By doing so, developers must clearly know what
   the operation means. A typical example would be, for example, the modified Newton algorithm or
   the [`BFGS`](../../Library/Solver/BFGS.md) method, in which `update_status()` will only be called once and getters of
   resistances and matrices would be called several times for each iteration in each sub-step. Splitting updater and
   getters apart will for sure save some computation efforts but is also error-prone.
4. Normally the damping matrix and the mass matrix shall only be defined as functions of current state at most --- if
   they are not constants. Essentially, they cannot be functions of trial strain/displacement if a quadratic convergence
   rate shall be preserved.
5. If the stiffness matrix is constant throughout the analysis, it is recommended to use
   function `ConstantStiffness(ElementData*)` to declare such a feature in order to save some memory.
6. If the damping matrix is constant throughout the analysis, it is recommended to use
   function `ConstantDamping(ElementData*)` to declare such a feature in order to save some memory.
7. If the mass matrix is constant throughout the analysis, it is recommended to use
   function `ConstantMass(ElementData*)` to declare such a feature in order to save some memory.

## Record Response

To record response, simply override

```cpp
virtual vector<vec> record(OutputType);
```

A number of physical variables can be identified and output accordingly in this method. Except for some special elements
that stores element-wise variables, most elements would directly forward call `record(OutputType)` in the associated
material objects following the order of integration points and generate and return a `vector<vec>`.

## Remarks

In general, implementing a new element class is not a difficult task. Basically, there are two things to do: 1)
initialize the element correctly and 2) update element status using nodal information in a correct, iterative way. The
remaining is automatically handled by the base class.

For different dimensions, here are some very simple elements implemented for reference.

1. 1D --- `Spring01` a spring element based on infinitesimal displacement.
2. 2D --- `ElementExample` a three-node triangle plain membrane element.
3. 3D --- `C3D4` a four-node tetragon using one-node integration.