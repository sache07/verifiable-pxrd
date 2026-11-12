"""Human-readable overview or worker stream; monitoring never dispatches work."""
from pathlib import Path
import json
import sys
import time

R = Path(__file__).resolve().parents[1]
if len(sys.argv) == 1:
    while True:
        print('\033[2J\033[H', end='')
        p = R / 'evidence/STATUS.md'
        print(p.read_text() if p.exists() else 'Waiting for the controller. No research agent has launched.')
        sys.stdout.flush()
        time.sleep(10)
else:
    jid = sys.argv[1]
    path = R / 'attempts' / jid / 'run/codex-events.jsonl'
    seen = 0
    print('WORKER ' + jid, flush=True)
    while True:
        if path.exists():
            with path.open() as f:
                f.seek(seen)
                for line in f:
                    try: event = json.loads(line)
                    except ValueError: continue
                    item = event.get('item', {})
                    if event.get('type') == 'item.completed':
                        if item.get('type') == 'agent_message':
                            print('\n' + item.get('text', ''), flush=True)
                        elif item.get('type') == 'command_execution':
                            print('\n$ ' + item.get('command', '')[:600], flush=True)
                            print(item.get('aggregated_output', '')[-1000:], flush=True)
                    elif event.get('type') in ['error', 'turn.failed', 'turn.completed']:
                        print('\n' + json.dumps(event), flush=True)
                seen = f.tell()
        time.sleep(5)
