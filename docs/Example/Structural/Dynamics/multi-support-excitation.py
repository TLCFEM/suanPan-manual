import dataclasses
import os
import shutil
import subprocess
from itertools import cycle

import h5py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt

matplotlib.rcParams.update({"font.size": 6})


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


template = """
node 1 0 0
node 2 0 1
material Elastic1D 1 100
section Rectangle2D 1 12 1 1
element B21 1 1 2 1 6
element MassPoint2D 2 1 11 11
element MassPoint2D 3 2 22 22
fix2 1 2 1
fix2 2 3 1
amplitude Tabular 1 random
supportacceleration 2 1 .2 1 1
hdf5recorder 1 Node U1 1 2
hdf5recorder 2 Node A1 1 2
step {analysis_type} 1 2
set ini_step_size 2.5E-3
set fixed_step_size true
set linear_system true
integrator {integrator_command}
converger AbsIncreAcc 1 1E-10 4 0
analyze
save recorder 1 2
exit
"""


@dataclasses.dataclass
class Response:
    time: np.ndarray
    a1: np.ndarray
    u2: np.ndarray


data = None


def numerical():
    def read_h5(name):
        with h5py.File(f"{name}.h5", "r") as f:
            data1 = f[f"/{name}/{name}1"]
            data2 = f[f"/{name}/{name}2"]
            return data1[:, 0], data1[:, 1], data2[:, 1]

    time, _, u2 = read_h5("R1-U1")
    _, a1, _ = read_h5("R2-A1")

    interp_func = interp1d(data[:, 0], data[:, 1], bounds_error=False, fill_value=0)

    return Response(time, a1 - 0.2 * interp_func(time), u2)


def amplitude():
    duration = 10
    dt = 0.01
    t = np.arange(0, duration, dt)

    np.random.seed(42)

    def bandpass_filter(data, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype="band")
        return filtfilt(b, a, data)

    filtered_signal = bandpass_filter(
        np.random.normal(0, 1, len(t)), 0.1, 10, fs=1 / dt
    )

    global data
    data = np.column_stack(
        (
            t,
            np.exp(-((t - duration / 2) ** 2) / (2 * (duration / 5) ** 2))
            * filtered_signal,
        )
    )
    data[0, 1] = 0.0

    np.savetxt("random", data, fmt="%.2f %.16f", comments="")


results = {}


def run(config):
    title, analysis_type, integrator_command = config

    print(f"Running {title}...")

    with open("tester.sp", "w") as f:
        f.write(
            template.format(
                analysis_type=analysis_type,
                integrator_command=integrator_command,
            )
        )

    subprocess.run(["suanpan", "-np", "-f", "tester.sp"])

    results[title] = numerical()


if __name__ == "__main__":
    if not shutil.which("suanpan"):
        print("suanpan command not found.")
        exit(1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    amplitude()

    configs = [
        ("Newmark Default", "dynamic", "Newmark 1"),
        (
            "Newmark Linear Acceleration",
            "dynamic",
            "Newmark 1 0.166666666666666666 0.5",
        ),
        ("OALTS 1.0", "dynamic", "OALTS 1 1"),
        ("OALTS 0.5", "dynamic", "OALTS 1 0.5"),
        ("OALTS 0.0", "dynamic", "OALTS 1 0"),
        ("BatheTwoStep 1.0", "dynamic", "BatheTwoStep 1"),
        ("BatheTwoStep 0.5", "dynamic", "BatheTwoStep 1 0.5"),
        ("BatheTwoStep 0.0", "dynamic", "BatheTwoStep 1 0.0"),
        ("GeneralizedAlpha 1.0", "dynamic", "GeneralizedAlpha 1 1.0"),
        ("GeneralizedAlpha 0.5", "dynamic", "GeneralizedAlpha 1 0.5"),
        ("GeneralizedAlpha 0.0", "dynamic", "GeneralizedAlpha 1 0.0"),
        ("GSSSS Optimal 1.0", "dynamic", "GSSSSOptimal 1 1.0"),
        ("GSSSS Optimal 0.5", "dynamic", "GSSSSOptimal 1 0.5"),
        ("GSSSS Optimal 0.0", "dynamic", "GSSSSOptimal 1 0.0"),
        ("BatheExplicit 1.0", "explicitdynamic", "BatheExplicit 1 1.0"),
        ("BatheExplicit 0.5", "explicitdynamic", "BatheExplicit 1 0.5"),
        ("BatheExplicit 0.0", "explicitdynamic", "BatheExplicit 1 0.0"),
        ("ICL 1.0", "explicitdynamic", "ICL 1 1.0"),
        ("ICL 0.5", "explicitdynamic", "ICL 1 0.5"),
        (
            "GeneralizedAlphaExplicit 1.0",
            "explicitdynamic",
            "GeneralizedAlphaExplicit 1 1.0",
        ),
        # extrapolate # (
        # extrapolate #     "GeneralizedAlphaExplicit 0.5",
        # extrapolate #     "explicitdynamic",
        # extrapolate #     "GeneralizedAlphaExplicit 1 0.5",
        # extrapolate # ),
        # extrapolate # (
        # extrapolate #     "GeneralizedAlphaExplicit 0.0",
        # extrapolate #     "explicitdynamic",
        # extrapolate #     "GeneralizedAlphaExplicit 1 0.0",
        # extrapolate # ),
        ("GSSE 1.0", "explicitdynamic", "GSSE 1 1.0"),
        ("GSSE 0.5", "explicitdynamic", "GSSE 1 0.5"),
        # extrapolate # ("GSSE 0.0", "explicitdynamic", "GSSE 1 0.0"),
        # extrapolate # ("WAT2 1.0", "explicitdynamic", "WAT2 1 1.0"),
        ("WAT2 Default", "explicitdynamic", "WAT2 1"),
        ("WAT2 0.0", "explicitdynamic", "WAT2 1 0.0"),
    ]

    for config in configs:
        run(config)

    fig = plt.figure(figsize=(6, 6))

    fig.add_subplot(211)

    for key, value in results.items():
        plt.plot(
            value.time,
            value.u2,
            label=key,
            linestyle=next(LS),
            linewidth=0.8,
        )

    plt.legend(ncol=3, fontsize=4)
    plt.xlabel("time (s)")
    plt.ylabel("displacement (free end)")
    plt.grid(which="both", linestyle="--", linewidth=0.2)
    plt.xlim(0, 2)

    fig.add_subplot(212)

    for key, value in results.items():
        plt.plot(
            value.time,
            np.abs(value.a1),
            label=key,
            linestyle=next(LS),
            linewidth=0.8,
        )

    plt.legend(ncol=3, fontsize=4)
    plt.xlabel("time (s)")
    plt.ylabel("absolute acceleration error (fixed end)")
    plt.grid(which="both", linestyle="--", linewidth=0.2)
    plt.xlim(0, 2)
    plt.yscale("log")

    fig.text(
        0,
        0,
        "Ground motion applied via support acceleration at the fixed end. Extrapolating schemes excluded.",
        horizontalalignment="left",
        verticalalignment="bottom",
        fontsize=4,
    )

    fig.tight_layout(pad=0.1)
    formatted_title = "multi-support-excitation-validation"
    fig.savefig(f"{formatted_title}.pdf")
    fig.savefig(f"{formatted_title}.svg", format="svg")
    plt.close(fig)
