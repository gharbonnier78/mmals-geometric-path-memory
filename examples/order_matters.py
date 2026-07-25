"""Minimal example: a unitary rotation and amplitude damping do not generally commute."""

import numpy as np

from mmals_path_memory import (
    amplitude_damping_channel,
    apply_unitary,
    bloch_to_density,
    density_to_bloch,
    trace_distance,
)

rho0 = bloch_to_density([0.55, 0.25, -0.10])
theta = np.deg2rad(55)
ux = np.array(
    [
        [np.cos(theta / 2), -1j * np.sin(theta / 2)],
        [-1j * np.sin(theta / 2), np.cos(theta / 2)],
    ],
    dtype=complex,
)

rotation_then_damping = amplitude_damping_channel(apply_unitary(rho0, ux), 0.35)
damping_then_rotation = apply_unitary(amplitude_damping_channel(rho0, 0.35), ux)

print("R -> D:", density_to_bloch(rotation_then_damping))
print("D -> R:", density_to_bloch(damping_then_rotation))
print("Order gap (trace distance):", trace_distance(rotation_then_damping, damping_then_rotation))
