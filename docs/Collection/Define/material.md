# material

The `material` command is used to construct a material prototype. Each prototype needs a unique tag. During the
initialization procedure, all valid elements will request a copy of associated material prototype for local use via the
problem domain.

Density is treated as a material property so in order to define consistent mass, often a proper density shall be
assigned in the definition of the material prototypes. Most material models has density as the final optional input
argument.

Please refer to the specific type of materials for details.

It shall be noted that some material models support initial conditions. In order to define initial conditions for the
specific material model, please use the [`initial`](initial.md) command. Please note the initial conditions are defined
in the material prototype, so it is necessary to define several material models if different initial conditions are
required.