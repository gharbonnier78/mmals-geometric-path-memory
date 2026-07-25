"""Run the core numerical smoke checks without opening notebooks."""

from __future__ import annotations

import numpy as np

from mmals_path_memory import (
    amplitude_damping_channel,
    apply_unitary,
    bloch_to_density,
    density_to_bloch,
    trace_distance,
)
from mmals_path_memory.mmals import diagnose_transition


def main() -> None:
    rho = bloch_to_density([0.55, 0.25, -0.10])
    theta = np.deg2rad(55)
    ux = np.array(
        [
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)],
        ],
        dtype=complex,
    )
    ab = amplitude_damping_channel(apply_unitary(rho, ux), 0.35)
    ba = apply_unitary(amplitude_damping_channel(rho, 0.35), ux)
    print("A -> B Bloch:", density_to_bloch(ab))
    print("B -> A Bloch:", density_to_bloch(ba))
    print("Order gap:", trace_distance(ab, ba))
    print("Transition diagnosis:", diagnose_transition(rho, ab))


if __name__ == "__main__":
    main()
