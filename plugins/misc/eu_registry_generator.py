"""
eu_registry_generator.py

Generate the adjusted EU designation registry used by suanPan's
SectionParser.cpp from the tabulated EN 10365:2017 section properties.

The input CSV (docs/Library/Section/Code/eu.csv) contains the nominal
dimensions and the tabulated properties A, Iy, Iz, Wply and Wplz of the
HEA, HEB, HEM, IPE, UB, UC and UBP series.  The rectangular I-section
idealization ignores root fillets and flange taper, so the nominal
dimensions do not reproduce the tabulated area and inertias exactly.

For every designation the flange width, flange thickness, web depth and web
thickness are adjusted with section_optimizer.py so that the computed
properties follow the tabulated values.  Equal flanges are kept equal.

The output is plain C++ initializer text that can be copied into
euisection_adjusted() in SectionParser.cpp.

Run:
    python eu_registry_generator.py
    python eu_registry_generator.py --output eu_registry.inc
    python eu_registry_generator.py --margin 0.10
    python eu_registry_generator.py --csv path/to/sections.csv

Requires:
    pip install numpy scipy
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from section_optimizer import I_SECTION, optimize_section

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = ROOT / "docs/Library/Section/Code/eu.csv"
DEFAULT_MARGIN = 0.10

# The C++ registry order used by euisection().
SERIES_ORDER = ("HEA", "HEB", "IPE", "HEM", "UB", "UC", "UBP")

# The rectangular idealization has four independent dimensions: flange width,
# flange thickness, web depth and web thickness.  Equal flanges are linked.
GROUPS = (("b_top", "b_bot"), ("t_top", "t_bot"))
VARIABLES = tuple(I_SECTION.parameter_names)

PROPERTIES = ("area", "Ix", "Iy", "Zx", "Zy")


@dataclass(frozen=True)
class GeneratedSection:
    label: str
    series: str
    dimensions: tuple[float, ...]
    errors: dict[str, float]
    mode: str


def _initial_dimensions(row: dict[str, str]) -> list[float]:
    b = float(row["b_mm"])
    tf = float(row["tf_mm"])
    h = float(row["h_mm"])
    tw = float(row["tw_mm"])
    # b_top, t_top, b_bot, t_bot, h_web, t_web
    return [b, tf, b, tf, h - 2.0 * tf, tw]


def _target_properties(row: dict[str, str]) -> dict[str, float]:
    # The CSV uses strong/weak rather than Dlubal's y/z axis names.
    return {
        "area": float(row["A_mm2"]),
        "Ix": float(row["I_strong_mm4"]),
        "Iy": float(row["I_weak_mm4"]),
        "Zx": float(row["Wpl_strong_mm3"]),
        "Zy": float(row["Wpl_weak_mm3"]),
    }


def _generate(row: dict[str, str], margin: float) -> GeneratedSection:
    target = _target_properties(row)
    result = optimize_section(
        I_SECTION,
        _initial_dimensions(row),
        target,
        mode="exact",
        variables=VARIABLES,
        groups=GROUPS,
        margin=margin,
        maxiter=5000,
    )
    dimensions = tuple(result.dimensions[name] for name in I_SECTION.parameter_names)
    properties = I_SECTION.properties(np.asarray(dimensions))
    errors = {
        name: (properties[name] - target[name]) / target[name] for name in PROPERTIES
    }
    return GeneratedSection(
        row["designation"], row["series"], dimensions, errors, result.mode_used
    )


def _cpp_number(value: float, decimals: int) -> str:
    text = f"{value:.{decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _cpp_line(section: GeneratedSection, decimals: int) -> str:
    values = ", ".join(_cpp_number(value, decimals) for value in section.dimensions)
    return f'{{"{section.label}", {{{values}}}}},'


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"Section property CSV (default: {DEFAULT_CSV.relative_to(ROOT)}).",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=DEFAULT_MARGIN,
        help=f"Maximum relative change of each dimension (default: {DEFAULT_MARGIN}).",
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

    if not args.csv.is_file():
        print(f"error: cannot find {args.csv}", file=sys.stderr)
        return 1

    with args.csv.open(newline="") as file:
        rows = list(csv.DictReader(file))

    order = {name: index for index, name in enumerate(SERIES_ORDER)}

    def sort_key(row: dict[str, str]) -> tuple[int, tuple[int, ...]]:
        size = tuple(int(value) for value in re.findall(r"\d+", row["designation"]))
        return order.get(row["series"], 99), size

    rows.sort(key=sort_key)

    sections = [_generate(row, args.margin) for row in rows]
    lines = [_cpp_line(section, args.decimals) for section in sections]

    text = "\n".join(lines) + "\n"
    if args.output:
        args.output.write_text(text)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)

    print(f"{len(sections)} sections generated.", file=sys.stderr)
    for series in SERIES_ORDER:
        group = [section for section in sections if section.series == series]
        if not group:
            continue
        strong = max(
            abs(section.errors[name])
            for section in group
            for name in ("area", "Ix", "Zx")
        )
        weak = max(
            abs(section.errors[name]) for section in group for name in ("Iy", "Zy")
        )
        print(
            f"  {series:4s} {len(group):3d} sections, "
            f"max {100.0 * max(strong, weak):5.2f}% "
            f"(strong {100.0 * strong:4.2f}%, weak {100.0 * weak:4.2f}%)",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
