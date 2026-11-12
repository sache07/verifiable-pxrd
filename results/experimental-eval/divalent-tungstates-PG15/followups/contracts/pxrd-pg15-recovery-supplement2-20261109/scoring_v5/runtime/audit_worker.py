from pathlib import Path
import json,hashlib,traceback
import replay_worker # installs the restricted data-only GSAS loader
from audit_profile import audit_project
p=Path('/input/final.gpx'); before=hashlib.sha256(p.read_bytes()).hexdigest()
try:
 d=audit_project(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==before
 d.update(source_sha256=before,source_unchanged=True)
 Path('/output/audit.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
except Exception as e:
 Path('/output/audit.json').write_text(json.dumps({'error':repr(e),'traceback':traceback.format_exc()}))
 raise
