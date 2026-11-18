"""
section_registry_generator.py

Generate the US designation registries used by suanPan's SectionParser.cpp
from the AISC Shapes Database.

For every designation supported by suanPan's US section families, the nominal
geometry is extracted from the spreadsheet and the tabulated section
properties (A, Ix, Iy, Zx, Zy) are used as optimization targets.  The
idealized dimensions are then adjusted with section_optimizer.py so that the
resulting section reproduces the AISC properties as closely as possible.

Supported families and their registry functions:
    W, M, S, HP      -> I-section   -> usisection()
    WT, MT, ST       -> T-section   -> ustsection()
    HSS (rectangle)  -> box section -> usrhssection()
    HSS (circle)     -> tube        -> uschssection()

The output is plain C++ initializer text.  Each block can be copied directly
into the corresponding TokenRegistry in SectionParser.cpp.

Run:
    python section_registry_generator.py
    python section_registry_generator.py --output us_registry.inc
    python section_registry_generator.py --xlsx <url-or-path> --margin 0.05

Requires:
    pip install pandas openpyxl numpy scipy
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas
from section_optimizer import (
    BOX_SECTION,
    I_SECTION,
    MARGIN,
    T_SECTION,
    CircleSection,
    SectionModel,
    optimize_section,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_XLSX = ROOT / "docs/Library/Section/Code/aisc-shapes-database-v16.0.xlsx"

# The optimizer uses "area" while the spreadsheet uses "A".
TARGET_PROPERTIES = ("area", "Ix", "Iy", "Zx", "Zy")
SPREADSHEET_PROPERTIES = {"area": "A", "Ix": "Ix", "Iy": "Iy", "Zx": "Zx", "Zy": "Zy"}

# CircleSection needs an explicit wall-thickness parameter for a hollow tube.
ROUND_HSS = CircleSection(("d", "t"), ("t",))


@dataclass(frozen=True)
class Family:
    """One supported suanPan section family."""

    key: str
    registry: str
    description: str
    model: SectionModel
    dimension_comment: str


I_FAMILY = Family(
    "I",
    "usisection",
    "I-sections (W, M, S, HP)",
    I_SECTION,
    "bf_top, tf_top, bf_bot, tf_bot, web_height, tw",
)
T_FAMILY = Family(
    "T",
    "ustsection",
    "T-sections (WT, MT, ST)",
    T_SECTION,
    "bf, tf, web_height, tw",
)
BOX_FAMILY = Family(
    "B",
    "usrhssection",
    "rectangular HSS",
    BOX_SECTION,
    "midline width, midline height, thickness",
)
CHS_FAMILY = Family(
    "C",
    "uschssection",
    "round HSS",
    ROUND_HSS,
    "radius, thickness",
)
FAMILIES = (I_FAMILY, T_FAMILY, BOX_FAMILY, CHS_FAMILY)


@dataclass(frozen=True)
class Task:
    label: str
    family: Family
    initial_dimensions: tuple[float, ...]
    target: dict[str, float]
    groups: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class GeneratedSection:
    label: str
    family: Family
    dimensions: tuple[float, ...]
    errors: dict[str, float]
    mode: str


def _number(value: Any) -> float | None:
    """Convert a spreadsheet cell to a finite float, or None for '–' etc."""
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _required_numbers(row: pandas.Series, names: tuple[str, ...]) -> tuple[float, ...]:
    values = []
    for name in names:
        value = _number(row[name])
        if value is None:
            raise ValueError(f"missing or invalid column {name!r}")
        values.append(value)
    return tuple(values)


def _independent(model: SectionModel) -> tuple[tuple[str, ...], ...]:
    """Give every parameter its own scale factor (no automatic linking)."""
    return tuple((name,) for name in model.parameter_names)


def _make_task(row: pandas.Series) -> Task | None:
    """Extract the initial geometry and optimization targets for one row."""
    row_type = str(row["Type"]).strip().upper()
    label = str(row["AISC_Manual_Label"]).strip()
    if not label or label.lower() == "nan":
        return None

    if row_type in ("W", "M", "S", "HP"):
        bf, tf, d, tw = _required_numbers(row, ("bf", "tf", "d", "tw"))
        # ISection2D stores the clear web height between the two flanges.
        initial = (bf, tf, bf, tf, d - 2.0 * tf, tw)
        family = I_FAMILY
        groups = (("b_top", "b_bot"), ("t_top", "t_bot"))
    elif row_type in ("WT", "MT", "ST"):
        bf, tf, d, tw = _required_numbers(row, ("bf", "tf", "d", "tw"))
        # TSection2D stores the clear web height below the flange.
        initial = (bf, tf, d - tf, tw)
        family = T_FAMILY
        groups = _independent(T_SECTION)
    elif row_type == "HSS":
        depth = _number(row["Ht"])
        diameter = _number(row["OD"])
        if depth is not None:
            (width,) = _required_numbers(row, ("B",))
            (thickness,) = _required_numbers(row, ("tdes",))
            # BOX_SECTION is defined by outside dimensions.  Box2D in suanPan
            # takes midline dimensions, so the conversion happens on output.
            initial = (width, depth, thickness)
            family = BOX_FAMILY
            # Keep square tubes square, but leave rectangular tubes free.
            groups = (
                (("b", "h"),)
                if math.isclose(width, depth)
                else _independent(BOX_SECTION)
            )
        elif diameter is not None:
            (thickness,) = _required_numbers(row, ("tdes",))
            initial = (diameter, thickness)
            family = CHS_FAMILY
            groups = _independent(ROUND_HSS)
        else:
            return None
    else:
        return None

    if any(value <= 0.0 for value in initial):
        raise ValueError(f"non-positive geometry: {initial}")

    target = {
        name: _required_numbers(row, (SPREADSHEET_PROPERTIES[name],))[0]
        for name in TARGET_PROPERTIES
    }
    if any(value <= 0.0 for value in target.values()):
        raise ValueError(f"non-positive target property: {target}")

    return Task(label, family, initial, target, groups)


def _to_registry_dimensions(
    family: Family, dimensions: dict[str, float]
) -> tuple[float, ...]:
    """Map optimizer parameter names to the C++ TokenRegistry dimension order."""
    if family.key in ("I", "T"):
        return tuple(dimensions[name] for name in family.model.parameter_names)
    if family.key == "B":
        # Box2D's stored B and H are measured from midline to midline.
        return (
            dimensions["b"] - dimensions["t"],
            dimensions["h"] - dimensions["t"],
            dimensions["t"],
        )
    if family.key == "C":
        # CircularHollow2D stores the radius, not the diameter.
        return (dimensions["d"] / 2.0, dimensions["t"])
    raise AssertionError(f"unknown family {family.key}")


def _to_model_dimensions(
    family: Family, dimensions: tuple[float, ...]
) -> tuple[float, ...]:
    """Inverse of _to_registry_dimensions, used when checking rounded output."""
    if family.key == "B":
        return (
            dimensions[0] + dimensions[2],
            dimensions[1] + dimensions[2],
            dimensions[2],
        )
    if family.key == "C":
        return (2.0 * dimensions[0], dimensions[1])
    return dimensions


def _generate(task: Task, margin: float, decimals: int) -> GeneratedSection:
    result = optimize_section(
        task.family.model,
        task.initial_dimensions,
        task.target,
        mode="exact",
        variables=task.family.model.parameter_names,
        groups=task.groups,
        margin=margin,
    )

    registry_dimensions = _to_registry_dimensions(task.family, result.dimensions)
    rounded = tuple(round(value, decimals) for value in registry_dimensions)
    if any(value <= 0.0 for value in rounded):
        raise ValueError(f"non-positive optimized dimension: {rounded}")

    # Report the error of the dimensions that will actually be written out.
    properties = task.family.model.properties(
        np.asarray(_to_model_dimensions(task.family, rounded), dtype=float)
    )
    errors = {
        name: (properties[name] - task.target[name]) / task.target[name]
        for name in TARGET_PROPERTIES
    }

    return GeneratedSection(
        task.label, task.family, rounded, errors, result.mode_used
    )


def _cpp_number(value: float, decimals: int) -> str:
    text = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
    if text in ("", "-0"):
        return "0.0"
    if "." not in text:
        text += ".0"
    return text


def _cpp_entry(section: GeneratedSection, decimals: int) -> str:
    body = ", ".join(_cpp_number(value, decimals) for value in section.dimensions)
    return f'{{"{section.label}", {{{body}}}}},'


def _render(sections: list[GeneratedSection], decimals: int, source: str) -> str:
    lines = [
        f"// Generated from {source} with section_optimizer.py.",
        "// Dimensions are in inches. Each line is a TokenRegistry entry ready",
        "// to paste into SectionParser.cpp.",
        "",
    ]

    for family in FAMILIES:
        group = [section for section in sections if section.family.key == family.key]
        if not group:
            continue
        worst = max(
            max(abs(error) for error in section.errors.values())
            for section in group
        )
        lines.append(
            f"// {family.registry}(): {family.description}, {len(group)} sections, "
            f"max |relative property error| = {100.0 * worst:.2f}%"
        )
        lines.append(f"// dimensions: {family.dimension_comment}")
        lines.extend(_cpp_entry(section, decimals) for section in group)
        lines.append("")

    return "\n".join(lines)


def _summarize(sections: list[GeneratedSection]) -> None:
    print(f"{len(sections)} supported sections generated.", file=sys.stderr)
    for family in FAMILIES:
        group = [section for section in sections if section.family.key == family.key]
        if not group:
            continue
        errors = [
            (section.label, max(abs(error) for error in section.errors.values()))
            for section in group
        ]
        worst_label, worst_error = max(errors, key=lambda item: item[1])
        over_five = sum(error > 0.05 for _, error in errors)
        print(
            f"  {family.registry:14s} {len(group):4d} sections, "
            f"max {100.0 * worst_error:5.2f}% ({worst_label}), "
            f"> 5%: {over_five}",
            file=sys.stderr,
        )


def _load_table(source: str, sheet: int | str) -> pandas.DataFrame:
    if source.startswith(("http://", "https://")):
        return pandas.read_excel(
            source,
            sheet_name=sheet,
            usecols="A:CF",
            storage_options={"User-Agent": "Mozilla/5.0"},
        )

    path = Path(source).expanduser()
    if not path.exists():
        raise FileNotFoundError(
            f"cannot find {path}; pass --xlsx with a valid path or the AISC URL"
        )
    return pandas.read_excel(path, sheet_name=sheet, usecols="A:CF")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate suanPan US section registry entries from the AISC "
            "Shapes Database, using section_optimizer.py to match the "
            "tabulated section properties."
        )
    )
    parser.add_argument(
        "--xlsx",
        default=str(DEFAULT_XLSX),
        help="AISC workbook path or URL (default: the local v16.0 workbook).",
    )
    parser.add_argument(
        "--sheet",
        default="1",
        help="Worksheet name or zero-based index (default: 1).",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=MARGIN,
        help=f"Maximum relative change of each dimension (default: {MARGIN}).",
    )
    parser.add_argument(
        "--decimals",
        type=int,
        default=4,
        help="Decimal places in the generated C++ values (default: 4).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the C++ text to this file instead of stdout.",
    )
    args = parser.parse_args(argv)

    if not 0.0 < args.margin < 1.0:
        parser.error("--margin must lie between 0 and 1")
    if args.decimals < 0:
        parser.error("--decimals must be non-negative")
    return args


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    sheet: int | str = (
        int(args.sheet) if args.sheet.lstrip("+-").isdigit() else args.sheet
    )

    try:
        table = _load_table(args.xlsx, sheet)
    except (FileNotFoundError, ValueError, ImportError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    sections: list[GeneratedSection] = []
    for _, row in table.iterrows():
        try:
            task = _make_task(row)
        except (KeyError, ValueError) as error:
            label = str(row.get("AISC_Manual_Label", "?"))
            print(f"warning: skipping {label}: {error}", file=sys.stderr)
            continue
        if task is None:
            continue
        try:
            sections.append(_generate(task, args.margin, args.decimals))
        except Exception as error:  # keep the pipeline usable if one row fails
            print(
                f"warning: optimization failed for {task.label}: {error}",
                file=sys.stderr,
            )

    if not sections:
        print("error: no supported sections were found", file=sys.stderr)
        return 1

    source = (
        args.xlsx
        if args.xlsx.startswith(("http://", "https://"))
        else Path(args.xlsx).name
    )
    text = _render(sections, args.decimals, source)
    if args.output is None:
        sys.stdout.write(text)
    else:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)

    _summarize(sections)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
