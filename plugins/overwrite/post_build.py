#  Copyright (C) 2022-2026 Theodore Chang
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Apply the ``overwrite_math`` corrections to a built Zensical site.

Zensical does not run MkDocs plugins, so the rewrites performed by
``plugins/overwrite/overwrite.py`` are applied to the generated HTML after
``zensical build`` instead. Usage::

    python plugins/overwrite/post_build.py [site_dir]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Each pattern maps to its literal replacement. A callable is used so that
# backslashes in the replacement are never interpreted as regex escapes.
REWRITES = (
    (
        re.compile(r"<span class=arithmatex>\\\(<span class=arithmatex>\\\("),
        r"<span class=arithmatex>\(",
    ),
    (re.compile(r"\\\)</span>\\\)</span>"), r"\)</span>"),
    (
        re.compile(r"\$<span class=arithmatex>\\\("),
        r"<span class=arithmatex>\(",
    ),
    (re.compile(r"\\\)</span>\$"), r"\)</span>"),
)


def rewrite(html: str) -> tuple[str, int]:
    """Return corrected HTML and the number of replacements made."""
    total = 0
    for pattern, replacement in REWRITES:
        html, count = pattern.subn(lambda _, text=replacement: text, html)
        total += count
    return html, total


def main(argv: list[str] | None = None) -> int:
    """Rewrite all HTML files in the given site directory."""
    site = Path((argv or ["site"])[0])
    if not site.is_dir():
        raise SystemExit(f"Site directory does not exist: {site}")

    changed_files = 0
    total = 0
    for path in site.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        updated, count = rewrite(html)
        if count:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
            total += count

    print(f"Overwrite math: {total} replacements in {changed_files} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
