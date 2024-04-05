# Introduction

This repository provides the user manual for [suanPan](https://tlcfem.github.io/suanPan/).
If you are browsing the GitHub repository,
please visit [https://tlcfem.github.io/suanPan-manual/latest/](https://tlcfem.github.io/suanPan-manual/latest/)
for a better presentation.

The manual is also hosted on [https://tlcfem.gitbook.io/suanpan-manual/](https://tlcfem.gitbook.io/suanpan-manual/),
which always contains the latest version of the manual.
This serves as an alternative if the mkdocs theme is not preferred.

I'm still working on this site from time to time. Hence, it is unlikely to get a complete reference by solely checking
this site. For any potential doubts, please feel free to contact me.

## Why to use?

Commercial packages are great, but may be too expensive. Unless your organization has already purchased a licence, it
is not likely for individuals to get access to them. Developing new elements, materials, etc., is also not easy. Imaging
you are asked to write a 3D material model in Fortran, which is not a pleasant experience (at least for me).

Existing open source packages often focus on specific areas, such as heat transfer, wave propagation, etc. Not many are
able to provide a wide range of elements, nonlinear material models, etc. [suanPan](https://tlcfem.github.io/suanPan/)
is striving to provide a platform to integrate latest research results into a single package. One can find many newly
proposed (within, say, the past one decade) elements, material models, time integration methods, etc., that are not
available in other packages but have been implemented in [suanPan](https://tlcfem.github.io/suanPan/).

Performance is another concern. [suanPan](https://tlcfem.github.io/suanPan/) is designed with high performance in mind.
Who doesn't want to get the results as soon as possible? If you are a researcher, it is also very convenient to
implement new ideas within the framework. For reference, I am able to implement a new uniaxial inelastic material model
within hours. If you have experience in developing new models in any language, you shall be able to do the same. The
architecture is continuously evolving to provide a hassle-free platform for researchers to implement new ideas.

## Where to start?

It is not easy to pick up a new finite element analysis tool, but it is not impossible.
The logic of input files resembles that of ABAQUS.
If you have some experience with ABAQUS, it shall be easy to create a simple model by hand.

After a simple demo presented in [Analyze](Basic/Analyze.md), you are recommended to check
out [Syntax](Basic/Syntax.md) and [Structure](Basic/Structure.md) to gain an overall picture of what an input file
would look like.

The `Example` section includes a number of examples with various degrees of complexity, check the ones you are familiar
with, or simple ones such as [Linear Analysis of A Truss Roof](Example/Structural/Statics/truss-roof.md)
and [Dynamic Analysis of A Portal Frame](Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md), as the
starting point.

The `Collection` section includes the top level commands used to develop finite element models.

The `Library` section contains all specific elements, materials, etc., that are available.

To develop a specific model, you may need to have this manual at hand to check the syntax of the corresponding commands.
You can also install the VS Code [extension](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan) to get
syntax highlighting and auto-completion.

You are also strongly recommended to check the [Example](https://github.com/TLCFEM/suanPan/tree/dev/Example) folder in
the source code repository. As those examples are used to provide coverage report, almost all commands are used in those
examples. You shall be able to have a better understanding of the syntax by checking those examples.

## Summary

Here is a complete [table of contents](SUMMARY.md). If you are interested in the architecture of the program, you can
check the [slides](ARCH.pdf) I prepared for a talk.

## About

Many FEM packages are available out there, so why another package?
Commercial packages are great, but may be too expensive for individuals to get access to.
The limited extensibility is another pain in the butt.
Modern programming paradigms for parallel computing have evolved a lot in recent years.
C++ itself has also received a huge number of updates starting from `C++11`.
`suanPan` is basically a practice of modern parallel computing with brand-new language features.
The civil/structural community also needs an update of new tools for efficient numerical analysis.
`suanPan` is designed to offer a concise but highly extensible framework for finite element analysis.
With the assist of `Armadillo`, the syntax of which is expressive, researchers can try out new ideas easily.

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
