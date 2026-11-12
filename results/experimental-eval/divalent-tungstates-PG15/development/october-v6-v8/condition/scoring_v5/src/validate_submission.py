"""Public, reference-free output validation for a future common solver harness."""
import argparse,json
from pathlib import Path
from common import read_json
from structure_metrics import parse_submission

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('workspace',type=Path)
    parser.add_argument('--elements',nargs='+',help='Defaults to workspace/inputs/metadata.json')
    args=parser.parse_args()
    try:
        elements=args.elements or read_json(args.workspace/'inputs/metadata.json')['elements']
        data,rows,notes=parse_submission(args.workspace,elements)
        details=data['_submission_parsing']
        hard=details['hard_physical_failure'] or any(r['physical']['status']=='fail' for r in rows)
        valid=not details['invalid_model_records'] and not details['fraction_issues'] and not hard
        result=dict(valid_format=valid,usable_atomic_models=len(rows),
                    unresolved_components=len(details['unresolved_components']),
                    fractions_complete=details['quantification_complete'],
                    invalid_model_records=details['invalid_model_records'],
                    fraction_issues=details['fraction_issues'],hard_physical_failure=hard,
                    notes=notes,ground_truth_accessed=False,
                    message='Unknown fractions are allowed; they do not receive quantitative credit.' if valid else 'Repair invalid records; do not invent unknown quantities.')
    except Exception as exc:
        valid=False;result=dict(valid_format=False,error=str(exc),ground_truth_accessed=False)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if valid else 1)

if __name__=='__main__':main()
