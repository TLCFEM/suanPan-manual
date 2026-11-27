"""
section_optimizer.py

Match target section properties by scaling a chosen set of dimensions.
Properties include area, moments of inertia (Ix, Iy) and plastic section
moduli (Zx, Zy). By default only thicknesses are scaled, and dimensions with
the same original value are linked so symmetric sections keep their shape.
Every scaled dimension stays within +/-5 % of its original value.

Requires:
    pip install numpy scipy
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from scipy.optimize import Bounds, OptimizeResult, least_squares, minimize

MARGIN = 0.05  # default maximum relative change of a design variable

# A rectangle dimension: a number, a parameter name, or a callable on the
# parameter dict (for offsets such as t_bot + h_web).
Datum = float | str | Callable[[Mapping[str, float]], float]


def _datum(value: Datum, p: Mapping[str, float]) -> float:
    if callable(value):
        return float(value(p))
    return p[value] if isinstance(value, str) else float(value)


def _abs_first_moment(lo: float, hi: float, cut: float) -> float:
    """Integral of |t - cut| from lo to hi."""
    if cut <= lo:
        return (hi**2 - lo**2) / 2 - cut * (hi - lo)
    if cut >= hi:
        return cut * (hi - lo) - (hi**2 - lo**2) / 2
    return ((cut - lo) ** 2 + (hi - cut) ** 2) / 2


def _equal_area_axis(
    intervals: Sequence[tuple[float, float, float]], total_area: float
) -> float:
    """Axis that splits an area into equal halves.

    Each interval is (lo, hi, breadth), where breadth is the extent in the
    perpendicular direction.
    """
    edges = sorted({edge for lo, hi, _ in intervals for edge in (lo, hi)})
    half = total_area / 2
    area = 0.0
    for lo, hi in itertools.pairwise(edges):
        breadth = sum(w for a, b, w in intervals if a <= lo and b >= hi)
        if breadth > 0.0 and area + breadth * (hi - lo) >= half:
            return lo + (half - area) / breadth
        area += breadth * (hi - lo)
    return edges[-1]


# ---------------------------------------------------------------------------
# Generic section interface
# ---------------------------------------------------------------------------


class SectionModel(Protocol):
    """
    A section type only needs to expose its parameter names, its thickness
    parameters (the default design variables), properties(x), and optional
    geometric inequalities(x) >= 0.
    """

    parameter_names: Sequence[str]
    thickness_parameters: Sequence[str]

    def properties(self, x: np.ndarray) -> dict[str, float]: ...

    def inequalities(self, x: np.ndarray) -> np.ndarray: ...


# ---------------------------------------------------------------------------
# Sections built from rectangles: I, T, box, angle, channel, ...
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rect:
    """Axis-aligned rectangle; strings refer to parameter names."""

    b: Datum
    h: Datum
    x: Datum = 0.0
    y: Datum = 0.0


@dataclass(frozen=True)
class RectSection:
    """A section of rectangles; reports Ix/Iy and plastic moduli Zx/Zy."""

    parameter_names: Sequence[str]
    blocks: Sequence[Rect]
    thickness_parameters: Sequence[str] = ()
    constraints: Sequence[Callable[[Mapping[str, float]], float]] = ()

    def properties(self, x: np.ndarray) -> dict[str, float]:
        p = dict(zip(self.parameter_names, x))
        parts = []
        for r in self.blocks:
            b, h = _datum(r.b, p), _datum(r.h, p)
            x0, y0 = _datum(r.x, p), _datum(r.y, p)
            a = b * h
            parts.append(
                (
                    a,
                    x0 + b / 2,
                    y0 + h / 2,
                    b * h**3 / 12,
                    h * b**3 / 12,
                    x0,
                    x0 + b,
                    y0,
                    y0 + h,
                )
            )

        A = sum(q[0] for q in parts)
        cx = sum(q[0] * q[1] for q in parts) / A
        cy = sum(q[0] * q[2] for q in parts) / A

        # Plastic section moduli use the equal-area axes, which coincide with
        # the centroidal axes only for symmetric sections.
        yp = _equal_area_axis([(q[7], q[8], q[6] - q[5]) for q in parts], A)
        xp = _equal_area_axis([(q[5], q[6], q[8] - q[7]) for q in parts], A)
        Zx = sum((q[6] - q[5]) * _abs_first_moment(q[7], q[8], yp) for q in parts)
        Zy = sum((q[8] - q[7]) * _abs_first_moment(q[5], q[6], xp) for q in parts)

        return {
            "area": float(A),
            "Ix": float(sum(q[3] + q[0] * (q[2] - cy) ** 2 for q in parts)),
            "Iy": float(sum(q[4] + q[0] * (q[1] - cx) ** 2 for q in parts)),
            "Zx": float(Zx),
            "Zy": float(Zy),
            "x_centroid": float(cx),
            "y_centroid": float(cy),
            "width": float(max(q[6] for q in parts) - min(q[5] for q in parts)),
            "depth": float(max(q[8] for q in parts) - min(q[7] for q in parts)),
        }

    def inequalities(self, x: np.ndarray) -> np.ndarray:
        p = dict(zip(self.parameter_names, x))
        return np.array([g(p) for g in self.constraints], dtype=float)


@dataclass(frozen=True)
class CircleSection:
    """
    Solid circle of diameter d.

    For a tube, use e.g. CircleSection(("d", "t"), ("t",)) to add the wall
    thickness parameter and use it as the default design variable.
    """

    parameter_names: Sequence[str] = ("d",)
    thickness_parameters: Sequence[str] = ("d",)

    def properties(self, x: np.ndarray) -> dict[str, float]:
        d = x[0]
        di = d - 2.0 * x[1] if len(x) > 1 else 0.0
        area = np.pi * (d**2 - di**2) / 4.0
        I = np.pi * (d**4 - di**4) / 64.0
        Z = (d**3 - di**3) / 6.0
        return {
            "area": float(area),
            "Ix": float(I),
            "Iy": float(I),
            "Zx": float(Z),
            "Zy": float(Z),
            "diameter": float(d),
        }

    def inequalities(self, x: np.ndarray) -> np.ndarray:
        return np.array([x[0] - 2.0 * x[1]]) if len(x) > 1 else np.empty(0)


# Ready-made sections. Custom sections can be assembled the same way.
I_SECTION = RectSection(
    ("b_top", "t_top", "b_bot", "t_bot", "h_web", "t_web"),
    (
        Rect("b_bot", "t_bot", x=lambda p: -p["b_bot"] / 2),
        Rect("t_web", "h_web", x=lambda p: -p["t_web"] / 2, y="t_bot"),
        Rect(
            "b_top",
            "t_top",
            x=lambda p: -p["b_top"] / 2,
            y=lambda p: p["t_bot"] + p["h_web"],
        ),
    ),
    thickness_parameters=("t_top", "t_bot", "t_web"),
    constraints=(lambda p: p["b_top"] - p["t_web"], lambda p: p["b_bot"] - p["t_web"]),
)

# H-section: an I-section rotated 90 degrees (left/right flanges plus web).
H_SECTION = RectSection(
    ("h_left", "t_left", "h_right", "t_right", "b_web", "t_web"),
    (
        Rect(
            "t_left",
            "h_left",
            x=lambda p: -p["b_web"] / 2 - p["t_left"],
            y=lambda p: -p["h_left"] / 2,
        ),
        Rect(
            "t_right",
            "h_right",
            x=lambda p: p["b_web"] / 2,
            y=lambda p: -p["h_right"] / 2,
        ),
        Rect(
            "b_web", "t_web", x=lambda p: -p["b_web"] / 2, y=lambda p: -p["t_web"] / 2
        ),
    ),
    thickness_parameters=("t_left", "t_right", "t_web"),
    constraints=(
        lambda p: p["h_left"] - p["t_web"],
        lambda p: p["h_right"] - p["t_web"],
    ),
)

T_SECTION = RectSection(
    ("b", "t_flange", "h_web", "t_web"),
    (
        Rect("t_web", "h_web", x=lambda p: -p["t_web"] / 2),
        Rect("b", "t_flange", x=lambda p: -p["b"] / 2, y="h_web"),
    ),
    thickness_parameters=("t_flange", "t_web"),
    constraints=(lambda p: p["b"] - p["t_web"],),
)

BOX_SECTION = RectSection(
    ("b", "h", "t"),
    (
        Rect("b", "t"),
        Rect("b", "t", y=lambda p: p["h"] - p["t"]),
        Rect("t", lambda p: p["h"] - 2 * p["t"], y="t"),
        Rect("t", lambda p: p["h"] - 2 * p["t"], x=lambda p: p["b"] - p["t"], y="t"),
    ),
    thickness_parameters=("t",),
    constraints=(lambda p: p["b"] - 2 * p["t"], lambda p: p["h"] - 2 * p["t"]),
)


# ---------------------------------------------------------------------------
# Optimizer
# ---------------------------------------------------------------------------


@dataclass
class OptimizationResult:
    dimensions: dict[str, float]
    properties: dict[str, float]
    target_properties: dict[str, float]
    relative_property_errors: dict[str, float]
    normalized_dimension_changes: dict[str, float]
    linked_groups: list[tuple[str, ...]]
    scipy_result: OptimizeResult
    mode_used: str


def _linked_groups(
    names: Sequence[str],
    values: Sequence[float],
    groups: Sequence[Sequence[str]] | None,
) -> list[tuple[int, ...]]:
    """Group variable positions that share one scale factor.

    Without explicit groups, variables with identical original values are
    linked. This keeps equal flanges equal and keeps a square box square.
    """
    index = {name: i for i, name in enumerate(names)}
    if groups is not None:
        linked = [tuple(index[n] for n in group) for group in groups]
        used = {i for group in linked for i in group}
        return linked + [(i,) for i in range(len(names)) if i not in used]

    buckets: dict[float, list[int]] = {}
    for i, value in enumerate(values):
        buckets.setdefault(float(value), []).append(i)
    return [tuple(group) for group in buckets.values()]


def optimize_section(
    section: SectionModel,
    original_dimensions: Sequence[float],
    target_properties: Mapping[str, float],
    *,
    mode: str = "exact",
    variables: Sequence[str] | None = None,
    groups: Sequence[Sequence[str]] | None = None,
    dimension_weights: Mapping[str, float] | None = None,
    property_weights: Mapping[str, float] | None = None,
    margin: float = MARGIN,
    soft_property_priority: float = 1.0e6,
    maxiter: int = 3000,
    feasibility_tolerance: float = 1.0e-8,
) -> OptimizationResult:
    """
    Optimize a section geometry.

    Parameters
    ----------
    section:
        A SectionModel, such as I_SECTION, H_SECTION, T_SECTION,
        BOX_SECTION or CircleSection(). Custom shapes can be built with
        RectSection.

    original_dimensions:
        Initial dimensions in the order of section.parameter_names.

    target_properties:
        Property values to match, e.g.
        {"area": 25000.0, "Ix": 8.0e8, "Zx": 2.0e6}. Plastic section moduli
        are available as "Zx" and "Zy".

    mode:
        "exact" solves the target properties with a bounded least-squares
        feasibility step and returns only when the match is within
        feasibility_tolerance. If the selected variables cannot represent
        the targets within the bounds, it falls back to "soft", which returns
        the best achievable least-squares property match. Supplying more
        variables (e.g. widths as well as thicknesses) makes more target sets
        exactly representable.

        "soft" directly minimizes weighted target error instead.

    variables:
        Names of the dimensions allowed to change. Defaults to
        section.thickness_parameters, i.e. widths and heights stay fixed.

    groups:
        Dimensions that must share one scale factor, e.g.
        [("b", "h")]. By default all variables with equal original values
        are linked, so equal flanges move together and boxes stay boxes.

    dimension_weights, property_weights:
        Optional relative weights keyed by dimension/property name.

    soft_property_priority:
        How strongly soft mode favours matching targets over keeping the
        original dimensions.

    margin:
        Allowed relative change of each design variable (default 5 %,
        i.e. bounds 0.95 to 1.05 of the original value).

    feasibility_tolerance:
        Maximum relative property error accepted as an exact match.
    """
    names = list(section.parameter_names)
    x0 = np.asarray(original_dimensions, dtype=float)

    if len(names) != len(x0):
        raise ValueError("original_dimensions must match parameter_names.")
    if np.any(x0 <= 0.0):
        raise ValueError("All original dimensions must be positive.")
    if not 0.0 < margin < 1.0:
        raise ValueError("margin must lie between 0 and 1.")

    chosen = list(variables or section.thickness_parameters or names)
    if not chosen or any(name not in names for name in chosen):
        raise ValueError(f"variables must be chosen from {names}.")

    design = [names.index(name) for name in chosen]
    links = _linked_groups(chosen, x0[design], groups)
    group_of = {i: g for g, group in enumerate(links) for i in group}

    property_names = list(target_properties)
    targets = np.array([target_properties[p] for p in property_names], dtype=float)
    if np.any(~np.isfinite(targets)):
        raise ValueError("Target properties must be finite.")

    original_props = section.properties(x0)
    level = np.array(
        [
            max(abs(t), abs(original_props[p]), 1.0)
            for p, t in zip(property_names, targets)
        ]
    )

    def expand(z: np.ndarray) -> np.ndarray:
        """Apply one scale factor per linked group; fixed dimensions stay put."""
        x = x0.copy()
        for pos, j in enumerate(design):
            x[j] = x0[j] * z[group_of[pos]]
        return x

    def residual(z: np.ndarray) -> np.ndarray:
        props = section.properties(expand(z))
        return (np.array([props[p] for p in property_names]) - targets) / level

    dw = np.array(
        [
            1.0 if dimension_weights is None else dimension_weights.get(n, 1.0)
            for n in chosen
        ]
    )
    pw = np.array(
        [
            1.0 if property_weights is None else property_weights.get(p, 1.0)
            for p in property_names
        ]
    )
    if np.any(dw <= 0.0) or np.any(pw <= 0.0):
        raise ValueError("Weights must be positive.")

    def geometry_objective(z: np.ndarray) -> float:
        dz = z - 1.0
        return float(sum(w * dz[group_of[pos]] ** 2 for pos, w in enumerate(dw)))

    def soft_objective(z: np.ndarray) -> float:
        # Normalized by the property priority so the solver sees an O(1)
        # objective; a huge raw weight destabilizes SLSQP's finite differences.
        return float(
            np.sum(pw * residual(z) ** 2)
            + geometry_objective(z) / soft_property_priority
        )

    def inequalities(z: np.ndarray) -> np.ndarray:
        return np.asarray(section.inequalities(expand(z)), dtype=float)

    constraints = (
        [{"type": "ineq", "fun": inequalities}] if len(section.inequalities(x0)) else []
    )

    n_groups = len(links)
    lb = np.full(n_groups, 1.0 - margin)
    ub = np.full(n_groups, 1.0 + margin)
    bounds = Bounds(lb, ub)

    def solve(fun, cons, z0):
        return minimize(
            fun=fun,
            x0=z0,
            method="SLSQP",
            bounds=bounds,
            constraints=cons,
            options={"maxiter": maxiter, "ftol": 1.0e-12, "disp": False},
        )

    def fit(weights: np.ndarray | None = None):
        """
        Least-squares match of the property residual.

        This is much more accurate than SLSQP equality constraints, especially
        when there are more target properties than design variables and the
        targets are consistent but the constraint system is redundant.
        """
        fun = (
            residual if weights is None else (lambda z: np.sqrt(weights) * residual(z))
        )
        return least_squares(
            fun,
            np.ones(n_groups),
            bounds=(lb, ub),
            method="dogbox",
            xtol=1.0e-14,
            ftol=1.0e-14,
            gtol=1.0e-14,
            max_nfev=maxiter,
        )

    def properties_ok(z: np.ndarray) -> bool:
        return np.max(np.abs(residual(z))) <= feasibility_tolerance

    def geometry_ok(z: np.ndarray) -> bool:
        return np.all(section.inequalities(expand(z)) >= -feasibility_tolerance)

    mode_used = mode.lower()
    if mode_used not in ("exact", "soft"):
        raise ValueError("mode must be either 'exact' or 'soft'.")

    if mode_used == "exact":
        result = fit()
        if properties_ok(result.x):
            # Use any remaining freedom to minimize geometry change while
            # keeping the exact property match.
            refined = solve(
                geometry_objective,
                constraints + [{"type": "eq", "fun": residual}],
                result.x,
            )
            if (
                refined.success
                and properties_ok(refined.x)
                and geometry_ok(refined.x)
                and geometry_objective(refined.x) <= geometry_objective(result.x)
            ):
                result = refined
            elif not geometry_ok(result.x):
                result = None
        else:
            result = None

        # Only fall back when the targets are truly infeasible within the
        # selected variables, groups, and bounds.
        if result is None:
            mode_used = "soft_fallback"
            result = solve(soft_objective, constraints, fit(pw).x)
            if not result.success or not geometry_ok(result.x):
                result = solve(soft_objective, constraints, np.ones(n_groups))
    else:
        result = solve(soft_objective, constraints, fit(pw).x)
        if not result.success or not geometry_ok(result.x):
            result = solve(soft_objective, constraints, np.ones(n_groups))

    x_opt = expand(result.x)
    props_opt = section.properties(x_opt)

    return OptimizationResult(
        dimensions=dict(zip(names, x_opt)),
        properties=props_opt,
        target_properties=dict(target_properties),
        relative_property_errors={
            p: float((props_opt[p] - target_properties[p]) / level[i])
            for i, p in enumerate(property_names)
        },
        normalized_dimension_changes={
            name: (x_opt[i] - x0[i]) / x0[i] for i, name in enumerate(names)
        },
        linked_groups=[tuple(chosen[i] for i in group) for group in links],
        scipy_result=result,
        mode_used=mode_used,
    )


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------


def _demo(section: SectionModel, x0: Sequence[float], factor: float = 1.03) -> None:
    """Recover a target produced by scaling every thickness by factor."""
    names = list(section.parameter_names)
    x_target = np.asarray(x0, dtype=float).copy()
    for name in section.thickness_parameters:
        x_target[names.index(name)] *= factor
    props = section.properties(x_target)
    target = {name: props[name] for name in ("area", "Ix", "Iy", "Zx", "Zy")}
    result = optimize_section(section, x0, target)

    print(
        f"\n{type(section).__name__}: mode={result.mode_used}, "
        f"linked={result.linked_groups}"
    )
    for name, value in result.dimensions.items():
        change = 100.0 * result.normalized_dimension_changes[name]
        print(f"  {name:10s} = {value:10.5f} ({change:+6.2f} %)")
    for name, error in result.relative_property_errors.items():
        print(f"  {name:10s} error {100.0 * error:+8.4f} %")


if __name__ == "__main__":
    # Units may be mm, inches, metres, etc., but must be consistent.
    # The demo targets are reachable by thickness changes, so exact mode
    # should reproduce them to numerical precision.
    # If a target needs more freedom, pass e.g.
    # variables=I_SECTION.parameter_names to let widths and height change.
    _demo(I_SECTION, [4.000, 0.255, 4.000, 0.255, 7.480, 0.230])
    _demo(H_SECTION, [4.000, 0.255, 4.000, 0.255, 7.480, 0.230])
    _demo(T_SECTION, [4.000, 0.300, 5.000, 0.250])
    _demo(BOX_SECTION, [4.000, 4.000, 0.250])
    _demo(CircleSection(), [2.000])
