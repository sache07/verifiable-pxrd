import hashlib
import json
import tomllib
from pathlib import Path

from verifiable_pxrd.util import sha256_file

ROOT = Path(__file__).resolve().parents[1]


def test_public_generation_sources_match_manifest() -> None:
    manifest = json.loads(
        (ROOT / "pxrd-bench/generation/MANIFEST.json").read_text(encoding="utf-8")
    )
    for name, record in manifest["files"].items():
        assert sha256_file(ROOT / "pxrd-bench/generation" / name) == record["sha256"]


def test_pattern_generation_lock_matches_record() -> None:
    root = ROOT / "pxrd-bench/generation/runtime"
    record = json.loads((root / "runtime-lock.json").read_text(encoding="utf-8"))
    assert sha256_file(root / "conda-linux-64.lock") == record["conda_explicit_lock_sha256"]
    assert sum(item["cases"] for item in record["validated_replay"].values()) == 200


def test_ood_generation_environment_lock_is_repo_relative_and_current() -> None:
    record = json.loads(
        (ROOT / "pxrd-bench/pXRD-ood/GENERATION.lock.json").read_text(encoding="utf-8")
    )
    relative_lock = Path(record["environment_lock_path"])
    assert not relative_lock.is_absolute()
    assert relative_lock.parts[0] == "pxrd-bench"
    assert sha256_file(ROOT / relative_lock) == record["environment_lock_sha256"]


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def test_agent_installation_payloads_are_exact_and_self_contained() -> None:
    matsci_expected = {
        (
            "matsci",
            "requirements_input",
        ): "196be85cf195231c310729c4d28505cea2d4e6b4ff1aaebb1b23340274496a03",
        (
            "matsci",
            "requirements_lock",
        ): "48c5027c09df1c47d32c58556c68d3641fe0863011e5dc17765e1e3a86065af8",
        (
            "matsci",
            "install_script",
        ): "6592e5a82a36e0b8d02e44022025ad30ce7ea47283a4ed9188f11f6f26e61be7",
    }
    pxrd_expected = {
        (
            "gsasii",
            "requirements_lock",
        ): "f71f2aa9151cda5b24141166b094ea0251e04df0b5254e755043cac1fcd488df",
        (
            "gsasii",
            "install_script",
        ): "00c7ae8e2ec916ed706d62703425600e7fe13da79d7615d494b34a6674829227",
        (
            "dicvol14",
            "install_script",
        ): "c0c800f96716931cab85900affd0a44a16a21ede0dcf9d0f26f9ab3ff9f5b3ba",
    }
    installations = {}
    for name in (
        "matsci-codex.toml",
        "pxrd-codex.toml",
        "adapted-codex.toml",
    ):
        with (ROOT / "experiments/agent-adaptation/conditions" / name).open("rb") as stream:
            installations[name] = tomllib.load(stream)["environment"]["installation"]
        for (component, field), digest in matsci_expected.items():
            assert _digest(installations[name][component][field]) == digest

    for name in ("pxrd-codex.toml", "adapted-codex.toml"):
        installation = installations[name]
        for (component, field), digest in pxrd_expected.items():
            assert _digest(installation[component][field]) == digest
        assert installation["gsasii"]["commit"] == ("c8f97a500d7e48fddbaf8586948c24b174d8bab3")
        assert installation["dicvol14"]["binary_sha256"] == (
            "317430d2806ec8e4ed8f87b70940d9315092cab0869f84e479ec1c6e3bb5e586"
        )
