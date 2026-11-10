"""Produce inspectable source and minimal GitHub Pages ZIPs; no remote writes."""
from pathlib import Path
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)
SITE=ROOT/'_site'
if not (SITE/'release.json').is_file():raise SystemExit('Run tools/build.py before packaging')
site_files=[path for path in sorted(SITE.rglob('*')) if path.is_file()]
source_files=[ROOT/name for name in ['index.html','legal.html','styles.css','presentation.css','.nojekyll','.gitignore','LICENSE','README.md','package.json','package-lock.json','requirements-dev.txt','ABRIR-LOCAL.cmd','research-evidence.json']]
for directory in ['src','assets','data','docs','tests','tools','research']:
    source_files.extend(path for path in sorted((ROOT/directory).rglob('*')) if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ['.pyc','.html'])
manifest=[]
release='.'.join(json.loads((ROOT/'package.json').read_text(encoding='utf-8'))['version'].split('.')[:2])
for name,files,base in [(f'disk-television-{release}-pages.zip',site_files,SITE),(f'disk-television-{release}-source.zip',source_files,ROOT)]:
    target=OUT/name
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path,path.relative_to(base).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:raise SystemExit('Corrupt archive')
        names=archive.namelist()
        required=['index.html','legal.html','styles.css','presentation.css','data/catalog.json','data/schedule.json','assets/logo.png','assets/logo.svg','assets/audio/ident-next.mp3','.nojekyll']
        required+=['app.bundle.js','release.json'] if base==SITE else ['src/app.js','src/schedule.js','src/playout.js','src/station-audio.js','package-lock.json']
        assert all(member in names for member in required)
        assert not any('.venv' in name or '__pycache__' in name for name in names)
        manifest.append({'file':str(target),'entries':len(names),'bytes':target.stat().st_size,'integrityChecked':True})
print(json.dumps(manifest,ensure_ascii=False,indent=2))
