"""Packaging checks and run status only; no statistical calculations or data edits."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, sys

ROOT=Path(__file__).resolve().parent
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    action=sys.argv[1] if len(sys.argv)>1 else '--check'
    status=ROOT/'results/RUN_COMPLETE.json'
    if action=='--start':
        status.parent.mkdir(exist_ok=True)
        status.write_text(json.dumps({'status':'running','started_at':datetime.now(timezone.utc).isoformat()},indent=2))
        return
    if action=='--complete':
        def count(name):
            with (ROOT/'results'/name).open(newline='') as f:
                return sum(1 for _ in csv.DictReader(f))
        result={'status':'completed','completed_at':datetime.now(timezone.utc).isoformat(),
                't_test_calls':count('t_tests.csv'),
                'bootstrap_calls':count('bootstrap_summary.csv'),
                'bootstrap_draws':count('bootstrap_draws.csv'),
                'python_model_coefficients':count('Python_coefficients.csv'),
                'R_model_coefficients':count('R_coefficients.csv'),
                'original_code_figures':len(list((ROOT/'results').glob('exp*_cell*.png'))),
                'data_sha256':digest(ROOT/'data/clean_trials.csv')}
        if result['bootstrap_draws']!=1000*result['bootstrap_calls']:
            raise SystemExit('Incomplete bootstrap output.')
        status.write_text(json.dumps(result,indent=2)+'\n')
        return
    if action!='--check':
        raise SystemExit('Usage: package_check.py [--check|--start|--complete]')
    manifest=json.loads((ROOT/'INPUT_CHECKSUMS.json').read_text())
    for relative,expected in manifest.items():
        path=ROOT/relative
        if not path.is_file() or digest(path)!=expected:
            raise SystemExit('Frozen input/code differs from the delivered package: '+relative)
    print(f'Checked {len(manifest)} frozen input/code files. Original values retained.')

if __name__=='__main__':main()
