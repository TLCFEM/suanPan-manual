import dataclasses
import os
import shutil
import subprocess
from itertools import cycle

import h5py
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress


def get_line_style():
    ls_tuple = [
        ("solid", (0, ())),
        ("loosely dotted", (0, (1, 4))),
        ("dotted", (0, (1, 2))),
        ("densely dotted", (0, (1, 1))),
        ("loosely dashed", (0, (5, 4))),
        ("dashed", (0, (5, 2))),
        ("densely dashed", (0, (5, 1))),
        ("loosely dashdotted", (0, (3, 4, 1, 4))),
        ("dashdotted", (0, (3, 2, 1, 2))),
        ("densely dashdotted", (0, (3, 1, 1, 1))),
        ("loosely dashdotdotted", (0, (3, 4, 1, 4, 1, 4))),
        ("dashdotdotted", (0, (3, 2, 1, 2, 1, 2))),
        ("densely dashdotdotted", (0, (3, 1, 1, 1, 1, 1))),
    ]

    for v in cycle(ls_tuple):
        yield v[1]


LS = get_line_style()


def get_line_color():
    color_tuple = ["r", "g", "b"]

    for v in cycle(color_tuple):
        yield v


LC = get_line_color()

template = """
node 1 0 0
node 2 1 0

material Elastic1D 1 5

element T2D2 1 1 2 1 1
element Mass 2 2 1 1

fix2 1 1 1
fix2 2 2 1 2

hdf5recorder 1 Node U 2
hdf5recorder 2 Node V 2
hdf5recorder 3 Node A 2

initial displacement 1 1 2
initial acceleration -5 1 2

modifier Rayleigh 1 0 0 0 0.01 1

step {analysis_type} 1 2
set ini_step_size {time_step}
set fixed_step_size 1

{integrator_command}

converger AbsIncreDisp 2 1E-14 10 0

analyze

save recorder 1 2 3

terminal mv R1-U.h5 R1-U-{time_step}.h5
terminal mv R2-V.h5 R2-V-{time_step}.h5
terminal mv R3-A.h5 R3-A-{time_step}.h5

exit
"""


@dataclasses.dataclass
class Response:
    time: np.ndarray
    u: np.ndarray
    u_error: np.ndarray
    v: np.ndarray
    v_error: np.ndarray
    a: np.ndarray
    a_error: np.ndarray


matplotlib.rcParams.update({"font.size": 6})


def analytical(para):
    def system(m, k, c):
        omega_n = np.sqrt(k / m)
        zeta = c / (2 * np.sqrt(k * m))

        omega_d = omega_n * np.sqrt(1 - zeta**2)

        A = 1  # u0
        B = (0 + zeta * omega_n * 1) / omega_d

        def oscillator(t):
            exp_term = np.exp(-zeta * omega_n * t)
            cos_term = np.cos(omega_d * t)
            sin_term = np.sin(omega_d * t)

            x = A * cos_term + B * sin_term
            x_dot = -A * omega_d * sin_term + B * omega_d * cos_term
            x_dot_dot = -A * omega_d**2 * cos_term - B * omega_d**2 * sin_term

            return (
                exp_term * x,
                exp_term * (x_dot - zeta * omega_n * x),
                exp_term
                * (x_dot_dot - zeta * omega_n * (2 * x_dot - zeta * omega_n * x)),
            )

        return oscillator

    oscillator = system(*para)
    t = 10
    dt = 0.01
    x = np.linspace(0, t, int(t / dt) + 1)
    u = np.zeros(len(x))
    v = np.zeros(len(x))
    a = np.zeros(len(x))
    for i in range(len(x)):
        u[i], v[i], a[i] = oscillator(x[i])

    plt.plot(x, u, next(LC), label="analytical u", linewidth=0.5)
    plt.plot(x, v, next(LC), label="analytical v", linewidth=0.5)
    plt.plot(x, a, next(LC), label="analytical a", linewidth=0.5)

    return oscillator


results = {}


def numerical(vibrator, pick):
    def read_h5(name):
        with h5py.File(f"{name}-{str(pick)}.h5", "r") as f:
            data = f[f"/{name}/{name}2"]
            return data[:, 0], data[:, 1]

    time, u = read_h5("R1-U")
    _, v = read_h5("R2-V")
    _, a = read_h5("R3-A")

    ref_u = np.zeros(len(time))
    ref_v = np.zeros(len(time))
    ref_a = np.zeros(len(time))
    for i in range(len(time)):
        ref_u[i], ref_v[i], ref_a[i] = vibrator(time[i])

    results[pick] = Response(
        time, u, np.abs(ref_u - u), v, np.abs(ref_v - v), a, np.abs(ref_a - a)
    )


