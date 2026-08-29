"""Run the RealPXRD-Solver benchmark adapter."""

from pathlib import Path

from verifiable_pxrd.baselines.runner import main

if __name__ == "__main__":
    raise SystemExit(main("realpxrd-solver", Path(__file__).with_name("adapter.py")))

