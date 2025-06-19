import subprocess
from genericpath import exists
from os import chdir, getcwd, mkdir, remove
from shutil import which
from time import sleep

import numpy as np
from matplotlib import pyplot as plt


try:
    from rich.progress import track

    has_rich = True
except ImportError:
    has_rich = False


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
        contour_samples: int = 40,
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
            contour_samples (int, optional): The number of samples for contour calculation. Defaults to 40.
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

    def _generate_base(self, center: int, resolution: int):
        base = np.linspace(0, center * self.ref_strain, resolution + 1, endpoint=True)
        return base[1:]

    def _generate_increment(self, dx: float):
        incre = np.linspace(0, dx * self.ref_strain, self.resolution + 1, endpoint=True)
        return incre[1:]

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

        return np.loadtxt("RESULT.txt")[-1]

    def _generate_figure(self, x, y):
        fig = plt.figure(figsize=(7.5, 7))
        plt.plot(x, y)
        plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon_{\\text{ref}}$")
        plt.ylabel("$\\Delta{}\\sigma_y/\\sigma_{\\text{ref}}$")
        plt.title(f"{self.material_name.upper()} Absolute Error")
        fig.text(
            0,
            0,
            f"{self.command}\ncenter: {self.base_deformation[-1]:.4e}, reference strain $\\varepsilon_\\text{{ref}}$: {self.ref_strain:.4e}, reference stress $\\sigma_\\text{{ref}}$: {self.ref_stress:.4e}",
            fontsize=8,
            va="bottom",
            ha="left",
        )
        plt.tight_layout()
        return fig

    def contour(self, title: str = "", *, center: int, size: int):
        self.base_deformation = self._generate_base(center, self.base_resolution)

        density = self.contour_samples
        region = np.array(range(-density, density + 1)) * size / float(density)
        num_points = len(region)
        error_curve = np.zeros(num_points)

        for i in (
            track(range(num_points), description="Contouring...", transient=True)  # type: ignore
            if has_rich
            else range(num_points)
        ):
            if not has_rich:
                print(f"Contouring {i + 1}/{num_points}...")

            increment = self._generate_increment(region[i]) + self.base_deformation[-1]
            reference = self._run_analysis(
                np.concatenate((self.base_deformation, increment))
            )
            coarse = self._run_analysis(np.append(self.base_deformation, increment[-1]))

            error_curve[i] = 100 * np.fabs(coarse - reference) / self.ref_stress

        fig = self._generate_figure(region, error_curve)
        full_title = f"{title or self.material_name}.abs.error"
        fig.savefig(f"{full_title}.pdf")
        fig.savefig(f"{full_title}.svg")


if __name__ == "__main__":
    pass
