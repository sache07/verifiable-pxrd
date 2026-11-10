import csv
import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metric import clean_rwp
from plot import ROOT, load


def test_pdf_uses_embedded_truetype():
    import matplotlib
    assert matplotlib.rcParams["pdf.fonttype"] == 42


def test_self_and_scale_invariance():
    profile = np.linspace(0, 1, 8501)
    assert clean_rwp(profile, profile) == 0
    assert clean_rwp(profile, 5 * profile) == pytest.approx(0, abs=1e-12)


def test_unbounded_residual():
    reference = np.zeros(8501)
    reference[0] = 1
    assert clean_rwp(reference, np.ones(8501)) > 100


def test_bad_profile_rejected():
    with pytest.raises(ValueError):
        clean_rwp(np.zeros(8501), np.zeros(8501))


def test_frozen_data_and_agent_panels_agree():
    data = ROOT / "results/appendix/profile-residuals/as-submitted"
    native, fixed = load(data, "native"), load(data, "fixed")
    for condition in ("GPT-5.6 Sol (high)", "matsci-codex", "pxrd-codex", "adapted-codex"):
        a = sorted((r["exact"], r["rwp"]) for r in native if r["condition"] == condition)
        b = sorted((r["exact"], r["rwp"]) for r in fixed if r["condition"] == condition)
        assert a == b


def test_summary_matches_frozen_statistics():
    data = ROOT / "results/appendix/profile-residuals/as-submitted"
    for metric, filename in (("native", "native-rwp-summary.csv"), ("fixed", "fixedparams-v1-rwp-summary.csv")):
        rows = load(data, metric)
        for expected in csv.DictReader((data / filename).open()):
            if expected.get("condition_type") == "reference":
                continue
            condition = expected.get("condition", expected.get("framework"))
            exact = expected["group"] == "exact match"
            values = [r["rwp"] for r in rows if r["condition"] == condition and r["exact"] == exact]
            assert len(values) == int(expected["n"])
            assert np.mean(values) == pytest.approx(float(expected["mean_rwp_percent"]), abs=1e-10)
            assert np.median(values) == pytest.approx(float(expected["median_rwp_percent"]), abs=1e-10)
