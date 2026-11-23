# Overview

This section introduces the fundamentals of using `suanPan`.
It follows a guided path from obtaining the application to running an analysis and, when necessary, compiling it from source.

## Features

`suanPan` is an open-source finite element simulation platform for solid mechanics and civil, structural and seismic engineering.
It is written in modern C++ and aims to provide an efficient, concise, flexible and reliable simulation environment.

Its main capabilities are summarised below.

| Area | Highlights |
|:-----|:-----------|
| Analysis | static, dynamic, arc-length, frequency, buckling and optimization steps |
| Elements | beams, trusses, membranes, plates, shells, 3D solids, contact, joints, mass and springs |
| Materials | elasticity, metal plasticity, concrete damage, orthotropic, hysteresis and user-defined models |
| Sections | structural, fibre, NM and code-based design sections |
| Constraints | MPC, rigid and restitution walls, embedding, node-line/facet and gap constraints |
| Integrators | implicit (Newmark, generalized-α, Bathe, GSSSS) and explicit (Bathe, Tchamwa, GSSE, WAT2) schemes |
| Parallelism | shared-memory (TBB), distributed-memory (MPI) and GPU acceleration (CUDA / MAGMA) |

A complete catalogue of commands and models is available in the [model library](../Library/Overview.md) and the [command collection](../Collection/Overview.md).

## Learning Path

1. [Obtain the Application](GettingStarted/Obtain.md) explains how to install or download a ready-to-run copy.
2. [Your First Analysis](GettingStarted/Analyze.md) walks through a complete model and shows the expected output.
3. [Model Syntax](GettingStarted/Syntax.md) describes the rules for writing commands.
4. [Model Structure](GettingStarted/Structure.md) explains how a model file is organised into setup, analysis and post-processing.
5. [Command-Line Configuration](Usage/Config.md) lists the available command-line options.
6. [Editor Setup](Usage/Editors.md) shows how to configure common editors for model files.
7. [Performance Tweaks](Usage/Performance.md) gives practical advice for faster analyses.
8. [Automation and System Integration](Usage/Automation.md) covers file associations and helper scripts.
9. [Compile the Application](Building/Compile.md) explains how to build `suanPan` from source.
10. [Build Options](Building/Options.md) documents the main CMake options.
11. [Build the Manual](Building/Build.md) explains how to build this documentation locally.

## Advanced Topics

The following pages describe the internal design and parallel execution model.
They are not required for everyday use.

* [Architecture Design](Advanced/Architecture.md)
* [Parallelism Mechanisms](Advanced/Parallelism.md)
* [Run on Clusters](Advanced/Cluster.md)
