# MassPoint

The `MassPoint` element is used to represent a mass point with translational mass and optional rotational inertia.

## Syntax

```text
element MassPoint2D (1) (2) (3) [4]
element MassPoint3D (1) (2) (3) [4]
# (1) int, unique element tag
# (2) int, node tag
# (3) double, translational mass magnitude
# [4] double, optional, rotational inertia magnitude
```

## Remarks

1. For 2D elements, `DOF::UX` and `DOF::UY` are assigned with the translational mass (equal magnitude), `DOF::URZ` 
   is assigned with the rotational inertia (optional).
2. For 3D elements, `DOF::UX`, `DOF::UY`, and `DOF::UZ` are assigned with the translational mass (equal magnitude), 
   `DOF::URX`, `DOF::URY`, and `DOF::URZ` are assigned with the rotational inertia (optional).
3. `MassPoint` elements are an alternative to `Mass` elements, which are more abstract and allow more general 
   assignment of mass.
