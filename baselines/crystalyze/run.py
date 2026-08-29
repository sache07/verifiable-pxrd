"""Run the Crystalyze benchmark adapter."""

from pathlib import Path

from verifiable_pxrd.baselines.runner import main

if __name__ == "__main__":
    raise SystemExit(main("crystalyze", Path(__file__).with_name("adapter.py")))

