# Introduction

This repository contains the official user documentation for [suanPan](https://tlcfem.github.io/suanPan/).
For an optimized reading experience, users browsing this GitHub repository are encouraged to visit the web-based [documentation](https://tlcfem.github.io/suanPan-manual/latest/).

As an alternative, a continuously updated version is hosted on [gitbook](https://tlcfem.gitbook.io/suanpan-manual/).
Note, however, that certain dynamically generated components may be absent in the GitBook version due to platform limitations regarding Jupyter Notebook conversions.

This documentation remains under active development.
Users are invited to submit issues via GitHub to report gaps in information or seek clarification.

## Motivation and Core Advantages

The development of [suanPan](https://tlcfem.github.io/suanPan/) is driven by two critical architectural requirements: **flexibility** and **high performance**.

While commercial finite element analysis (FEA) software packages offer robust capabilities, they are often constrained by prohibitive licensing costs, limiting access for individual researchers and smaller institutions.
Furthermore, implementing novel constitutive models or element formulations in traditional commercial environments (e.g., via C/Fortran user subroutines) is frequently hindered by legacy programming constraints and laborious tensor algebra implementations.
Conversely, many open-source alternatives are tailored to narrow domains or lack comprehensive multi-dimensional modelling capabilities.
For instance, packages like `OpenSEES` primarily optimize for uniaxial frame structures, offering limited support for complex 2D and 3D continuum mechanics.

[suanPan](https://tlcfem.github.io/suanPan/) addresses these challenges by integrating cutting-edge research into a unified, high-performance platform.
The framework provides an extensive, multi-domain library comprising:

1. **Advanced Element Formulations:** A comprehensive suite of 1D, 2D, and 3D elements incorporating modern finite element techniques;
2. **Constitutive Models:** High-fidelity uniaxial and multiaxial nonlinear material models for metals, concrete, timber, geomaterials, etc.;
3. **Advanced Numerical Solvers:** State-of-the-art solution routines and modern time-integration schemes;
4. **Extended Domain Capabilities:** Additional specialized modelling features.

To maximize computational efficiency, [suanPan](https://tlcfem.github.io/suanPan/) natively exploits modern multi-core processor architectures with ***hybrid parallelization***.
Key pipeline operations, including element/material state determination, global matrix assembly, and constraint enforcement, are fully parallelized.
Consequently, the framework systematically outperforms conventional single-threaded or distributed-memory MPI-based packages on modern workstation hardware.

Built on **modern C++** and powered by the `Armadillo` linear algebra library, [suanPan](https://tlcfem.github.io/suanPan/) offers an expressive API where core structural code closely mirrors the underlying mathematical expressions.
This significantly lowers the barrier to entry for researchers implementing and validating novel computational mechanics theories.

## Getting Started

The input file logic in [suanPan](https://tlcfem.github.io/suanPan/) shares syntax paradigms with `ABAQUS`, enabling users familiar with commercial software to transition efficiently.

To establish a baseline understanding, users should review the initial demonstration in [Analyze](Basic/Analyze.md), followed by the foundational architectural overviews in [Syntax](Basic/Syntax.md) and [Structure](Basic/Structure.md).

For practical applications, the `Example` section offers a tiered learning path ranging from introductory benchmarks to complex simulations.
Recommended entry points include:

* [>Linear Analysis of A Truss Roof<](Example/Structural/Statics/truss-roof.md)
* [>Dynamic Analysis of A Portal Frame<](Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md)

Detailed command syntaxes and programmatic entities are catalogued across the `Collection` and `Library` sections.
To streamline workflow productivity, a dedicated VS Code [extension](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan) is available, providing syntax highlighting and auto-completion capabilities.

Additionally, the comprehensive test suite in the repository's [Example](https://github.com/TLCFEM/suanPan/tree/dev/Example) directory provides an exhaustive reference of validated input configurations.

## Documentation Architecture

A comprehensive overview of the manual is available via the [table of contents](SUMMARY.md).
For insights into the software's underlying software engineering paradigms and system architecture, please refer to the technical [slides](ARCH.pdf).

## Collaborative Contribution

Contributions to the [suanPan](https://tlcfem.github.io/suanPan/) ecosystem are highly encouraged.
Feature requests or inquiries regarding the implementation of specific elements or material models can be directed to the core development team.

Documentation improvements, including errata and clarifications, should be submitted as pull requests or tracking issues.
Documentation contributions for third-party libraries must consist of a self-contained markdown file outlining usage guidelines and relevant theoretical foundations.
Detailed instructions for local compilation of this manual are provided in [Build](Basic/Build.md).

## Citation

If [suanPan](https://tlcfem.github.io/suanPan/) facilitates or supports your research publications, please cite the framework via its registered DOI at [10.5281/zenodo.1285221](https://doi.org/10.5281/zenodo.1285221), selecting the version appropriate to your work.
