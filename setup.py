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

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from setuptools import setup

ROOT_FOLDER = Path(__file__).parent


def prepare_doxygen(archive_path: Path):
    if shutil.which("doxygen") is None:
        return

    # 2. generate doxygen documentation
    url = "https://api.github.com/repos/TLCFEM/suanPan/commits/dev"
    with urlopen(url) as response:
        (doxyfile := archive_path / "Doxyfile").write_text(
            re.sub(
                r"^PROJECT_NUMBER\s+=.*$",
                f"PROJECT_NUMBER = {json.load(response)['sha'][:7]}",
                doxyfile.read_text(),
            )
        )

    subprocess.run(["doxygen"], cwd=archive_path, check=True)

    shutil.copytree(archive_path / "Document/html", ROOT_FOLDER / "docs/Doxygen")
    shutil.copytree(archive_path / "Resource", ROOT_FOLDER / "docs/Doxygen/Resource")
    shutil.copy(
        ROOT_FOLDER / "docs/favicon.ico",
        ROOT_FOLDER / "docs/Doxygen/favicon.ico",
    )


def prepare_binary():
    if shutil.which("suanpan") is not None or shutil.which("sp") is not None:
        return

    # skip arm64
    if platform.machine().lower() in ("arm64", "aarch64", "arm"):
        return

    system = platform.system().lower()

    # 3. download binary file
    if system.startswith("linux"):
        binary_file_name = "suanPan-linux-amd64-openblas-no-avx"
        binary_file = f"{binary_file_name}.tar.gz"
    elif system.startswith("windows"):
        binary_file_name = "suanPan-win-mkl-vtk"
        binary_file = f"{binary_file_name}.zip"
    elif system.startswith("darwin"):
        binary_file_name = "suanPan-macos-15-amd64-openblas-vtk-avx"
        binary_file = f"{binary_file_name}.tar.gz"
    else:
        return

    shutil.rmtree(binary_file_name, True)

    with urlopen("https://api.github.com/repos/TLCFEM/suanPan/releases") as response:
        releases = json.load(response)

    latest_tag = next((r["tag_name"] for r in releases if r["assets"]), None)
    url = f"https://github.com/TLCFEM/suanPan/releases/download/{latest_tag}/{binary_file}"

    with TemporaryDirectory() as tmp_dir:
        archive_path = Path(tmp_dir) / binary_file

        with urlopen(url) as response, archive_path.open("wb") as archive:
            shutil.copyfileobj(response, archive)

        if binary_file.endswith(".tar.gz"):
            target = tarfile.open(archive_path, "r:gz")
        else:
            target = zipfile.ZipFile(archive_path, "r")

        with target as archive:
            archive.extractall(binary_file_name)


def install(run_doxygen: bool):
    # root directory
    shutil.rmtree(ROOT_FOLDER / "docs/Doxygen", True)
    shutil.rmtree(ROOT_FOLDER / "site", True)

    # 1. download source code
    with TemporaryDirectory() as tmp_dir:
        archive_name = "suanPan-dev"
        archive_zip = Path(tmp_dir) / f"{archive_name}.zip"
        archive_path = Path(tmp_dir) / archive_name

        url = "https://github.com/TLCFEM/suanPan/archive/refs/heads/dev.zip"
        with urlopen(url) as response, archive_zip.open("wb") as archive:
            shutil.copyfileobj(response, archive)
        with zipfile.ZipFile(archive_zip, "r") as archive:
            archive.extractall(tmp_dir)

        version = (archive_path / "Toolbox/command.h").read_text()
        major = re.search(r"constexpr auto SUANPAN_MAJOR = (\d);", version).group(1)
        minor = re.search(r"constexpr auto SUANPAN_MINOR = (\d);", version).group(1)
        patch = re.search(r"constexpr auto SUANPAN_PATCH = (\d);", version).group(1)

        if run_doxygen:
            prepare_doxygen(archive_path)

    prepare_binary()

    setup(
        name="suanPan-manual",
        version=f"{major}.{minor}.{patch}",
        description="suanPan-manual",
        author="Theodore Chang",
        author_email="tlcfem@gmail.com",
        install_requires=Path("requirements.txt").read_text().splitlines(),
        entry_points={
            "mkdocs.plugins": [
                "overwrite_math = plugins.overwrite.overwrite:OverwriteMath",
            ]
        },
    )


if __name__ == "__main__":
    os.chdir(ROOT_FOLDER)

    install("egg_info" not in sys.argv)
