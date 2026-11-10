"""Summarise actual data and QA evidence; never infer deployment or TV certification."""
from pathlib import Path
from datetime import datetime,timezone
import collections,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
code="import fs from 'node:fs';import {compileSchedule} from './src/schedule.js';const c=JSON.parse(fs.readFileSync('data/catalog.json')),s=JSON.parse(fs.readFileSync('data/schedule.json'));console.log(JSON.stringify({catalog:c,config:s,slots:compileSchedule(s,c)}));"
p=subprocess.run([shutil.which('node'),'--input-type=module','-e',code],cwd=ROOT,capture_output=True,text=True,check=True)
d=json.loads(p.stdout);catalog=d['catalog'];items={x['id']:x for x in catalog};slots=d['slots'];videos=[s for s in slots if s['type']=='video'];idents=[s for s in slots if s['type']=='ident']
metrics={'generatedAt':datetime.now(timezone.utc).isoformat(),'catalogItems':len(catalog),'usedDistinct':len({s['contentId'] for s in videos}),'blocks':len(d['config']['blocks']),'cycleSeconds':d['config']['cycleSeconds'],'slots':len(slots),'videoSlots':len(videos),'blockOpenings':sum(s.get('role')=='block-opening' for s in idents),'programmeLinks':sum(s.get('role')=='programme-link' for s in idents),'continuityFillSeconds':sum(s['duration'] for s in idents if s['variant']=='continuity'),'japaneseAnimationSeconds':sum(s['duration'] for s in videos if items[s['contentId']].get('isJapaneseAnime')),'uniqueContentSeconds':sum(x['durationSeconds'] for x in catalog),'playbackEvidencePreviouslyConfirmed':sum(x.get('verification',{}).get('actualPlayback') is True for x in catalog),'physicalSamsung':False,'noNewSeedUploadsAdded':True}
qa=json.loads((ROOT/'docs/evidence/test-run.json').read_text(encoding='utf-8'));counts={}
for c in qa['commands']:
    m=re.search(r'(?m)^. tests (\d+)',c['stdout']) if c['name']=='unit' else re.search(r'Ran (\d+) tests?',c['stdout']+c['stderr'])
    if m:counts[c['name']]=int(m.group(1))
metrics['testCounts']=counts;metrics['totalTests']=sum(counts.values());metrics['qaAllPassed']=qa['allPassed'];metrics['diagnostics']=[{'name':c['name'],'exitCode':c['exitCode']} for c in qa['commands'] if c['name'] not in counts]
metrics['blocksDetail']=[{'label':b['label'],'start':b['start'],'videoSlots':sum(s['block']==b['label'] and s['type']=='video' for s in slots),'fillSeconds':sum(s['duration'] for s in slots if s['block']==b['label'] and s.get('variant')=='continuity')} for b in d['config']['blocks']]
out=ROOT/'docs/evidence/launch';out.mkdir(parents=True,exist_ok=True);(out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'compiled-schedule.json').write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
