import numpy as np

from mmals_path_memory.mmals import covariance_density, diagnose_transition


def test_covariance_density() -> None:
    rng = np.random.default_rng(7)
    features = rng.normal(size=(100, 4))
    rho = covariance_density(features)
    assert rho.shape == (4, 4)
    assert np.isclose(np.trace(rho), 1.0)


def test_diagnose_transition_returns_bounded_ratio() -> None:
    before = np.diag([0.8, 0.2]).astype(complex)
    after = np.diag([0.6, 0.4]).astype(complex)
    result = diagnose_transition(before, after)
    assert 0.0 <= result.transverse_ratio <= 1.0
    assert result.transverse_energy > 0
