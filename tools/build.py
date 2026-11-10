"""Build a minimal, secret-free GitHub Pages tree with a Chrome 69 syntax target.
The target improves compatibility; actual Samsung browser support still needs a TV test.
"""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
ENTRY=ROOT/'node_modules/esbuild/bin/esbuild'
NODE=shutil.which('node')
if not ENTRY.exists() or not NODE:raise SystemExit('Install Node and the pinned development dependency with npm ci before building.')
OUT.mkdir(exist_ok=True)
# The output is generated; never sweep/delete unrelated project directories.
for path in list(OUT.iterdir()):
    if path.is_dir():shutil.rmtree(path)
    else:path.unlink()
for name in ['index.html','legal.html','styles.css','presentation.css','LICENSE','.nojekyll']:
    shutil.copy2(ROOT/name,OUT/name)
for name in ['assets','data']:shutil.copytree(ROOT/name,OUT/name)
html=(OUT/'index.html').read_text(encoding='utf-8')
old='<script type="module" src="./src/app.js"></script>'
if old not in html:raise SystemExit('Unexpected script entry; refusing an incomplete build')
(OUT/'index.html').write_text(html.replace(old,'<script defer src="./app.bundle.js"></script>'),encoding='utf-8')
compat=(ROOT/'src/compat.js').read_text(encoding='utf-8')
result=subprocess.run([NODE,str(ENTRY),'src/app.js','--bundle','--format=iife','--target=chrome69','--charset=utf8','--legal-comments=inline','--outfile='+str(OUT/'app.bundle.js'),'--banner:js='+compat],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
print(result.stdout+result.stderr)
if result.returncode:raise SystemExit(result.returncode)
files={}
for path in OUT.rglob('*'):
    if not path.is_file():continue
    data=path.read_bytes();name=path.relative_to(OUT).as_posix()
    if re.search(rb'(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)',data):raise SystemExit('Potential secret found in production output: '+name)
    files[name]=hashlib.sha256(data).hexdigest()
release={'version':json.loads((ROOT/'package.json').read_text())['version'],'generatedAt':datetime.now(timezone.utc).isoformat(),'syntaxTarget':'chrome69','samsungPhysicallyTested':False,'files':files}
(OUT/'release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(OUT),'files':len(files)+1,'version':release['version'],'secretScan':'passed','requiresLocalServerInProduction':False},indent=2))
