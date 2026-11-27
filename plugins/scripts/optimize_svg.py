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

"""Optimize SVG files in parallel with batched svgo invocations."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

DEFAULT_EXCLUDE = ("inherit_graph.*",)


def collect(directories: list[Path], exclude: tuple[str, ...]) -> list[Path]:
    """Find SVG files, skipping names matched by the exclusion regexes."""
    patterns = [re.compile(pattern) for pattern in exclude]
    files: set[Path] = set()
    for directory in directories:
        if not directory.is_dir():
            raise FileNotFoundError(f"not a directory: {directory}")
        for path in directory.rglob("*"):
            if (
                path.is_file()
                and path.suffix.lower() == ".svg"
                and not any(pattern.search(path.name) for pattern in patterns)
            ):
                files.add(path)
    return sorted(files)


def optimize(files: list[Path], executable: str) -> list[tuple[Path, str]]:
    """Optimize one batch in place and return (file, message) for failures."""
    result = subprocess.run(
        [executable, "--quiet", "--", *(str(path) for path in files)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0:
        return []

    message = (
        result.stderr
        or result.stdout
        or f"{executable} exited with {result.returncode}"
    ).strip()
    if len(files) == 1:
        return [(files[0], message)]

    # A bad SVG makes svgo exit early. Retry individually to isolate it and
    # still optimize the rest of the batch.
    failures: list[tuple[Path, str]] = []
    for path in files:
        failures.extend(optimize([path], executable))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directories", nargs="+", type=Path, help="directories to scan recursively"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        metavar="REGEX",
        help="regex matched against file names; default: inherit_graph.*",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=int(os.environ.get("SVGO_JOBS", os.cpu_count() or 1)),
        help="number of concurrent svgo processes; default: CPU count",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="files per svgo invocation; default: 16",
    )
    parser.add_argument(
        "--executable", default="svgo", help="svgo executable; default: svgo"
    )
    args = parser.parse_args()

    if shutil.which(args.executable) is None:
        print(f"error: {args.executable} not found on PATH", file=sys.stderr)
        return 1
    if args.jobs < 1 or args.batch_size < 1:
        parser.error("--jobs and --batch-size must be positive")

    exclude = tuple(args.exclude) if args.exclude is not None else DEFAULT_EXCLUDE
    try:
        files = collect(args.directories, exclude)
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if not files:
        print("No SVG files found.")
        return 0

    batches = [
        files[index : index + args.batch_size]
        for index in range(0, len(files), args.batch_size)
    ]
    workers = min(args.jobs, len(batches))
    print(
        f"Optimizing {len(files)} SVG files with {workers} workers in {len(batches)} batches..."
    )
    start = perf_counter()
    failures: list[tuple[Path, str]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(optimize, batch, args.executable) for batch in batches]
        for future in as_completed(futures):
            failures.extend(future.result())

    if failures:
        for path, message in failures:
            print(f"error: {path}: {message}", file=sys.stderr)
        print(
            f"Failed to optimize {len(failures)} of {len(files)} files.",
            file=sys.stderr,
        )
        return 1

    print(f"Optimized {len(files)} files in {perf_counter() - start:.2f}s.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
