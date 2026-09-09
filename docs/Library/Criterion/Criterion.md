# Criterion

!!! warning "activation"
    Each step can have multiple criteria, they shall be defined in each step block.
    The criteria defined before the first step is not activated by default.

    In the following example, the first `MaxHistory` criterion and the second `MinHistory` criterion are defined before the definition of the first step.
    If the third `LogicOR` criterion is not defined, no criterion will be used in the analysis.

    ```text
    # definitions of nodes and elements
    # ...

    criterion MaxHistory 1 S 300
    criterion MinHistory 2 S -500

    step static 1

    criterion LogicOR 3 1 2

    analyze

    exit
    ```

## Overview

A `Criterion` defines a conditional threshold based on specific model quantities.
Its primary function is to signal termination conditions for numerical simulations and computational workflows.

## Arc-Length Analysis

In a standard [`ArcLength`](../Step/ArcLength.md) analysis, load levels and displacement response are inherently unknown *a priori*.
A `Criterion` governs the solution path by evaluating current states against user-defined limits; once any target threshold is met, it issues an exit flag to terminate the step.

## Other Applications

Beyond path-following methods, a `Criterion` serves as an early-stopping mechanism in standard static/dynamic analyses and structural optimization routines.
