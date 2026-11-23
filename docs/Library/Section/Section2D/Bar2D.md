# Bar2D

2D Reinforcing Bar Section

![arrangement](PIC/Cell.svg)

## Background

`Bar2D` is an alias of `Cell2D`, both names are parsed into the same section class and behave identically.
Each instance represents one reinforcing bar (or any small cell) with a given area, a one-dimensional material and a location along the transverse axis.
It stores one integration point, so the strain in the bar is evaluated at its own eccentricity relative to the section reference axis and its contribution is assembled by a parent fibre section such as `Fibre2D`.
The linear density of the bar is its area times the material density.

## Syntax

```text title="Bar2D"
section Bar2D (1) (2) (3) [4]
# (1) int, unique section tag
# (2) double, area
# (3) int, material tag
# [4] double, eccentricity/location, default: 0.0
```

## Remarks

The fourth argument gives the location of the bar relative to the section reference axis, internally the sign is flipped and stored as eccentricity, see [Eccentricity](../Eccentricity.md) for the convention.
`Cell2D` is interchangeable with `Bar2D`, the names only indicate whether the cell is regarded as a reinforcing bar or a generic part of the section.

## Example

Two symmetric reinforcing bars are combined with a concrete cell as follows, adapted from `Example/Section/Fibre2D.supan`.

```text
material ConcreteTsai 1 3E4 30. 2. 2. 2. .2 2E-3 1E-4
material MPF 2 2E5 400 .01
section Rectangle2D 2 300 500 1 9
section Bar2D 3 1200 2 230
section Bar2D 4 1200 2 -230
section Fibre2D 1 2 3 4
```
