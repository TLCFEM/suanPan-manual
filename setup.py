import os
import re
import shutil
import sys
import tarfile
import zipfile
from urllib.request import urlopen

from setuptools import setup


def remove(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


def install(run_doxygen: bool):
    # root directory
    remove("docs/Doxygen")
    remove("site")

    # 1. download source code
    archive_name = "suanPan-dev"

    url = "https://github.com/TLCFEM/suanPan/archive/refs/heads/dev.zip"
    with urlopen(url) as response, open(f"{archive_name}.zip", "wb") as archive:
        shutil.copyfileobj(response, archive)
    with zipfile.ZipFile(f"{archive_name}.zip", "r") as archive:
        archive.extractall(".")
    os.remove(f"{archive_name}.zip")

    # 2. generate doxygen documentation
    os.chdir(archive_name)

    if shutil.which(doxygen_bin := "doxygen") is not None and run_doxygen:
        os.system(doxygen_bin)

        target_path = "../docs/Doxygen"
        shutil.copytree("Document/html", target_path)
        shutil.copytree("Resource", f"{target_path}/Resource/")
        shutil.copy("../docs/favicon.ico", f"{target_path}/favicon.ico")

    with open("Toolbox/argument.cpp") as f:
        version_file = f.read()

    major = re.search(r"constexpr auto SUANPAN_MAJOR = (\d);", version_file).group(1)
    minor = re.search(r"constexpr auto SUANPAN_MINOR = (\d);", version_file).group(1)
    patch = re.search(r"constexpr auto SUANPAN_PATCH = (\d);", version_file).group(1)

    os.chdir("..")

    remove(archive_name)

    # 3. download binary file
    if sys.platform.startswith("linux"):
        binary_file_name = "suanPan-linux-openblas-no-avx"
        binary_file = f"{binary_file_name}.tar.gz"
    else:
        binary_file_name = "suanPan-win-mkl-vtk"
        binary_file = f"{binary_file_name}.zip"
    remove(binary_file_name)

    with urlopen("https://github.com/TLCFEM/suanPan") as response:
        content = response.read().decode("utf-8")
        version_string = re.search(r"suanPan-v\d\.\d(\.\d)?", content).group(0)

    url = f"https://github.com/TLCFEM/suanPan/releases/download/{version_string}/{binary_file}"
    with urlopen(url) as response, open(binary_file, "wb") as archive:
        shutil.copyfileobj(response, archive)

    if sys.platform.startswith("linux"):
        with tarfile.open(binary_file, "r:gz") as archive:
            archive.extractall(binary_file_name)
    else:
        with zipfile.ZipFile(binary_file, "r") as archive:
            archive.extractall(binary_file_name)

    os.remove(binary_file)

    with open("requirements.txt") as f:
        required = f.read().splitlines()

    setup(
        name="suanPan-manual",
        version=f"{major}.{minor}.{patch}",
        description="suanPan-manual",
        author="Theodore Chang",
        author_email="tlcfem@gmail.com",
        install_requires=required,
        entry_points={
            "mkdocs.plugins": [
                "overwrite_math = plugins.overwrite.overwrite:OverwriteMath",
            ]
        },
    )


if __name__ == "__main__":
    install("egg_info" not in sys.argv)
