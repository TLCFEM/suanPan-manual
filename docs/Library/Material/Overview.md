This section contains all available material models.

!!! info "reference book"
    The theoretical formulations of most models are provided in the reference book [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook).
    The book may be consulted for further details and insights.

There are mainly two categories: 1D and 3D material models.

Wrappers of various types are provided to allow one to wrap one material model into another that can be used in a different context.

All material models support the following basic output types.

| variable label | physical meaning              |
|----------------|-------------------------------|
| S              | all stress components         |
| E              | all strain components         |
| EE             | all elastic strain components |
| PE             | all plastic strain components |
| HIST           | history vector                |
| YF             | yield flag                    |

## Material Categories

The library groups models by spatial dimension and by the physical mechanism they represent.
One-dimensional models return a single axial stress and are used with truss, beam, damper and fiber-section elements.
Three-dimensional models return a full stress tensor and are required when multiaxial stress states, shear or non-proportional loading matter.
Elastic models provide a reversible secant or tangent relation and are the baseline for all other families.
Plasticity models introduce a yield surface and a flow rule to represent permanent deformation, with metal plasticity described in the [`Metal`](Guide/Metal.md) guide.
Hysteresis models reproduce a prescribed unloading and reloading shape without necessarily defining a yield surface.
Concrete models cover rule-based cyclic laws, tabulated backbones and damage-plasticity formulations.
Viscous and rheological models depend on strain rate and require an element that passes it to the material.
Damage and degradation models reduce the secant stiffness or strength as a history variable evolves.
Wrappers combine or transform other materials without adding a new constitutive law, as described in the [`Customisation`](Guide/Customisation.md) guide.

## Choosing a Model

Start from the physics of the problem and the data available for calibration rather than from the number of parameters.
If the response is rate independent, prefer a hysteretic or plasticity model and combine several laws with the `Parallel` wrapper when different mechanisms act at the same time.
If creep, relaxation or velocity-dependent forces are important, use a dashpot or a spring-dashpot rheology from the viscosity family.
For concrete under reversed cyclic loading, compare the rule-based [`ConcreteCM`](Material1D/Concrete/ConcreteCM.md) with the damage-plasticity [`ConcreteK4`](Material1D/Concrete/ConcreteK4.md).
For energy-based softening, [`ConcreteExp`](Material1D/Concrete/ConcreteExp.md) and [`ConcreteTable`](Material1D/Concrete/ConcreteTable.md) give energy-based or measured backbones.
Check that the chosen element supplies every quantity the material needs, since dashpots reject a strain-only update.
Use [`Substepping`](Wrapper/Substepping.md) when a return mapping converges only for small increments.

## Conventions

A material returns stress, tangent stiffness and, where applicable, tangent damping to the element.
History variables are stored separately in a trial and a committed state so that a failed iteration can be rolled back.
The density stored by a material is used for mass and inertia calculations and defaults to zero unless specified.
The characteristic length defaults to unity and is normally set by the element, which matters for objective damage laws.

!!! info "deviation from theory"
    The characteristic length defaults to unity, so an objective damage law is only mesh objective when the element overwrites this value.

!!! note "developer note"
    The characteristic length is stored by the material base class.
