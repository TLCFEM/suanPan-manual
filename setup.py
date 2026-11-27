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

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SOURCE_URL = "https://github.com/TLCFEM/suanPan/archive/refs/heads/dev.zip"
COMMIT_URL = "https://api.github.com/repos/TLCFEM/suanPan/commits/dev"
RELEASES_URL = "https://api.github.com/repos/TLCFEM/suanPan/releases"
BINARY = {
    "linux": "suanPan-linux-amd64-openblas-no-avx.tar.gz",
    "windows": "suanPan-win-mkl-vtk.zip",
    "darwin": "suanPan-macos-15-amd64-openblas-vtk-avx.tar.gz",
}


def fetch_json(url: str) -> dict:
    with urlopen(url) as response:
        return json.load(response)


def download(url: str, target: Path) -> None:
    with urlopen(url) as response, target.open("wb") as file:
        shutil.copyfileobj(response, file)


def read_version(source: Path) -> str:
    command = (source / "Toolbox/command.h").read_text()
    return ".".join(
        re.search(rf"constexpr auto SUANPAN_{part} = (\d);", command).group(1)
        for part in ("MAJOR", "MINOR", "PATCH")
    )


def prepare_source(directory: Path) -> Path:
    archive = directory / "suanPan-dev.zip"
    download(SOURCE_URL, archive)
    with zipfile.ZipFile(archive) as file:
        file.extractall(directory)
    return directory / "suanPan-dev"


def prepare_doxygen(source: Path) -> None:
    if shutil.which("doxygen") is None:
        return

    doxyfile = source / "Doxyfile"
    sha = fetch_json(COMMIT_URL)["sha"][:7]
    doxyfile.write_text(
        re.sub(
            r"^PROJECT_NUMBER\s+=.*$",
            f"PROJECT_NUMBER = {sha}",
            doxyfile.read_text(),
        )
    )
    subprocess.run(["doxygen"], cwd=source, check=True)

    target = DOCS / "Doxygen"
    shutil.copytree(source / "Document/html", target)
    shutil.copytree(source / "Resource", target / "Resource")
    shutil.copy(DOCS / "favicon.ico", target / "favicon.ico")


def prepare_binary() -> None:
    if shutil.which("suanpan") or shutil.which("sp"):
        return
    if platform.machine().lower() in ("arm64", "aarch64", "arm"):
        return

    system = platform.system().lower()
    filename = next(
        (name for prefix, name in BINARY.items() if system.startswith(prefix)),
        None,
    )
    if filename is None:
        return

    name = filename.split(".", 1)[0]
    shutil.rmtree(name, True)
    tag = next(
        release["tag_name"] for release in fetch_json(RELEASES_URL) if release["assets"]
    )
    with TemporaryDirectory() as directory:
        archive = Path(directory) / filename
        download(
            f"https://github.com/TLCFEM/suanPan/releases/download/{tag}/{filename}",
            archive,
        )
        with (
            tarfile.open(archive, "r:gz")
            if filename.endswith(".tar.gz")
            else zipfile.ZipFile(archive)
        ) as file:
            file.extractall(name)


def install() -> None:
    shutil.rmtree(DOCS / "Doxygen", True)
    shutil.rmtree(ROOT / "site", True)
    with TemporaryDirectory() as directory:
        source = prepare_source(Path(directory))
        version = read_version(source)
        if "egg_info" not in sys.argv:
            prepare_doxygen(source)
        prepare_binary()

    setup(
        name="suanPan-manual",
        version=version,
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
    os.chdir(ROOT)
    install()
