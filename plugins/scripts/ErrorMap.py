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
        parallel: int = cpu_count(True),
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
            parallel (int, optional): The number of parallel processes to use. Defaults to the number of CPU cores available.
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

    def _generate_base(self, center: tuple, resolution: int):
        deformation = np.zeros((resolution, self.dimension))
        for i, x in enumerate(center):
            deformation[:, i] = np.linspace(
                0, x * self.ref_strain, resolution + 1, endpoint=True
            )[1:]
        return deformation

    def _generate_increment(self, dd: tuple[float, float], components: tuple[int, int]):
        increment = np.zeros((self.resolution, self.dimension))
        for c, d in zip(components, dd):
            increment[:, c] = np.linspace(
                0, d * self.ref_strain, self.resolution + 1, endpoint=True
            )[1:]
        return increment

    def _run_analysis(self, increment: np.ndarray):
        def _ensure_2d(_x):
            return _x.reshape(1, -1) if len(_x.shape) == 1 else _x

        if self._base is None:
            strain_history = _ensure_2d(increment)
        else:
            strain_history = np.vstack((self._base, self._base[-1, :] + increment))

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

        return _ensure_2d(np.loadtxt("RESULT.txt"))[-1, :]

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
        center_text = ""
        if self._base is not None:
            center = []
            for x in self._base[-1, :]:
                if x == 0:
                    break
                center.append(f"{x:.4e}")
            center_text = f"center: ({', '.join(center)}), "
        fig.text(
            0,
            0,
            f"{self.command}\n{center_text}reference strain $\\varepsilon_\\text{{ref}}$: {self.ref_strain:.4e}, reference stress $\\sigma_\\text{{ref}}$: {self.ref_stress:.4e}",
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

    def _run_all(self, dd: tuple[float, float], type: set, components: tuple[int, int]):
        with self._temporary_dir():
            increment = self._generate_increment(dd, components)
            reference = self._run_analysis(increment)
            coarse = self._run_analysis(increment[-1, :])
            results: dict = {}
            error = 100 * self._norm(coarse - reference)
            for t in type:
                match t:
                    case "abs":
                        results[t] = error / self.ref_stress
                    case "rel":
                        results[t] = error / self._norm(reference)
            return results

    def contour(
        self,
        title: str = "",
        *,
        center: tuple | None,
        size: int,
        components: tuple[int, int] = (0, 1),
        type: Literal["abs", "rel"] | set[Literal["abs", "rel"]] = "abs",
    ):
        """
        Generates and saves contour plots of error values over a specified 2D region.

        This method evaluates error values on a grid centred at a specified point, for the
        selected components and error types (absolute and/or relative). It then produces and
        saves contour plots in both PDF and SVG formats.

        :param str title: Optional title used as the base for the output filenames.
        :param tuple center: Center of the region in local coordinates. If provided,
            the base state will be regenerated with this center.
        :param int size: Half-size of the region in each direction. Determines the extent
            of the grid over which errors are computed.
        :param tuple[int, int] components: Indices of the components for which errors
            will be computed. Defaults to (0, 1).
        :param type: Type(s) of error to compute: absolute ("abs"), relative ("rel"), or both.
            Can be a single string or a set of strings.
        :type type: Literal["abs", "rel"] or set[Literal["abs", "rel"]]

        :raises RuntimeError: If there is a failure during the parallelized computation.
            In that case, a message will be printed, and no plots will be generated.

        :returns: None
        """
        if center:
            self._base = self._generate_base(center, self.base_resolution)

        bound = self.contour_samples
        region = np.array(range(-bound, bound + 1)) * size / float(bound)
        num_points = len(region)
        error_grid = np.zeros((num_points, num_points))

        if isinstance(type, str):
            type = {type}

        tasks: list = [None] * error_grid.size
        for x in range(error_grid.size):
            i, j = divmod(x, num_points)
            tasks[x] = (i, j, region[i], region[j])

        def _runner(_i, _j, _dx, _dy):
            return _i, _j, self._run_all((_dx, _dy), type, components)

        results: dict = {}
        try:
            for i, j, point in Parallel(  # type: ignore
                n_jobs=self.parallel, return_as="generator_unordered"
            )(delayed(_runner)(*task) for task in tqdm(tasks, desc="Contouring...")):
                results[(i, j)] = point
        except RuntimeError:
            print(
                "\nError encountered. Check the temporary directory for strain history files."
            )
            return

        ex_grid, ey_grid = np.meshgrid(region, region)

        for t in type:
            for (i, j), value in results.items():
                error_grid[i, j] = value[t]
            fig = self._generate_figure(ex_grid, ey_grid, error_grid, t)
            full_title = f"{title or self._material_name}.{t}.error"
            fig.savefig(f"{full_title}.pdf")
            fig.savefig(f"{full_title}.svg")
            plt.close()


if __name__ == "__main__":
    pass
