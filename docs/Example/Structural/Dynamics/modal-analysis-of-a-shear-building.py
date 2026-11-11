"""Post-processing and validation for the ten-storey shear building example.

The script reads the modal data written by the ``Modal`` recorder and
independently reconstructs the eigenproblem with NumPy/SciPy.  It then uses the
same modal data to reproduce a response history analysis and to perform an
SRSS/CQC modal combination.

If ``suanPan`` is available in ``PATH``, the script runs the two models first.
Otherwise, run them manually from this directory before executing the script:

    suanPan -np -f shear-building.supan
    suanPan -np -f shear-building-rha.supan
"""

import subprocess
from pathlib import Path
from shutil import which

import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh

BASE = Path(__file__).resolve().parent

N_FLOOR = 10
FLOOR_MASS = 10.0  # t
STOREY_STIFFNESS = 4.0e4  # kN/m

MODAL_FILE = BASE / "R1-Modal.h5"
RHA_FILE = BASE / "R2-U1.h5"
GROUND_MOTION_FILE = BASE / "ground_motion.txt"

GAL_TO_SI = 0.01  # the record is in gal, 1 gal = 0.01 m/s^2


# ---------------------------------------------------------------------------
# optional execution of suanPan
# ---------------------------------------------------------------------------
def run_suanpan() -> None:
    executable = which("suanPan") or which("suanpan") or which("sp")
    if executable is None:
        return
    for script in ("shear-building.supan", "shear-building-rha.supan"):
        if (BASE / script).exists():
            subprocess.run(
                [executable, "-np", "-f", str(BASE / script)],
                check=True,
                cwd=BASE,
            )


# ---------------------------------------------------------------------------
# explicit finite element matrices
# ---------------------------------------------------------------------------
def system_matrices():
    stiffness = STOREY_STIFFNESS * (
        2.0 * np.eye(N_FLOOR) - np.eye(N_FLOOR, k=1) - np.eye(N_FLOOR, k=-1)
    )
    stiffness[-1, -1] = STOREY_STIFFNESS
    mass = FLOOR_MASS * np.eye(N_FLOOR)
    return stiffness, mass


# ---------------------------------------------------------------------------
# modal data stored by the Modal recorder
# ---------------------------------------------------------------------------
def read_modal_data():
    with h5py.File(MODAL_FILE, "r") as file:
        frequency = file["Frequency"][()].ravel()
        participation = file["U1/ParticipationFactor"][()].ravel()
        effective_mass = file["U1/EffectiveMass"][()].ravel()

        # Node 2 is the first floor, Node 11 the roof.  A two-dimensional node
        # stores [U1, U2]; U1 is therefore the first entry of each N dataset.
        shape = np.zeros((N_FLOOR, frequency.size))
        force = np.zeros((N_FLOOR, frequency.size))
        for mode in range(frequency.size):
            for floor, node in enumerate(range(2, 2 + N_FLOOR)):
                shape[floor, mode] = file[f"Mode {mode + 1}/N{node}"][()].ravel()[0]
                force[floor, mode] = file[f"Mode {mode + 1}/F{node}"][()].ravel()[0]

    return frequency, shape, participation, effective_mass, force


# ---------------------------------------------------------------------------
# SDOF response and response spectrum
# ---------------------------------------------------------------------------
def newmark_sdof(omega, zeta, acceleration, dt):
    """Constant-average-acceleration Newmark solution of

        d'' + 2 zeta omega d' + omega^2 d = -a_g(t)

    with zero initial conditions.  Returns displacement, velocity and
    acceleration histories.
    """
    stiffness = omega**2
    damping = 2.0 * zeta * omega
    gamma, beta = 0.5, 0.25

    displacement = np.zeros_like(acceleration)
    velocity = np.zeros_like(acceleration)
    accel = np.zeros_like(acceleration)
    accel[0] = acceleration[0]

    effective_stiffness = (
        stiffness + gamma / (beta * dt) * damping + 1.0 / (beta * dt**2)
    )

    for i in range(1, acceleration.size):
        effective_load = (
            acceleration[i]
            + displacement[i - 1] / (beta * dt**2)
            + velocity[i - 1] / (beta * dt)
            + (1.0 / (2.0 * beta) - 1.0) * accel[i - 1]
            + damping
            * (
                gamma / (beta * dt) * displacement[i - 1]
                + (gamma / beta - 1.0) * velocity[i - 1]
                + dt * (gamma / (2.0 * beta) - 1.0) * accel[i - 1]
            )
        )
        displacement[i] = effective_load / effective_stiffness
        accel[i] = (
            (displacement[i] - displacement[i - 1]) / (beta * dt**2)
            - velocity[i - 1] / (beta * dt)
            - (1.0 / (2.0 * beta) - 1.0) * accel[i - 1]
        )
        velocity[i] = velocity[i - 1] + dt * (
            (1.0 - gamma) * accel[i - 1] + gamma * accel[i]
        )

    return displacement, velocity, accel


