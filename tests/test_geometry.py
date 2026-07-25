import numpy as np

from mmals_path_memory.geometry import (
    amplitude_damping_channel,
    bloch_to_density,
    discrete_uhlmann_transport,
    normalize_psd,
    tangent_normal_decomposition,
    trace_distance,
    von_neumann_entropy,
)


def test_normalize_psd_trace_and_positivity() -> None:
    matrix = np.array([[2.0, 0.3], [0.3, -0.1]])
    rho = normalize_psd(matrix)
    assert np.isclose(np.trace(rho), 1.0)
    assert np.min(np.linalg.eigvalsh(rho)) > 0


def test_entropy_extremes() -> None:
    pure_like = normalize_psd(np.array([[1.0, 0.0], [0.0, 0.0]]), epsilon=1e-12)
    mixed = np.eye(2) / 2.0
    assert von_neumann_entropy(pure_like) < 1e-8
    assert np.isclose(von_neumann_entropy(mixed), 1.0)


def test_tangent_normal_reconstruct_velocity() -> None:
    rho = np.diag([0.7, 0.3]).astype(complex)
    velocity = np.array([[0.02, 0.1j], [-0.1j, -0.02]], dtype=complex)
    tangent, normal = tangent_normal_decomposition(rho, velocity)
    assert np.allclose(tangent + normal, velocity)
    assert np.allclose(np.diag(tangent), 0.0)
    assert np.allclose(normal - np.diag(np.diag(normal)), 0.0)


def test_channel_order_can_matter() -> None:
    rho = bloch_to_density([0.55, 0.25, -0.10])
    theta = 0.9
    unitary = np.array(
        [
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)],
        ]
    )
    first = amplitude_damping_channel(unitary @ rho @ unitary.conj().T, 0.35)
    damped = amplitude_damping_channel(rho, 0.35)
    second = unitary @ damped @ unitary.conj().T
    assert trace_distance(first, second) > 1e-3


def test_discrete_transport_is_unitary() -> None:
    path = [
        bloch_to_density([0.2, 0.1, 0.2]),
        bloch_to_density([0.25, 0.15, 0.1]),
        bloch_to_density([0.2, 0.1, 0.2]),
    ]
    transport, steps = discrete_uhlmann_transport(path)
    assert len(steps) == 2
    assert np.allclose(transport.conj().T @ transport, np.eye(2), atol=1e-8)
