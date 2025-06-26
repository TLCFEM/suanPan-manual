#  Copyright (C) 2022-2025 Theodore Chang
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

import subprocess
from contextlib import contextmanager
from genericpath import exists
from os import chdir, environ, getcwd, mkdir, remove
from random import choices
from shutil import which
from string import ascii_letters, digits
from tempfile import TemporaryDirectory
from time import sleep
from typing import Literal

import numpy as np
from joblib import Parallel, cpu_count, delayed
from matplotlib import pyplot as plt
from tqdm import tqdm


class ErrorLine:
    def __init__(
        self,
        command: str,
        *,
        ref_strain: float,
        ref_stress: float = 1.0,
        resolution: int = 100,
        base_resolution: int = 200,
        executable: str = "suanpan",
        tmp_dir: str = "tmp",
        contour_samples: int = 20,
        parallel: int = cpu_count(True),
    ):
        """Initializes an ErrorLine instance with the specified parameters.
        Args:
            command (str): The command string, typically containing the material name as the second word.
            ref_strain (float): The reference strain value.
            ref_stress (float, optional): The reference stress value. Defaults to 1.0.
            resolution (int, optional): The number of steps used to compute from center to target. Defaults to 100.
            base_resolution (int, optional): The number of steps used to compute from origin to center. Defaults to 200.
            executable (str, optional): The name or path of the executable to use. Defaults to "suanpan".
            tmp_dir (str, optional): The directory for temporary files. Defaults to "tmp".
            contour_samples (int, optional): The number of samples for contour calculation. Defaults to 20.
            parallel (int, optional): The number of parallel processes to use. Defaults to the number of CPU cores available.
        Raises:
            FileNotFoundError: If the specified executable is not found in the system PATH.
            ValueError: If the temporary directory is not specified.
        """
        self.command = command
        self.ref_strain = ref_strain
        self.ref_stress = ref_stress
        self.resolution = resolution
        self.base_resolution = base_resolution
        self.executable = executable
        self.tmp_dir = tmp_dir
        self.contour_samples = contour_samples
        self.parallel = max(1, parallel)

        if which(self.executable) is None:
            raise FileNotFoundError(f"Executable '{self.executable}' not found.")

        if not self.tmp_dir:
            raise ValueError("Temporary directory must be specified.")

        self._material_name = command.split()[1].lower()
        self._base: np.ndarray = None  # type: ignore
        self._original_dir = getcwd()
        self._tmp_abs_dir = None  # type: ignore

        environ["MKL_NUM_THREADS"] = "1"
        environ["OMP_NUM_THREADS"] = "1"

    def __enter__(self):
        if not exists(self.tmp_dir):
            mkdir(self.tmp_dir)
        chdir(self.tmp_dir)
        self._tmp_abs_dir = getcwd()

        self._write_main()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        chdir(self._original_dir)

        return False

    def _write_main(self):
        with open("isomap.sp", "w") as f:
            f.write(
                f"{self.command}\nmaterialtestbystrainhistory 1 strain_history\nexit\n"
            )

    def _generate_base(self, center: float, resolution: int):
        return np.linspace(0, center * self.ref_strain, resolution + 1, endpoint=True)[
            1:
        ]

    def _generate_increment(self, dx: float):
        return np.linspace(0, dx * self.ref_strain, self.resolution + 1, endpoint=True)[
            1:
        ]

    def _run_analysis(self, increment: np.ndarray):
        if self._base is not None:
            strain_history = np.concatenate((self._base, self._base[-1] + increment))
        else:
            strain_history = increment

        np.savetxt("strain_history", strain_history)

        if exists("RESULT.txt"):
            remove("RESULT.txt")

        result = subprocess.run(
            [self.executable, "-f", "isomap.sp"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if "[ERROR]" in result.stdout:
            np.savetxt(
                f"{self._tmp_abs_dir}/strain_history_"
                + "".join(choices(ascii_letters + digits, k=6)),
                strain_history,
            )
            raise RuntimeError(result.stdout)

        while not exists("RESULT.txt"):
            sleep(0.01)

        return np.loadtxt("RESULT.txt")[-1]

    def _generate_figure(self, x: np.ndarray, y: np.ndarray, type: str):
        fig = plt.figure(figsize=(7.5, 5))
        plt.title(self._material_name.upper())
        if type == "abs":
            full_title = r"Absolute Error (unit: % of $\sigma_\text{ref}$)"
        else:
            full_title = "Relative Error (unit: %)"

        plt.plot(x, y, label="linear scale", marker="o")
        plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon_{\\text{ref}}$")
        plt.ylabel(full_title)
        plt.legend(loc="center left")
        plt.grid()

        ax2 = plt.gca().twinx()
        ax2.set_ylabel(" absolute value")
        ax2.plot(x, np.abs(y), label="log scale", marker="x", color="orange")
        ax2.set_yscale("log")
        plt.legend(loc="center right")
        plt.grid(linestyle="--")

        center_text = ""
        if self._base is not None:
            center_text = f"center: ({self._base[-1]:.4e}), "

        fig.text(
            0,
            0,
            f"{self.command}\n{center_text}reference strain $\\varepsilon_\\text{{ref}}$: {self.ref_strain:.4e}, reference stress $\\sigma_\\text{{ref}}$: {self.ref_stress:.4e}",
            fontsize=8,
            va="bottom",
            ha="left",
        )
        plt.tight_layout()
        return fig

    @contextmanager
    def _temporary_dir(self):
        if self.parallel > 1:
            original_dir = getcwd()
            with TemporaryDirectory() as tmp_dir:
                chdir(tmp_dir)
                self._write_main()
                try:
                    yield tmp_dir
                finally:
                    chdir(original_dir)
        else:
            yield

    def _run_all(self, dx, type: set):
        with self._temporary_dir():
            increment = self._generate_increment(dx)
            reference = self._run_analysis(increment)
            coarse = self._run_analysis(increment[-1:])
            results: dict = {}
            error = 100 * (coarse - reference)
            for t in type:
                match t:
                    case "abs":
                        results[t] = error / self.ref_stress
                    case "rel":
                        results[t] = error / reference
            return results

    def contour(
        self,
        title: str = "",
        *,
        center: float | None,
        size: int,
        type: Literal["abs", "rel"] | set[Literal["abs", "rel"]] = "abs",
    ):
        """
        Generates and saves a 1D contour plot of error values over a specified region.

        This method computes error values along a 1D line centered at a given point, for one
        or both error types (absolute and/or relative), and generates corresponding plots.

        :param str title: Optional prefix for the output filenames. Defaults to an empty string.
        :param float center: Center coordinate of the region to evaluate.
        :param int size: Half-size of the region to plot. Determines the extent of the sampling region.
        :param type: Type(s) of error to compute: "abs" (absolute error), "rel" (relative error),
            or both. Can be a single string or a set of strings.
        :type type: Literal["abs", "rel"] or set[Literal["abs", "rel"]]

        :raises RuntimeError: If a parallel execution error occurs during evaluation.

        :returns: None
        """
        if center is not None:
            self._base = self._generate_base(center, self.base_resolution)

        bound = self.contour_samples
        region = (
            np.array([x for x in range(-bound, bound + 1) if x != 0])
            * size
            / float(bound)
        )
        error_grid = np.zeros_like(region)

        if isinstance(type, str):
            type = {type}

        def _runner(_x, _dx):
            return _x, self._run_all(_dx, type)

        results: list = [None] * error_grid.size
        try:
            for i, point in Parallel(  # type: ignore
                n_jobs=self.parallel, return_as="generator_unordered"
            )(
                delayed(_runner)(x, dx)
                for x, dx in enumerate(tqdm(region, desc="Contouring..."))
            ):
                results[i] = point
        except RuntimeError:
            print(
                "\nError encountered. Check the temporary directory for strain history files."
            )
            return

        for t in type:
            for i, value in enumerate(results):
                error_grid[i] = value[t]
            fig = self._generate_figure(region, error_grid, t)
            full_title = f"{title or self._material_name}.{t}.error"
            fig.savefig(f"{full_title}.pdf")
            fig.savefig(f"{full_title}.svg")
            plt.close()


if __name__ == "__main__":
    pass
