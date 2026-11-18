"""
section_optimizer.py

Requires:
    pip install numpy scipy
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from scipy.optimize import Bounds, OptimizeResult, minimize

# ---------------------------------------------------------------------------
# Generic interface for any section type
# ---------------------------------------------------------------------------


class SectionModel(Protocol):
    """
    Interface required by the optimizer.

    A new section type only needs to implement:
        - parameter_names
        - properties(x)
        - inequalities(x), optional but recommended
    """

    parameter_names: Sequence[str]

    def properties(self, x: np.ndarray) -> dict[str, float]:
        """
        Return section properties.

        Example:
            {
                "area": ...,
                "Ix": ...,
                "Iy": ...,
            }
        """
        ...

    def inequalities(self, x: np.ndarray) -> np.ndarray:
        """
        Return inequality constraint values g(x) such that g(x) >= 0.

        Return an empty array if there are no additional constraints.
        """
        ...


# ---------------------------------------------------------------------------
# I-section definition
# ---------------------------------------------------------------------------


@dataclass
class ISection:
    """
    Symmetric-about-vertical-axis I-section.

    Parameter order:
        0: b_top   = top flange width
        1: t_top   = top flange thickness
        2: b_bot   = bottom flange width
        3: t_bot   = bottom flange thickness
        4: h_web   = clear web height between flanges
        5: t_web   = web thickness

    Geometry convention:
        - Bottom of lower flange is y = 0.
        - Web is centered horizontally.
        - Web height excludes flange thicknesses.
        - Ix is the centroidal strong-axis moment of inertia.
        - Iy is the centroidal weak-axis moment of inertia.
    """

    parameter_names = (
        "b_top",
        "t_top",
        "b_bottom",
        "t_bottom",
        "h_web",
        "t_web",
    )

    def properties(self, x: np.ndarray) -> dict[str, float]:
        b_top, t_top, b_bot, t_bot, h_web, t_web = x

        # Rectangle areas
        A_top = b_top * t_top
        A_bot = b_bot * t_bot
        A_web = t_web * h_web
        A = A_top + A_bot + A_web

        # Centroid locations measured from bottom of section
        y_bot = t_bot / 2.0
        y_web = t_bot + h_web / 2.0
        y_top = t_bot + h_web + t_top / 2.0

        # Overall centroid location
        y_bar = (A_bot * y_bot + A_web * y_web + A_top * y_top) / A

        # Local strong-axis inertias of the three rectangles
        Ix_bot_local = b_bot * t_bot**3 / 12.0
        Ix_web_local = t_web * h_web**3 / 12.0
        Ix_top_local = b_top * t_top**3 / 12.0

        # Parallel-axis theorem for centroidal strong-axis inertia
        Ix = (
            Ix_bot_local
            + A_bot * (y_bot - y_bar) ** 2
            + Ix_web_local
            + A_web * (y_web - y_bar) ** 2
            + Ix_top_local
            + A_top * (y_top - y_bar) ** 2
        )

        # All three components are centered on the vertical centerline.
        # Therefore no parallel-axis term is needed for Iy.
        Iy = t_bot * b_bot**3 / 12.0 + h_web * t_web**3 / 12.0 + t_top * b_top**3 / 12.0

        return {
            "area": float(A),
            "Ix": float(Ix),
            "Iy": float(Iy),
            "y_centroid_from_bottom": float(y_bar),
            "depth": float(t_top + h_web + t_bot),
        }

    def inequalities(self, x: np.ndarray) -> np.ndarray:
        """
        Geometric constraints g(x) >= 0.

        The scalar bounds in the optimizer already require all dimensions
        to be positive. The two constraints below ensure that the web fits
        within both flange widths, producing a conventional I-section.
        """
        b_top, _, b_bot, _, _, t_web = x

        return np.array(
            [
                b_top - t_web,
                b_bot - t_web,
            ],
            dtype=float,
        )


# ---------------------------------------------------------------------------
# Optimization utilities
# ---------------------------------------------------------------------------


@dataclass
class OptimizationResult:
    dimensions: dict[str, float]
    properties: dict[str, float]
    target_properties: dict[str, float]
    relative_property_errors: dict[str, float]
    normalized_dimension_changes: dict[str, float]
    scipy_result: OptimizeResult
    mode_used: str


def optimize_section(
    section: SectionModel,
    original_dimensions: Sequence[float],
    target_properties: Mapping[str, float],
    *,
    mode: str = "exact",
    dimension_weights: Sequence[float] | None = None,
    property_weights: Mapping[str, float] | None = None,
    lower_bounds: Sequence[float] | None = None,
    upper_bounds: Sequence[float] | None = None,
    soft_property_priority: float = 1.0e6,
    maxiter: int = 3000,
    feasibility_tolerance: float = 1.0e-6,
) -> OptimizationResult:
    """
    Optimize a section geometry.

    Parameters
    ----------
    section:
        A SectionModel, such as ISection().

    original_dimensions:
        Initial geometry dimensions in the order defined by
        section.parameter_names.

    target_properties:
        Example:
            {
                "area": 25000.0,
                "Ix": 8.0e8,
                "Iy": 1.2e8,
            }

    mode:
        "exact":
            Enforce requested target properties as equality constraints and
            minimize normalized geometry changes.

            If the target cannot be matched, the solver automatically falls
            back to soft optimization.

        "soft":
            Minimize weighted property error plus geometry changes.

    dimension_weights:
        Relative importance of preserving each dimension.
        Larger value = less change allowed.

        Default: all dimensions weighted equally in relative terms.

    property_weights:
        Property-specific weights used in soft mode.
        Example:
            {"area": 1.0, "Ix": 2.0, "Iy": 2.0}

    lower_bounds, upper_bounds:
        Physical dimension bounds. Dimensions must have consistent units.

    soft_property_priority:
        Weight applied to property mismatch in soft mode. Increase this value
        if matching target properties is more important than preserving the
        original geometry.

    Returns
    -------
    OptimizationResult
    """

    x0 = np.asarray(original_dimensions, dtype=float)
    n = len(x0)

    if len(section.parameter_names) != n:
        raise ValueError(
            "original_dimensions length must match section.parameter_names."
        )

    if np.any(x0 <= 0.0):
        raise ValueError("All original dimensions must be positive.")

    property_names = list(target_properties.keys())
    targets = np.asarray([target_properties[p] for p in property_names], dtype=float)

    if np.any(~np.isfinite(targets)):
        raise ValueError("Target properties must be finite.")

    # Scale variables by their original values. This improves conditioning:
    # z = x / x0, so z = 1 represents the original geometry.
    x_scale = np.maximum(np.abs(x0), 1.0)

    if lower_bounds is None:
        lb = np.maximum(1.0e-9 * x_scale, 1.0e-12)
    else:
        lb = np.asarray(lower_bounds, dtype=float)

    if upper_bounds is None:
        ub = np.full(n, np.inf)
    else:
        ub = np.asarray(upper_bounds, dtype=float)

    if np.any(lb <= 0.0):
        raise ValueError("Lower bounds must be positive.")

    if np.any(ub <= lb):
        raise ValueError("Every upper bound must be greater than lower bound.")

    z0 = x0 / x_scale
    z_lb = lb / x_scale
    z_ub = ub / x_scale

    # Ensure starting point lies within scalar bounds.
    z0 = np.clip(z0, z_lb, z_ub)

    if dimension_weights is None:
        dimension_weights_array = np.ones(n)
    else:
        dimension_weights_array = np.asarray(dimension_weights, dtype=float)

    if len(dimension_weights_array) != n:
        raise ValueError("dimension_weights must have one value per dimension.")

    if np.any(dimension_weights_array <= 0.0):
        raise ValueError("dimension_weights must be positive.")

    if property_weights is None:
        property_weights_array = np.ones(len(property_names))
    else:
        property_weights_array = np.asarray(
            [property_weights.get(name, 1.0) for name in property_names],
            dtype=float,
        )

    if np.any(property_weights_array <= 0.0):
        raise ValueError("property_weights must be positive.")

    # Use target magnitude as normalizing scale. If a target is zero,
    # use the original property or 1.0 to avoid division by zero.
    original_props = section.properties(x0)
    property_scale = np.array(
        [
            max(abs(target_properties[name]), abs(original_props[name]), 1.0)
            for name in property_names
        ],
        dtype=float,
    )

    def physical_dimensions(z: np.ndarray) -> np.ndarray:
        return z * x_scale

    def property_residual(z: np.ndarray) -> np.ndarray:
        x = physical_dimensions(z)
        props = section.properties(x)
        values = np.asarray([props[name] for name in property_names])
        return (values - targets) / property_scale

    def dimension_change_objective(z: np.ndarray) -> float:
        """
        Squared normalized relative geometry change.

        z=1 means no change from original dimensions.
        """
        dz = z - 1.0
        return float(np.sum(dimension_weights_array * dz**2))

    def soft_objective(z: np.ndarray) -> float:
        """
        Weighted target mismatch + weighted geometry change.
        """
        rp = property_residual(z)

        property_error = np.sum(property_weights_array * rp**2)
        geometry_error = dimension_change_objective(z)

        return float(soft_property_priority * property_error + geometry_error)

    def geometric_inequalities(z: np.ndarray) -> np.ndarray:
        x = physical_dimensions(z)
        g = np.asarray(section.inequalities(x), dtype=float)

        # Empty constraints are acceptable to scipy.
        return g

    constraints = []

    # Add section-specific geometric constraints such as:
    # b_top >= t_web and b_bottom >= t_web.
    if len(section.inequalities(x0)) > 0:
        constraints.append(
            {
                "type": "ineq",
                "fun": geometric_inequalities,
            }
        )

    bounds = Bounds(z_lb, z_ub)

    # --------------------------------------------------------------
    # Exact mode: match target properties and minimize changes.
    # --------------------------------------------------------------
    result: OptimizeResult
    mode_used = mode

    if mode.lower() == "exact":
        exact_constraints = list(constraints)
        exact_constraints.append(
            {
                "type": "eq",
                "fun": property_residual,
            }
        )

        result = minimize(
            fun=dimension_change_objective,
            x0=z0,
            method="SLSQP",
            bounds=bounds,
            constraints=exact_constraints,
            options={
                "maxiter": maxiter,
                "ftol": 1.0e-12,
                "disp": False,
            },
        )

        # Verify that equality constraints really were met.
        max_property_error = np.max(np.abs(property_residual(result.x)))

        # If exact equality is infeasible, solve a prioritised soft problem.
        if (not result.success) or (max_property_error > feasibility_tolerance):
            mode_used = "soft_fallback"

            result = minimize(
                fun=soft_objective,
                x0=np.clip(result.x, z_lb, z_ub),
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={
                    "maxiter": maxiter,
                    "ftol": 1.0e-12,
                    "disp": False,
                },
            )

    elif mode.lower() == "soft":
        result = minimize(
            fun=soft_objective,
            x0=z0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={
                "maxiter": maxiter,
                "ftol": 1.0e-12,
                "disp": False,
            },
        )

    else:
        raise ValueError("mode must be either 'exact' or 'soft'.")

    # Convert optimized normalized variables back to physical dimensions.
    x_opt = physical_dimensions(result.x)
    props_opt = section.properties(x_opt)

    relative_errors = {}
    for name in property_names:
        scale = max(abs(target_properties[name]), 1.0)
        relative_errors[name] = (props_opt[name] - target_properties[name]) / scale

    normalized_changes = {
        name: (value - original) / max(abs(original), 1.0)
        for name, value, original in zip(section.parameter_names, x_opt, x0)
    }

    return OptimizationResult(
        dimensions=dict(zip(section.parameter_names, x_opt)),
        properties=props_opt,
        target_properties=dict(target_properties),
        relative_property_errors=relative_errors,
        normalized_dimension_changes=normalized_changes,
        scipy_result=result,
        mode_used=mode_used,
    )


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Units may be mm, inches, metres, etc., but must be consistent.
    # If dimensions are mm:
    #   area is mm^2
    #   Ix and Iy are mm^4

    original_i_section = np.array(
        [
            250.0,  # b_top
            18.0,  # t_top
            220.0,  # b_bottom
            22.0,  # t_bottom
            400.0,  # h_web
            12.0,  # t_web
        ]
    )

    target = {
        "area": 15500.0,
        "Ix": 4.80e8,
        "Iy": 3.20e7,
    }

    i_section = ISection()

    result = optimize_section(
        section=i_section,
        original_dimensions=original_i_section,
        target_properties=target,
        # Try to exactly match the target set.
        # Automatically falls back to soft optimization if infeasible.
        mode="exact",
        # Preserve flange thicknesses somewhat more strongly, for example.
        dimension_weights=[
            1.0,  # b_top
            3.0,  # t_top
            1.0,  # b_bottom
            3.0,  # t_bottom
            1.0,  # h_web
            2.0,  # t_web
        ],
        # Optional manufacturing/design limits:
        lower_bounds=[
            50.0,  # b_top
            4.0,  # t_top
            50.0,  # b_bottom
            4.0,  # t_bottom
            50.0,  # h_web
            3.0,  # t_web
        ],
        upper_bounds=[
            1000.0,
            100.0,
            1000.0,
            100.0,
            2000.0,
            100.0,
        ],
    )

    print("\nOptimization status:")
    print("  Success:", result.scipy_result.success)
    print("  Message:", result.scipy_result.message)
    print("  Mode used:", result.mode_used)

    print("\nOptimized dimensions:")
    for name, value in result.dimensions.items():
        print(f"  {name:12s} = {value:12.5f}")

    print("\nSection properties:")
    for name, value in result.properties.items():
        print(f"  {name:24s} = {value:16.6e}")

    print("\nTarget property errors:")
    for name, error in result.relative_property_errors.items():
        print(f"  {name:12s} = {100.0 * error:12.6f} %")

    print("\nNormalized dimension changes:")
    for name, change in result.normalized_dimension_changes.items():
        print(f"  {name:12s} = {100.0 * change:12.6f} %")