def cqc_correlation(omega, zeta):
    rho = np.eye(omega.size)
    for j in range(omega.size):
        for k in range(j + 1, omega.size):
            wj, wk = omega[j], omega[k]
            zj, zk = zeta[j], zeta[k]
            numerator = 8.0 * np.sqrt(zj * zk) * (wj * wk) ** 1.5 * (zj * wj + zk * wk)
            denominator = (
                (wj**2 - wk**2) ** 2
                + 4.0 * zj * zk * wj * wk * (wj**2 + wk**2)
                + 4.0 * (zj**2 + zk**2) * wj**2 * wk**2
            )
            rho[j, k] = rho[k, j] = numerator / denominator
    return rho


def read_rha():
    with h5py.File(RHA_FILE, "r") as file:
        group = file["R2-U1"]
        time = group["R2-U12"][()][:, 0]
        displacement = np.column_stack(
            [group[f"R2-U1{node}"][()][:, 1] for node in range(2, 2 + N_FLOOR)]
        )
    return time, displacement


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    run_suanpan()

    stiffness, mass = system_matrices()
    eigenvalues, eigenvectors = eigh(stiffness, mass)
    omega = np.sqrt(eigenvalues)
    frequency_exact = omega / (2.0 * np.pi)

    frequency, shape, participation, effective_mass, force = read_modal_data()

    # ------------------------------------------------------------------
    # 1. validate modal properties against the explicit eigenproblem
    # ------------------------------------------------------------------
    frequency_error = np.max(np.abs(frequency - frequency_exact) / frequency_exact)
    orthogonality_error = np.max(np.abs(shape.T @ mass @ shape - np.eye(N_FLOOR)))

    influence = np.ones(N_FLOOR)
    participation_exact = shape.T @ mass @ influence
    effective_mass_exact = participation_exact**2

    participation_error = np.max(np.abs(participation - participation_exact))
    effective_mass_error = np.max(np.abs(effective_mass - effective_mass_exact))

    force_exact = stiffness @ shape
    force_error = np.max(np.abs(force - force_exact)) / np.max(np.abs(force_exact))

    # eigenvectors are only defined up to a sign
    sign_error = 0.0
    for mode in range(N_FLOOR):
        exact = eigenvectors[:, mode]
        sign_error = max(
            sign_error,
            min(
                np.max(np.abs(shape[:, mode] - exact)),
                np.max(np.abs(shape[:, mode] + exact)),
            ),
        )

    print("Modal property validation")
    print(f"  maximum relative frequency error       : {frequency_error:.3e}")
    print(f"  maximum |Phi^T M Phi - I|              : {orthogonality_error:.3e}")
    print(f"  maximum mode-shape difference          : {sign_error:.3e}")
    print(f"  maximum participation-factor error     : {participation_error:.3e}")
    print(f"  maximum effective-mass error           : {effective_mass_error:.3e}")
    print(f"  maximum force-response error           : {force_error:.3e}")
    print(
        f"  sum of effective masses / total mass   : "
        f"{effective_mass.sum() / mass.sum():.9f}"
    )

    # ------------------------------------------------------------------
    # 2. modal superposition and modal combination
    # ------------------------------------------------------------------
    ground_motion = np.loadtxt(GROUND_MOTION_FILE)
    ground_time = ground_motion[:, 0]
    ground_acceleration = ground_motion[:, 1] * GAL_TO_SI

    # The Rayleigh damping in the model is fitted to 5% at modes 1 and 3.
    target_damping = 0.05
    first, third = 0, 2
    rayleigh_b = 2.0 * target_damping / (omega[first] + omega[third])
    rayleigh_a = rayleigh_b * omega[first] * omega[third]
    damping_ratio = rayleigh_a / (2.0 * omega) + rayleigh_b * omega / 2.0

    dt = 0.01
    time = np.arange(0.0, ground_time[-1] + dt / 2.0, dt)
    acceleration = np.interp(time, ground_time, ground_acceleration)

    modal_coordinate = np.zeros((N_FLOOR, time.size))
    spectral_displacement = np.zeros(N_FLOOR)
    for mode in range(N_FLOOR):
        # modal equation: q'' + 2 zeta omega q' + omega^2 q = -Gamma a_g
        modal_coordinate[mode], _, _ = newmark_sdof(
            omega[mode], damping_ratio[mode], -participation[mode] * acceleration, dt
        )
        # unit-mass SDOF response used for the response spectrum
        unit_response, _, _ = newmark_sdof(
            omega[mode], damping_ratio[mode], -acceleration, dt
        )
        spectral_displacement[mode] = np.max(np.abs(unit_response))

    displacement_modal = shape @ modal_coordinate

    rha_time, displacement_rha = read_rha()
    common = min(time.size, rha_time.size)
    history_error = np.max(
        np.abs(displacement_modal[:, :common] - displacement_rha[:common].T)
    ) / np.max(np.abs(displacement_rha))

    # peak modal contributions
    modal_peak = shape * (participation * spectral_displacement)
    srss = np.sqrt(np.sum(modal_peak**2, axis=1))
    rho = cqc_correlation(omega, damping_ratio)
    cqc = np.sqrt(np.einsum("fm,mn,fn->f", modal_peak, rho, modal_peak))

    peak_rha = np.max(np.abs(displacement_rha), axis=0)
    srss_error = np.max(np.abs(srss - peak_rha) / peak_rha)
    cqc_error = np.max(np.abs(cqc - peak_rha) / peak_rha)

    # base shear: the first storey spring connects the base and the first floor
    base_shear_rha = STOREY_STIFFNESS * displacement_rha[:, 0]
    modal_base_shear = participation**2 * omega**2 * spectral_displacement
    base_shear_srss = np.sqrt(np.sum(modal_base_shear**2))
    base_shear_cqc = np.sqrt(modal_base_shear @ rho @ modal_base_shear)

    print("\nResponse history validation")
    print(f"  modal superposition vs direct RHA     : {history_error:.3e}")
    print(
        "  peak roof displacement, RHA / SRSS / CQC: "
        f"{peak_rha[-1]:.6e} / {srss[-1]:.6e} / {cqc[-1]:.6e}"
    )
    print(f"  maximum SRSS peak error               : {srss_error:.3%}")
    print(f"  maximum CQC peak error                : {cqc_error:.3%}")
    print(
        "  base shear, RHA / SRSS / CQC          : "
        f"{np.max(np.abs(base_shear_rha)):.6e} / "
        f"{base_shear_srss:.6e} / {base_shear_cqc:.6e}"
    )

    # ------------------------------------------------------------------
    # 3. figures
    # ------------------------------------------------------------------
    heights = np.arange(1, N_FLOOR + 1)

    fig, ax = plt.subplots(figsize=(4.0, 4.5), dpi=150)
    for mode in range(3):
        ax.plot(shape[:, mode], heights, marker="o", label=f"Mode {mode + 1}")
    ax.axvline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("mass-normalised mode shape")
    ax.set_ylabel("floor")
    ax.set_yticks(heights)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE / "modal-analysis-of-a-shear-building-modes.svg")
    plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(9.0, 4.0), dpi=150)
    ax[0].plot(peak_rha, heights, "k-", marker="o", label="direct RHA")
    ax[0].plot(srss, heights, "C0--", marker="s", label="SRSS")
    ax[0].plot(cqc, heights, "C3-.", marker="^", label="CQC")
    ax[0].set_xlabel("peak floor displacement")
    ax[0].set_ylabel("floor")
    ax[0].legend()
    ax[1].plot(
        rha_time[:common],
        displacement_rha[:common, -1],
        "k-",
        label="direct RHA",
    )
    ax[1].plot(
        time[:common],
        displacement_modal[-1, :common],
        "C0--",
        label="modal superposition",
    )
    ax[1].set_xlabel("time / s")
    ax[1].set_ylabel("roof displacement")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(BASE / "modal-analysis-of-a-shear-building-combination.svg")
    plt.close(fig)


if __name__ == "__main__":
    main()
