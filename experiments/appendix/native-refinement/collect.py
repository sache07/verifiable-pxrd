"""Retrieve completed Modal calls without starting any new paid computation."""
import argparse
from pathlib import Path
import modal
from common import read_json
from remote import collect

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--wait", action="store_true", help="Wait for unfinished calls instead of skipping them")
    args = parser.parse_args()
    for record in read_json(args.ledger)["calls"]:
        destination = Path(record["output"])
        if (destination / "candidates" / record["id"] / "result.json").exists():
            continue
        try:
            payload = modal.FunctionCall.from_id(record["call_id"]).get(timeout=None if args.wait else 0)
        except TimeoutError:
            print(record["id"], "pending")
            continue
        collect(payload, destination)
