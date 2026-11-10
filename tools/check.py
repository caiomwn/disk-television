"""Run reproducible QA and retain actual command output (not generated claims).
python tools/check.py [--browser] [--live]
Use the project .venv Python for asset/browser checks.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--browser',action='store_true');parser.add_argument('--live',action='store_true');args=parser.parse_args()
node=shutil.which('node')
if not node:raise SystemExit('Node is required for the engine tests.')
commands=[('unit',[node,'--test',*[str(p) for p in sorted((ROOT/'tests').glob('*.test.mjs'))]]),('assets',[sys.executable,str(ROOT/'tests/asset_test.py')]),('launcher',[sys.executable,str(ROOT/'tests/launcher_test.py')])]
commands.append(('embed-evidence',[sys.executable,str(ROOT/'tests/embed_evidence_test.py')]))
if args.browser:commands.append(('browser',[sys.executable,str(ROOT/'tests/browser_test.py')]))
if args.browser:commands.append(('editorial-browser',[sys.executable,str(ROOT/'tests/editorial_browser_test.py')]))
commands.append(('production-build',[sys.executable,str(ROOT/'tests/build_test.py')]))
if args.browser:
    for label,filename in [('presentation-browser','presentation_browser_test.py'),('production-browser','production_browser_test.py'),('real-audio-browser','audio_browser_test.py')]:
        commands.append((label,[sys.executable,str(ROOT/'tests'/filename)]))
if args.live:commands.append(('live',[sys.executable,str(ROOT/'tests/live_player.py')]))
if args.live:commands.append(('production-live-abc',[sys.executable,str(ROOT/'tests/production_live.py')]))
report={'checkedAt':datetime.now(timezone.utc).isoformat(),'commands':[]}
for label,command in commands:
    completed=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    item={'name':label,'command':command,'exitCode':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr}
    report['commands'].append(item)
    print(f'[{label}] exit={completed.returncode}\n{completed.stdout}{completed.stderr}',flush=True)
report['allPassed']=all(command['exitCode']==0 for command in report['commands'])
out=ROOT/'docs/evidence/test-run.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Actual test log: {out}')
raise SystemExit(0 if report['allPassed'] else 1)
