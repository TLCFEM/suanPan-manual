# Criterion

## Overview

A `Criterion` defines a conditional threshold based on specific model quantities.
Its primary function is to signal termination conditions for numerical simulations and computational workflows.

## Arc-Length Analysis

In a standard [`ArcLength`](../Step/ArcLength.md) analysis, load levels and displacement response are inherently unknown *a priori*.
A `Criterion` governs the solution path by evaluating current states against user-defined limits; once any target threshold is met, it issues an exit flag to terminate the step.

## Other Applications

Beyond path-following methods, a `Criterion` serves as an early-stopping mechanism in standard static/dynamic analyses and structural optimization routines.
