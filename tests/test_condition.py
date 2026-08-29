import tomllib
from dataclasses import replace
from pathlib import Path

from verifiable_pxrd.condition import load_condition
from verifiable_pxrd.run import _config_text

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ROOT / "experiments/agent-adaptation/conditions"

CANONICAL_CONDITIONS = (
    "adapted-codex.toml",
    "llm-chat-sol-high-api-v2.toml",
    "matsci-codex.toml",
    "pxrd-codex.toml",
)
CODEX_CONDITIONS = tuple(name for name in CANONICAL_CONDITIONS if not name.startswith("llm-chat"))


def test_only_canonical_condition_tomls_are_live() -> None:
    assert {path.name for path in CONDITIONS.glob("*.toml")} == set(CANONICAL_CONDITIONS)


def test_source_conditions_embed_environment_and_installation() -> None:
    for name in CODEX_CONDITIONS:
        with (CONDITIONS / name).open("rb") as stream:
            raw = tomllib.load(stream)
        assert isinstance(raw.get("environment"), dict), name
        assert "runtime_locks" not in raw["environment"], name
        assert "matsci" in raw["environment"]["installation"], name

    for name in ("pxrd-codex.toml", "adapted-codex.toml"):
        condition = load_condition(CONDITIONS / name)
        assert set(condition.installation) == {"matsci", "gsasii", "dicvol14"}


def test_llm_chat_condition_is_model_only_and_uses_current_prompt() -> None:
    with (CONDITIONS / "llm-chat-sol-high-api-v2.toml").open("rb") as stream:
        condition = tomllib.load(stream)
    assert condition["adapter"] == "responses-api"
    assert condition["model"] == "gpt-5.6-sol"
    assert condition["reasoning_effort"] == "high"
    assert condition["prompt"] == "experiments/agent-adaptation/prompts/chat-solve.md"
    assert condition["tools"] == []
    assert condition["input_transport"] == "inline-text"


def test_pxrd_conditions_share_scientific_one_hour_contract(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("VPBENCH_CODEX", "/usr/local/bin/codex")
    monkeypatch.setenv("VPBENCH_AUTH_HOME", str(tmp_path / "api-auth"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    baseline = load_condition(CONDITIONS / "pxrd-codex.toml")
    adapted = load_condition(CONDITIONS / "adapted-codex.toml")

    assert baseline.auth_method == "api"
    assert baseline.auth_home == (tmp_path / "api-auth").resolve()
    assert adapted.auth_method == "chatgpt"
    assert adapted.auth_home == (tmp_path / "home/.codex").resolve()
    assert baseline.timeout_seconds == adapted.timeout_seconds == 3600

    records = []
    for name in ("pxrd-codex.toml", "adapted-codex.toml"):
        with (CONDITIONS / name).open("rb") as stream:
            record = tomllib.load(stream)
        for key in ("id", "status", "capability", "auth_method", "auth_home"):
            record.pop(key, None)
        records.append(record)
    assert records[0] == records[1]


def test_capability_bin_is_first_on_trainee_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("VPBENCH_CODEX", "/usr/local/bin/codex")
    condition = load_condition(CONDITIONS / "adapted-codex.toml")
    condition = replace(condition, capability=tmp_path / "source-capability")
    workspace = tmp_path / "workspace"
    capability_bin = workspace / ".vpbench-capability/bin"
    capability_bin.mkdir(parents=True)

    config = tomllib.loads(_config_text(condition, workspace))
    path = config["shell_environment_policy"]["set"]["PATH"].split(":")

    assert path[0] == str(capability_bin)
