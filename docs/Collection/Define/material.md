# material

The `material` command constructs a material prototype.
Each prototype requires a unique tag.
During the initialization procedure, all valid elements request a copy of the associated material prototype from the problem domain for local use.

Density is treated as a material property.
To define a consistent mass matrix, a proper density often needs to be assigned in the material prototype definition.
Most material models accept the density as the final optional argument.

Please refer to the specific material types for details.

Some material models support initial conditions.
To define initial conditions for a specific material model, use the [`initial`](initial.md) command.
The initial conditions are defined on the material prototype.
Thus, several material models must be defined if different initial conditions are required.
