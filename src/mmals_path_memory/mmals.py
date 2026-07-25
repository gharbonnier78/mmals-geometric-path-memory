"""MMALS-oriented state descriptors and path metrics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .geometry import normalize_psd, tangent_normal_decomposition, von_neumann_entropy


@dataclass(frozen=True)
class RegimeDiagnostics:
    """Compact diagnostics for one representation-state transition."""

    tangent_energy: float
    transverse_energy: float
    transverse_ratio: float
    entropy_before: float
    entropy_after: float
    entropy_delta: float
    recommendation: str


def covariance_density(features: NDArray[np.floating], epsilon: float = 1e-6) -> NDArray[np.complex128]:
    """Convert a feature batch into a trace-normalized covariance operator."""

    array = np.asarray(features, dtype=float)
    if array.ndim != 2 or array.shape[0] < 2:
        raise ValueError("features must be a 2D array with at least two samples")
    centered = array - np.mean(array, axis=0, keepdims=True)
    covariance = centered.T @ centered / max(1, array.shape[0] - 1)
    covariance += epsilon * np.eye(covariance.shape[0])
    return normalize_psd(covariance, epsilon=epsilon)


def diagnose_transition(
    rho_before: NDArray[np.complexfloating],
    rho_after: NDArray[np.complexfloating],
    transverse_threshold: float = 0.35,
) -> RegimeDiagnostics:
    """Classify a state transition as mostly reorientation or structural change."""

    before = normalize_psd(rho_before)
    after = normalize_psd(rho_after)
    velocity = after - before
    tangent, transverse = tangent_normal_decomposition(before, velocity)
    tangent_energy = float(np.linalg.norm(tangent, ord="fro"))
    transverse_energy = float(np.linalg.norm(transverse, ord="fro"))
    total = tangent_energy + transverse_energy
    ratio = transverse_energy / total if total > 0 else 0.0
    entropy_before = von_neumann_entropy(before)
    entropy_after = von_neumann_entropy(after)
    delta = entropy_after - entropy_before

    if ratio >= transverse_threshold:
        recommendation = "Evaluate new-host creation, host split/merge, or protected replay."
    elif tangent_energy > 0:
        recommendation = "Prefer in-host adaptation and monitor order-sensitive interference."
    else:
        recommendation = "No meaningful representation change detected."

    return RegimeDiagnostics(
        tangent_energy=tangent_energy,
        transverse_energy=transverse_energy,
        transverse_ratio=ratio,
        entropy_before=entropy_before,
        entropy_after=entropy_after,
        entropy_delta=delta,
        recommendation=recommendation,
    )
