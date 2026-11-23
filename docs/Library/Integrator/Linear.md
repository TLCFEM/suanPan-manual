# Linear

A `Linear` integrator basically does nothing and is used as the default integrator in static analysis.

If no integrator is defined in a step, a linear one will automatically be created and used.

## Background

`Linear` is the plain [`Integrator`](Overview.md) base class rather than a separately registered dynamic integrator.
It adds no damping or inertia to the equation of motion, so the resistance is simply the stiffness times the displacement.
A [`Static`](../Step/Static.md) step always uses this integrator.
