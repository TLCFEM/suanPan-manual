import subprocess
from genericpath import exists
from os import chdir, getcwd, mkdir, remove
from shutil import which
from time import sleep

import numpy as np
from matplotlib import pyplot as plt


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
        Raises:
            FileNotFoundError: If the specified executable is not found in the system PATH.
        """
        self.material_name = command.split()[1].lower()
        self.command = command
        self.ref_strain = ref_strain
        self.ref_stress = ref_stress
        self.resolution = resolution
        self.base_resolution = base_resolution
        self.base_deformation: np.ndarray = None  # type: ignore
        self.executable = executable
        self.tmp_dir = tmp_dir
        self.contour_samples = contour_samples

        if which(self.executable) is None:
            raise FileNotFoundError(
                f"Executable '{self.executable}' not found. Please ensure it is installed and in your PATH."
            )

        self.original_dir = None

    def __enter__(self):
        if not self.tmp_dir:
            return self

        if not exists(self.tmp_dir):
            mkdir(self.tmp_dir)

        self.original_dir = getcwd()
        chdir(self.tmp_dir)

        with open("isomap.sp", "w") as f:
            f.write(
                f"{self.command}\nmaterialtestbystrainhistory 1 strain_history\nexit\n"
            )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.original_dir:
            chdir(self.original_dir)

        return False

    def _generate_base(self, center: tuple[int, int], resolution: int):
        deformation = np.zeros((resolution, 6))
        deformation[:, 0] = np.linspace(
            0, center[0] * self.ref_strain, resolution + 1, endpoint=True
        )[1:]
        deformation[:, 1] = np.linspace(
            0, center[1] * self.ref_strain, resolution + 1, endpoint=True
        )[1:]
        return deformation

    def _generate_increment(self, dx: float, dy: float):
        increment = np.zeros((self.resolution, 6))
        increment[:, 0] = np.linspace(
            0, dx * self.ref_strain, self.resolution + 1, endpoint=True
        )[1:]
        increment[:, 1] = np.linspace(
            0, dy * self.ref_strain, self.resolution + 1, endpoint=True
        )[1:]
        return increment

    def _run_analysis(self, strain_history: np.ndarray):
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
            raise RuntimeError(result.stdout)

        while not exists("RESULT.txt"):
            sleep(0.01)

        return np.loadtxt("RESULT.txt")[-1, :]

    def _generate_figure(
        self, x_grid: np.ndarray, y_grid: np.ndarray, grid: np.ndarray
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
        plt.title(
            f"{self.material_name.upper()} Absolute Error (unit: % of $\\sigma_\\text{{ref}}$)"
        )
        fig.text(
            0,
            0,
            f"{self.command}\ncenter: ({self.base_deformation[-1, 0]:.4e}, {self.base_deformation[-1, 1]:.4e}), reference strain $\\varepsilon_\\text{{ref}}$: {self.ref_strain:.4e}, reference stress $\\sigma_\\text{{ref}}$: {self.ref_stress:.4e}",
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

    def contour(self, title: str = "", *, center: tuple[int, int], size: int):
        self.base_deformation = self._generate_base(center, self.base_resolution)

        contour_size = self.contour_samples
        region = (
            np.array(range(-contour_size, contour_size + 1))
            * size
            / float(contour_size)
        )
        num_points = len(region)
        error_grid = np.zeros((num_points, num_points))

        counter = 0
        for i in range(num_points):
            for j in range(num_points):
                counter += 1
                print(f"Contouring {counter}/{error_grid.size}...")

                increment = (
                    self._generate_increment(region[i], region[j])
                    + self.base_deformation[-1, :]
                )
                reference = self._run_analysis(
                    np.vstack((self.base_deformation, increment))
                )
                coarse = self._run_analysis(
                    np.vstack((self.base_deformation, increment[-1, :]))
                )

                error_grid[i, j] = (
                    100 * self._norm(coarse - reference) / self.ref_stress
                )

        ex_grid, ey_grid = np.meshgrid(region, region)
        fig = self._generate_figure(ex_grid, ey_grid, error_grid)
        full_title = f"{title or self.material_name}.abs.error"
        fig.savefig(f"{full_title}.pdf")
        fig.savefig(f"{full_title}.svg")


if __name__ == "__main__":
    pass
