"""Numerical geometry helpers.

The functions in this module are deliberately small and explicit. They are
intended for reproducible engineering experiments, not as a replacement for a
specialized quantum-information package.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import polar, sqrtm

ComplexMatrix = NDArray[np.complex128]
RealVector = NDArray[np.float64]


def _hermitize(matrix: NDArray[np.complexfloating]) -> ComplexMatrix:
    arr = np.asarray(matrix, dtype=np.complex128)
    return (arr + arr.conj().T) / 2.0


def normalize_psd(matrix: NDArray[np.complexfloating], epsilon: float = 1e-10) -> ComplexMatrix:
    """Project a Hermitian matrix to a full-rank density-like operator.

    Negative eigenvalues caused by numerical noise are clipped, a small floor
    is added, and the result is normalized to trace one.
    """

    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    matrix_h = _hermitize(matrix)
    values, vectors = np.linalg.eigh(matrix_h)
    values = np.maximum(values.real, 0.0) + epsilon
    projected = (vectors * values) @ vectors.conj().T
    trace = np.trace(projected).real
    if trace <= 0:
        raise ValueError("matrix cannot be normalized to a density operator")
    return _hermitize(projected / trace)


def von_neumann_entropy(rho: NDArray[np.complexfloating], base: float = 2.0) -> float:
    """Return ``-Tr(rho log rho)`` using the requested logarithm base."""

    if base <= 0 or np.isclose(base, 1.0):
        raise ValueError("base must be positive and different from one")
    density = normalize_psd(rho)
    values = np.linalg.eigvalsh(density).real
    values = values[values > 0]
    return float(-np.sum(values * np.log(values)) / np.log(base))


def bloch_to_density(vector: Iterable[float]) -> ComplexMatrix:
    """Convert a three-dimensional Bloch vector into a qubit density matrix."""

    x, y, z = np.asarray(tuple(vector), dtype=float)
    norm = float(np.linalg.norm([x, y, z]))
    if norm > 1.0 + 1e-10:
        raise ValueError("Bloch-vector norm must not exceed one")
    return np.array(
        [[1.0 + z, x - 1j * y], [x + 1j * y, 1.0 - z]], dtype=np.complex128
    ) / 2.0


def density_to_bloch(rho: NDArray[np.complexfloating]) -> RealVector:
    """Convert a qubit density matrix to its Bloch vector."""

    density = normalize_psd(rho)
    if density.shape != (2, 2):
        raise ValueError("density_to_bloch expects a 2x2 matrix")
    return np.array(
        [
            2.0 * density[0, 1].real,
            -2.0 * density[0, 1].imag,
            density[0, 0].real - density[1, 1].real,
        ],
        dtype=float,
    )


def apply_unitary(rho: NDArray[np.complexfloating], unitary: NDArray[np.complexfloating]) -> ComplexMatrix:
    """Apply ``rho -> U rho U^dagger`` after validating matrix shapes."""

    density = normalize_psd(rho)
    unitary_c = np.asarray(unitary, dtype=np.complex128)
    if unitary_c.shape != density.shape:
        raise ValueError("unitary and density matrix must have the same shape")
    identity = np.eye(unitary_c.shape[0], dtype=np.complex128)
    if not np.allclose(unitary_c.conj().T @ unitary_c, identity, atol=1e-8):
        raise ValueError("provided matrix is not unitary")
    return _hermitize(unitary_c @ density @ unitary_c.conj().T)


def amplitude_damping_channel(rho: NDArray[np.complexfloating], probability: float) -> ComplexMatrix:
    """Apply a qubit amplitude-damping channel with damping probability ``p``."""

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between zero and one")
    density = normalize_psd(rho)
    if density.shape != (2, 2):
        raise ValueError("amplitude damping expects a 2x2 density matrix")
    p = float(probability)
    k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - p)]], dtype=np.complex128)
    k1 = np.array([[0.0, np.sqrt(p)], [0.0, 0.0]], dtype=np.complex128)
    return _hermitize(k0 @ density @ k0.conj().T + k1 @ density @ k1.conj().T)


def trace_distance(rho: NDArray[np.complexfloating], sigma: NDArray[np.complexfloating]) -> float:
    """Return the quantum trace distance ``0.5 * ||rho-sigma||_1``."""

    delta = _hermitize(normalize_psd(rho) - normalize_psd(sigma))
    singular_values = np.linalg.svd(delta, compute_uv=False)
    return float(0.5 * np.sum(singular_values))


def commutator_norm(a: NDArray[np.complexfloating], b: NDArray[np.complexfloating]) -> float:
    """Return the Frobenius norm of the matrix commutator ``AB-BA``."""

    a_c = np.asarray(a, dtype=np.complex128)
    b_c = np.asarray(b, dtype=np.complex128)
    if a_c.shape[1] != b_c.shape[0] or b_c.shape[1] != a_c.shape[0]:
        raise ValueError("matrices must have compatible square shapes")
    return float(np.linalg.norm(a_c @ b_c - b_c @ a_c, ord="fro"))


def spectral_blocks(rho: NDArray[np.complexfloating], tolerance: float = 1e-8) -> tuple[NDArray[np.float64], list[ComplexMatrix]]:
    """Return eigenvalues and projectors grouped by approximate degeneracy."""

    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    density = normalize_psd(rho)
    values, vectors = np.linalg.eigh(density)
    order = np.argsort(values)
    values = values[order]
    vectors = vectors[:, order]

    groups: list[list[int]] = []
    for index, value in enumerate(values):
        if not groups or abs(value - values[groups[-1][0]]) > tolerance:
            groups.append([index])
        else:
            groups[-1].append(index)

    projectors: list[ComplexMatrix] = []
    grouped_values: list[float] = []
    for group in groups:
        basis = vectors[:, group]
        projectors.append(_hermitize(basis @ basis.conj().T))
        grouped_values.append(float(np.mean(values[group])))
    return np.asarray(grouped_values, dtype=float), projectors


def tangent_normal_decomposition(
    rho: NDArray[np.complexfloating],
    velocity: NDArray[np.complexfloating],
    tolerance: float = 1e-8,
) -> tuple[ComplexMatrix, ComplexMatrix]:
    """Split a Hermitian velocity into orbit-tangent and spectral-block parts.

    For spectral projectors ``P_a``, the block-diagonal component
    ``sum_a P_a X P_a`` is the part that can change eigenvalues or the state
    within degenerate blocks. The remaining cross-block component is tangent to
    the unitary coadjoint orbit.
    """

    density = normalize_psd(rho)
    x = _hermitize(velocity)
    if density.shape != x.shape:
        raise ValueError("rho and velocity must have the same shape")
    _, projectors = spectral_blocks(density, tolerance=tolerance)
    normal = np.zeros_like(density)
    for projector in projectors:
        normal += projector @ x @ projector
    normal = _hermitize(normal)
    tangent = _hermitize(x - normal)
    return tangent, normal


def lyapunov_generator(
    rho: NDArray[np.complexfloating], velocity: NDArray[np.complexfloating]
) -> ComplexMatrix:
    """Solve ``G rho + rho G = velocity`` for a full-rank density operator."""

    density = normalize_psd(rho)
    x = _hermitize(velocity)
    if density.shape != x.shape:
        raise ValueError("rho and velocity must have the same shape")
    values, vectors = np.linalg.eigh(density)
    x_basis = vectors.conj().T @ x @ vectors
    denominator = values[:, None] + values[None, :]
    if np.any(denominator <= 0):
        raise ValueError("rho must be full rank")
    g_basis = x_basis / denominator
    return _hermitize(vectors @ g_basis @ vectors.conj().T)


def discrete_uhlmann_transport(
    path: Iterable[NDArray[np.complexfloating]],
) -> tuple[ComplexMatrix, list[ComplexMatrix]]:
    """Compute a discrete Uhlmann parallel-transport unitary along a state path.

    For consecutive states, the polar unitary of
    ``sqrt(rho_{k+1}) sqrt(rho_k)`` aligns amplitudes so that their overlap is
    positive. The returned unitary is a path-dependent transport factor. For a
    closed loop it is a discrete holonomy estimate.
    """

    densities = [normalize_psd(rho) for rho in path]
    if len(densities) < 2:
        raise ValueError("path must contain at least two states")
    shape = densities[0].shape
    if any(rho.shape != shape for rho in densities):
        raise ValueError("all states must have the same shape")

    transport = np.eye(shape[0], dtype=np.complex128)
    steps: list[ComplexMatrix] = []
    for current, following in zip(densities[:-1], densities[1:], strict=True):
        overlap = np.asarray(sqrtm(following) @ sqrtm(current), dtype=np.complex128)
        unitary, _positive = polar(overlap)
        transport = unitary @ transport
        steps.append(unitary)
    return transport, steps
