# Introduction

This repository provides the user manual for [suanPan](https://tlcfem.github.io/suanPan/).
If you are browsing the GitHub repository,
please visit [documentation](https://tlcfem.github.io/suanPan-manual/latest/)
for a better presentation.

The manual is also hosted on [gitbook](https://tlcfem.gitbook.io/suanpan-manual/),
which always contains the latest version.
This serves as an alternative if the `mkdocs` theme is not preferred.
Since `gitbook` does not allow conversion of jupyter notebook, some dynamically generated contents will be missing.

I'm still working on this site from time to time.
Some information may still be missing.
For any potential doubts, please feel free to create issues.

## Why to use?

In short, two points: **flexibility** and **performance**.

Commercial packages are powerful, I personally have used `ABAQUS` and `ANSYS` extensively, and tried a few others.
With the trend of SaaS, those commercial packages may charge thousands per month/year.
It is probably too expensive.
Unless your organization has already purchased a licence, it is not likely for individuals to get access to them.
Developing new elements, materials, etc., is also not easy, due to various limitations, including ones from the programming language itself.
Imaging writing a 3D material model in C/Fortran, since it involves heavy tensor algebra, the implementation must be laborious and hard to maintain.
It is not going to be a pleasant experience (at least for me).

Existing open source packages often focus on specific domains, such as heat transfer, wave propagation, etc.
Not many provide a wide collection of elements of different types, nonlinear material models, time integration methods, etc.
For example, `OpenSees` is mainly a uniaxial package with frame elements and uniaxial material models, its 2D/3D capability is limited.

[suanPan](https://tlcfem.github.io/suanPan/) is striving to integrate the latest research into a universal platform.
It aims to provide a wide collection of

1. elements, including common 1D/2D/3D elements with modern element techniques;
2. materials, including advanced uniaxial and 3D nonlinear material models for metals, concrete, timber, geomaterials, etc.;
3. advanced solving techniques and modern time integration methods;
4. and many more.

[suanPan](https://tlcfem.github.io/suanPan/) also fully utilise the multicore architecture of today's PCs.
From element/material state determination to global matrix assembly and handling of constraints, almost all parts of FEA are parallelised, meaning the computational capacity provided by the hardware is fully used.
For the same analysis task, it is typically faster than other single-threaded or MPI based packages.

[suanPan](https://tlcfem.github.io/suanPan/) is written in **modern** CPP, with the assist of the fabulous `Armadillo` library, which offers full linear algebra support.
For developers/researchers, it is relatively easy to implement new elements, materials, etc., and try out new ideas since the core implementation would be very expressive and highly resembles the corresponding mathematics expressions.

## Where to start?

It is not easy to pick up a new finite element analysis tool, but it is not impossible.
The logic of input files resembles that of `ABAQUS`.
If you have some experience with `ABAQUS`, it shall be easy to create a simple model by hand.

After a simple demo presented in [Analyze](Basic/Analyze.md), you are recommended to check
out [Syntax](Basic/Syntax.md) and [Structure](Basic/Structure.md) to gain an overall picture of what an input file
would look like.

The `Example` section includes a number of examples with various degrees of complexity, check the ones you are familiar
with, or simple ones such as [>Linear Analysis of A Truss Roof<](Example/Structural/Statics/truss-roof.md)
and [>Dynamic Analysis of A Portal Frame<](Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md), as the
starting point.

The `Collection` section includes the top level commands used to develop finite element models.

The `Library` section contains all specific elements, materials, etc., that are available.

To develop a specific model, you may need to have this manual at hand to check the syntax of the corresponding commands.
You can also install the VS Code [extension](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan) to get
syntax highlighting and auto-completion.

You are also strongly recommended to check the [Example](https://github.com/TLCFEM/suanPan/tree/dev/Example) folder in the source code repository.
As those examples are used to provide coverage report, almost all commands are used in those examples.
You shall be able to have a better understanding of the syntax by checking those examples.

## Summary

Here is a complete [table of contents](SUMMARY.md). If you are interested in the architecture of the program, you can
check the [slides](ARCH.pdf) I prepared for a talk.

## Contribution

You are very welcome to contribute to the application. Please feel free to create feature requests or directly contact
me if you wish to have a new element, material model, etc., implemented.

To contribute to this manual, please create pull requests. Besides, if you find any typos, please also feel free to
create issues.

All third party libraries must provide a single markdown file to explain how to use the library and if possible with
some theories.

It may be convenient to build the manual locally, please check [Build](Basic/Build.md) for more details.

## Citation

If `suanPan` has offered some convenience to your research work, please consider
visiting [10.5281/zenodo.1285221](https://doi.org/10.5281/zenodo.1285221) and citing any version appropriate.
