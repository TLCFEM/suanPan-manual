# Amplitude

The `Amplitude` class holds arbitrary functions (of time) and provides magnitudes of anything that changes with time,
such as load and constraint. The concept is identical to that of the amplitude in ABAQUS.

There are a few universal patterns. Special databases, such as New Zealand ground motion database, are also implemented.

* Universal
  - [Constant](Universal/Constant.md)
  - [Linear/Ramp](Universal/Linear.md)
  - [Cosine/Sine](Universal/Trig.md)
  - [Modulated](Universal/Modulated.md)
  - [Decay](Universal/Decay.md)
  - [Tabular](Universal/Tabular.md)
  - [Combine](Universal/Combine.md)
* Special
  - [NZ Strong Motion](Special/NZStrongMotion.md)