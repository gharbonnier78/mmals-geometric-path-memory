"""Path-sensitive geometry utilities for quantum and continual-learning labs."""

from .geometry import (
    amplitude_damping_channel,
    apply_unitary,
    bloch_to_density,
    commutator_norm,
    density_to_bloch,
    discrete_uhlmann_transport,
    lyapunov_generator,
    normalize_psd,
    tangent_normal_decomposition,
    trace_distance,
    von_neumann_entropy,
)

__all__ = [
    "amplitude_damping_channel",
    "apply_unitary",
    "bloch_to_density",
    "commutator_norm",
    "density_to_bloch",
    "discrete_uhlmann_transport",
    "lyapunov_generator",
    "normalize_psd",
    "tangent_normal_decomposition",
    "trace_distance",
    "von_neumann_entropy",
]
