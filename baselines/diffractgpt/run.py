"""Run the DiffractGPT benchmark adapter."""

from pathlib import Path

from verifiable_pxrd.baselines.runner import main

if __name__ == "__main__":
    raise SystemExit(main("diffractgpt", Path(__file__).with_name("adapter.py")))

