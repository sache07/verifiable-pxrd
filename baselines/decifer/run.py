"""Run the deCIFer benchmark adapter."""

from pathlib import Path

from verifiable_pxrd.baselines.runner import main

if __name__ == "__main__":
    raise SystemExit(main("decifer", Path(__file__).with_name("adapter.py")))

