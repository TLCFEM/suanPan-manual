import os
import subprocess
from shutil import which
from time import sleep

import matplotlib.pyplot as plt
import numpy as np

base_num = 200
young_modulus = 1e5
yield_stress = 100.0
hardening_ratio = 0.05


def generate_base(size: float, biaxial: bool = True):
    strain = np.zeros((base_num, 6))
    strain[:, 0] = np.linspace(0, size, strain.shape[0] + 1, endpoint=True)[1:]
    if biaxial:
        strain[:, 1] = strain[:, 0]
    return strain


def generate_increment(dx, dy):
    num = 100
    strain = np.zeros((num, 6))
    strain[:, 0] = np.linspace(0, dx, strain.shape[0] + 1, endpoint=True)[1:]
    strain[:, 1] = np.linspace(0, dy, strain.shape[0] + 1, endpoint=True)[1:]
    return strain


def run_analysis(strain):
    np.savetxt("hist", strain)

    if os.path.exists("RESULT.txt"):
        os.remove("RESULT.txt")

    result = subprocess.run(
        ["suanpan", "-np", "-f", "isomap.sp"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if "[ERROR]" in result.stdout:
        np.savetxt("error", strain)
        raise RuntimeError(f"Error in suanpan: {result.stdout}\n{result.stderr}")

    while not os.path.exists("RESULT.txt"):
        sleep(0.01)

    return np.loadtxt("RESULT.txt")[-1, :]


def figure(x_grid, y_grid, grid):
    plt.figure(figsize=(7, 6))
    contour = plt.contourf(x_grid, y_grid, grid, levels=20, cmap="coolwarm")
    plt.colorbar(contour)
    contour = plt.contour(
        x_grid, y_grid, grid, levels=20, colors="black", linewidths=0.2
    )
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon^i$")
    plt.ylabel("$\\Delta{}\\varepsilon_y/\\varepsilon^i$")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()


def plot(model, biaxial):
    with open("isomap.sp", "w") as f:
        f.write(f"{model}\nmaterialtestbystrainhistory 1 hist\nexit\n")

    def norm(s):
        s = np.square(s)
        s[3:] = 2 * s[3:]
        return np.sqrt(np.sum(s))

    base = generate_base(-2 * yield_stress / young_modulus, biaxial)

    increment = np.array(range(-20, 21)) * 5e-5
    num_points = len(increment)
    ex_grid, ey_grid = np.meshgrid(increment, increment)
    ex_grid *= young_modulus / yield_stress
    ey_grid *= young_modulus / yield_stress

    grid = np.zeros((num_points, num_points))
    abs_grid = np.zeros_like(grid)

    index = 0
    for i in range(num_points):
        for j in range(num_points):
            index += 1
            print(f"{index}/{grid.size}")

            offset = generate_increment(increment[i], increment[j]) + base[-1, :]
            ref_stress = run_analysis(np.vstack((base, offset)))
            coarse_stress = run_analysis(np.vstack((base, offset[-1, :])))

            diff = 100 * norm(ref_stress - coarse_stress)

            grid[i, j] = diff / norm(ref_stress)
            abs_grid[i, j] = diff / yield_stress

    figure(ex_grid, ey_grid, grid)
    plt.title(f"Relative Error (%) {'Biaxial' if biaxial else 'Uniaxial'} Loading")
    title = "rel.error.iso." + ("biaxial" if biaxial else "uniaxial")
    plt.savefig(f"{title}.pdf")
    plt.savefig(f"{title}.svg")

    figure(ex_grid, ey_grid, abs_grid)
    plt.title(
        f"Absolute Error (unit: % of $\\sigma_y$) {'Biaxial' if biaxial else 'Uniaxial'} Loading"
    )
    title = "abs.error.iso." + ("biaxial" if biaxial else "uniaxial")
    plt.savefig(f"{title}.pdf")
    plt.savefig(f"{title}.svg")


if __name__ == "__main__":
    if os.name != "posix":
        print("This script only works on linux.")
        exit(1)

    if not which("suanpan"):
        print("suanPan not found, please install it first.")
        exit(1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    os.chdir("tmp")

    for flag in (True, False):
        plot(
            f"material BilinearJ2 1 {young_modulus} .2 {yield_stress} {hardening_ratio} 0.5",
            flag,
        )
