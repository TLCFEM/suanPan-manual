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
from shutil import which
from tempfile import TemporaryDirectory
from time import sleep
from typing import Literal

import numpy as np
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
from tqdm import tqdm


class ErrorMap:
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
        parallel: int = 1,
        dimension: int = 6,
    ):
        """Initializes an ErrorMap instance with the specified parameters.
        Args:
            command (str): The command string, typically containing the material name as the second word.
            ref_strain (float): The reference strain value.
            ref_stress (float, optional): The reference stress value. Defaults to 1.0.
            resolution (int, optional): The number of steps used to compute from center to target. Defaults to 100.
            base_resolution (int, optional): The number of steps used to compute from origin to center. Defaults to 200.
            executable (str, optional): The name or path of the executable to use. Defaults to "suanpan".
            tmp_dir (str, optional): The directory for temporary files. Defaults to "tmp".
            contour_samples (int, optional): The number of samples for contour calculation. Defaults to 20.
            parallel (int, optional): The number of parallel processes to use. Defaults to 1.
            dimension (int, optional): The dimension of the problem, either 3 or 6. Defaults to 6.
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
        self.dimension = dimension

        if which(self.executable) is None:
            raise FileNotFoundError(f"Executable '{self.executable}' not found.")

        if not self.tmp_dir:
            raise ValueError("Temporary directory must be specified.")

        if self.dimension not in (3, 6):
            raise ValueError("Dimension must be 3 or 6.")

        self._material_name = command.split()[1].lower()
        self._base: np.ndarray = None  # type: ignore
        self._original_dir = getcwd()

        environ["MKL_NUM_THREADS"] = "1"
        environ["OMP_NUM_THREADS"] = "1"

    def __enter__(self):
        if not exists(self.tmp_dir):
            mkdir(self.tmp_dir)
        chdir(self.tmp_dir)

        if self.parallel < 2:
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

    def _generate_base(self, center: tuple, resolution: int):
        deformation = np.zeros((resolution, self.dimension))
        for i, x in enumerate(center):
            deformation[:, i] = np.linspace(
                0, x * self.ref_strain, resolution + 1, endpoint=True
            )[1:]
        return deformation

    def _generate_increment(self, dx: float, dy: float):
        increment = np.zeros((self.resolution, self.dimension))
        increment[:, 0] = np.linspace(
            0, dx * self.ref_strain, self.resolution + 1, endpoint=True
        )[1:]
        increment[:, 1] = np.linspace(
            0, dy * self.ref_strain, self.resolution + 1, endpoint=True
        )[1:]
        return increment

    def _run_analysis(self, increment: np.ndarray):
        np.savetxt(
            "strain_history",
            np.vstack((self._base, self._base[-1, :] + increment)),
        )

        if exists("RESULT.txt"):
            remove("RESULT.txt")

        result = subprocess.run(
            [self.executable, "-f", "isomap.sp"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if "[ERROR]" in result.stdout:
            raise RuntimeError(result.stdout)

        while not exists("RESULT.txt"):
            sleep(0.01)

        return np.loadtxt("RESULT.txt")[-1, :]

    def _generate_figure(
        self, x_grid: np.ndarray, y_grid: np.ndarray, grid: np.ndarray, type: str
    ):
        fig = plt.figure(figsize=(7.5, 7))
        contour = plt.contourf(x_grid, y_grid, grid, levels=20, cmap="coolwarm")
        plt.colorbar(contour, aspect=30, ax=fig.gca(), fraction=0.03)
        contour = plt.contour(
            x_grid, y_grid, grid, levels=20, colors="black", linewidths=0.2
        )
        plt.clabel(contour, inline=True, fontsize=8)
        plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon_{\\text{ref}}$")
        plt.ylabel("$\\Delta{}\\varepsilon_y/\\varepsilon_{\\text{ref}}$")
        if type == "abs":
            full_title = f"{self._material_name.upper()} Absolute Error (unit: % of $\\sigma_\\text{{ref}}$)"
        else:
            full_title = f"{self._material_name.upper()} Relative Error (unit: %)"
        plt.title(full_title)
        center = []
        for x in self._base[-1, :]:
            if x == 0:
                break
            center.append(f"{x:.4e}")
        fig.text(
            0,
            0,
            f"{self.command}\ncenter: ({', '.join(center)}), reference strain $\\varepsilon_\\text{{ref}}$: {self.ref_strain:.4e}, reference stress $\\sigma_\\text{{ref}}$: {self.ref_stress:.4e}",
            fontsize=8,
            va="bottom",
            ha="left",
        )
        plt.gca().set_aspect("equal", adjustable="box")
        plt.tight_layout()
        return fig

    @staticmethod
    def _norm(stress: np.ndarray):
        stress = np.square(stress)
        stress[3:] = 2 * stress[3:]
        return np.sqrt(np.sum(stress))

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

    def _run_all(self, dx, dy, type):
        with self._temporary_dir():
            increment = self._generate_increment(dx, dy)
            reference = self._run_analysis(increment)
            coarse = self._run_analysis(increment[-1, :])
            denominator = self.ref_stress if type == "abs" else self._norm(reference)
            return 100 * self._norm(coarse - reference) / denominator

    def contour(
        self,
        title: str = "",
        *,
        center: tuple,
        size: int,
        type: Literal["abs", "rel"] = "abs",
    ):
        """Generates and saves a contour plot of error values over a specified region.
        Args:
            title (str, optional): The title prefix for the generated plot files. Defaults to "".
            type (Literal["abs", "rel"], optional): The type of error to plot, either "abs" for absolute error or "rel" for relative error. Defaults to "abs".
            center (tuple): The center coordinates of the region to plot.
            size (int): The half-size of the region to plot, determining the extent of the contour grid.
        Generates:
            - A contour plot of error values computed over a grid centered at `center` with the specified `size`.
            - Saves the plot as both PDF and SVG files, named using the material name, error type, and "error" suffix.
        """
        self._base = self._generate_base(center, self.base_resolution)

        region = (
            np.array(range(-self.contour_samples, self.contour_samples + 1))
            * size
            / float(self.contour_samples)
        )
        num_points = len(region)
        error_grid = np.zeros((num_points, num_points))

        tasks: list = [None] * error_grid.size
        for x in range(error_grid.size):
            i, j = divmod(x, num_points)
            tasks[x] = (i, j, region[i], region[j])

        def _runner(_i, _j, _dx, _dy):
            return _i, _j, self._run_all(_dx, _dy, type)

        for i, j, point in Parallel(  # type: ignore
            n_jobs=self.parallel, return_as="generator_unordered"
        )(delayed(_runner)(*task) for task in tqdm(tasks, desc="Contouring...")):
            error_grid[i, j] = point

        ex_grid, ey_grid = np.meshgrid(region, region)
        fig = self._generate_figure(ex_grid, ey_grid, error_grid, type)
        full_title = f"{title or self._material_name}.{type}.error"
        fig.savefig(f"{full_title}.pdf")
        fig.savefig(f"{full_title}.svg")


if __name__ == "__main__":
    pass