def run(config):
    title, analysis_type, integrator_command = config

    print(f"Running {title}...")

    time_steps = [0.001, 0.002, 0.005, 0.01]

    for t in time_steps:
        with open("tester.sp", "w") as f:
            f.write(
                template.format(
                    analysis_type=analysis_type,
                    integrator_command=integrator_command,
                    time_step=t,
                )
            )

        subprocess.run(
            ["suanpan", "-np", "-f", "tester.sp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    fig = plt.figure(figsize=(6, 5))
    plt.suptitle(title, fontsize=8)

    fig.add_subplot(311)

    m = 1
    k = 5
    c = 0.01 * k
    sdof = analytical([m, k, c])
    for t in time_steps:
        numerical(sdof, t)

    for key, value in results.items():
        for x in [value.u, value.v, value.a]:
            plt.plot(
                value.time,
                x,
                label=f"$\\Delta{{}}t=${key:1.0E}",
                linestyle=next(LS),
                color=next(LC),
                linewidth=0.8,
            )

    plt.legend(loc="lower right", ncol=2)
    plt.xlabel("time (s)")
    plt.ylabel("$u/v/a$")
    plt.grid(which="both", linestyle="--", linewidth=0.2)
    plt.xlim(0, 2)

    fig.add_subplot(3, 1, 2)

    error_x = []
    error_u = []
    error_v = []
    error_a = []
    for key, value in results.items():
        error_x.append(key)
        error_u.append(np.max(value.u_error))
        error_v.append(np.max(value.v_error))
        error_a.append(np.max(value.a_error))

    for x in [error_u, error_v, error_a]:
        result = linregress(np.log(error_x), np.log(x))
        plt.loglog(
            error_x,
            np.exp(result[1]) * np.power(error_x, result[0]),
            next(LC) + "--",
            label=f"slope {result[0]:.3f} $r^2=${result[2] ** 2:.3f}",
        )
        plt.loglog(error_x, x, "o")
    plt.grid(which="both", linestyle="--", linewidth=0.2)
    plt.legend()
    plt.xlabel(r"$\Delta{}t$ (s)")
    plt.ylabel("absolute error $\\epsilon$")

    fig.add_subplot(3, 1, 3)

    for key, value in results.items():
        for x in [value.u_error, value.v_error, value.a_error]:
            plt.plot(
                value.time,
                x,
                label=f"$\\Delta{{}}t=${float(key):1.0E}",
                linestyle=next(LS),
                color=next(LC),
                linewidth=0.8,
            )

    plt.yscale("log")
    plt.legend(loc="lower right", ncol=2)
    plt.xlabel("time (s)")
    plt.ylabel("absolute error $\\epsilon$")
    plt.grid(which="both", linestyle="--", linewidth=0.2)
    plt.xlim(1, 2)

    fig.text(
        0,
        0,
        "SDOF, max history as error, $k=5$, $m=1$, $c=0.05$, $u_0=1$, $v_0=0$, $a_0=-5$",
        fontsize=4,
        ha="left",
        va="bottom",
    )

    fig.tight_layout(pad=0.1)
    formatted_title = title.lower().replace(" ", "-")
    fig.savefig(f"{formatted_title}.pdf")
    fig.savefig(f"{formatted_title}.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    if not shutil.which("suanpan"):
        print("suanpan command not found.")
        exit(1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    for config in [
        ("Newmark Default", "dynamic", "integrator Newmark 1"),
        (
            "Newmark Linear Acceleration",
            "dynamic",
            "integrator Newmark 1 0.166666666666666666 0.5",
        ),
        ("OALTS 1.0", "dynamic", "integrator OALTS 1 1"),
        ("OALTS 0.5", "dynamic", "integrator OALTS 1 0.5"),
        ("OALTS 0.0", "dynamic", "integrator OALTS 1 0"),
        ("BatheTwoStep 1.0", "dynamic", "integrator BatheTwoStep 1"),
        ("BatheTwoStep 0.5", "dynamic", "integrator BatheTwoStep 1 0.5"),
        ("BatheTwoStep 0.0", "dynamic", "integrator BatheTwoStep 1 0.0"),
        ("GeneralizedAlpha 1.0", "dynamic", "integrator GeneralizedAlpha 1 1.0"),
        ("GeneralizedAlpha 0.5", "dynamic", "integrator GeneralizedAlpha 1 0.5"),
        ("GeneralizedAlpha 0.0", "dynamic", "integrator GeneralizedAlpha 1 0.0"),
        ("GSSSS Optimal 1.0", "dynamic", "integrator GSSSSOptimal 1 1.0"),
        ("GSSSS Optimal 0.5", "dynamic", "integrator GSSSSOptimal 1 0.5"),
        ("GSSSS Optimal 0.0", "dynamic", "integrator GSSSSOptimal 1 0.0"),
        ("GSSSS U0 1.0", "dynamic", "integrator GSSSSU0 1 1. 1. 1."),
        ("GSSSS U0 0.5", "dynamic", "integrator GSSSSU0 1 1. .5 .5"),
        ("GSSSS U0 0.0", "dynamic", "integrator GSSSSU0 1 1. 0. 0."),
        ("GSSSS V0 1.0", "dynamic", "integrator GSSSSV0 1 1. 1. 1."),
        ("GSSSS V0 0.5", "dynamic", "integrator GSSSSV0 1 1. .5 .5"),
        ("GSSSS V0 0.0", "dynamic", "integrator GSSSSV0 1 1. 0. 0."),
        ("BatheExplicit 1.0", "explicitdynamic", "integrator BatheExplicit 1 1.0"),
        ("BatheExplicit 0.5", "explicitdynamic", "integrator BatheExplicit 1 0.5"),
        ("BatheExplicit 0.0", "explicitdynamic", "integrator BatheExplicit 1 0.0"),
        (
            "GeneralizedAlphaExplicit 1.0",
            "explicitdynamic",
            "integrator GeneralizedAlphaExplicit 1 1.0",
        ),
        (
            "GeneralizedAlphaExplicit 0.0",
            "explicitdynamic",
            "integrator GeneralizedAlphaExplicit 1 0.0",
        ),
        (
            "GeneralizedAlphaExplicit 0.5",
            "explicitdynamic",
            "integrator GeneralizedAlphaExplicit 1 0.5",
        ),
        ("GSSE 1.0", "explicitdynamic", "integrator GSSE 1 1.0"),
        ("GSSE 0.5", "explicitdynamic", "integrator GSSE 1 0.5"),
        ("GSSE 0.0", "explicitdynamic", "integrator GSSE 1 0.0"),
        ("ICL 1.0", "explicitdynamic", "integrator ICL 1 1.0"),
        ("ICL 0.5", "explicitdynamic", "integrator ICL 1 0.5"),
    ]:
        run(config)
