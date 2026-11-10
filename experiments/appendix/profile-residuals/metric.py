"""The shared clean fixedparams-v1 residual, in percent (unit weights)."""
import numpy as np


def normalize(profile):
    values = np.asarray(profile, dtype=np.float64)
    if values.shape != (8501,) or not np.isfinite(values).all() or values.max() <= 0:
        raise ValueError("Expected a finite positive 8501-bin clean profile")
    return values / values.max()


def clean_rwp(reference, candidate):
    reference, candidate = normalize(reference), normalize(candidate)
    return float(100 * np.sqrt(np.sum((reference - candidate) ** 2) / np.sum(reference ** 2)))
