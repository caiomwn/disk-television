"""Generate editorial counts and inspectable verification/catalogue tables from data."""
from collections import Counter
from datetime import datetime,timezone
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def stamp(seconds):return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'
catalog=read('data/catalog.json');slots=read('docs/evidence/dt002/compiled-schedule.json');config=read('data/schedule.json')
old=read('tests/fixtures/dt001/catalog.json');old_ids={i['youtubeId'] for i in old};by_id={i['id']:i for i in catalog};proof=read('docs/evidence/dt002/playback-results.json')
new=[i for i in catalog if i['youtubeId'] not in old_ids];active=[i for i in catalog if i['broadcastEnabled']]
videos=[s for s in slots if s['type']=='video'];jp=sum(s['duration'] for s in videos if by_id[s['contentId']]['isJapaneseAnime']);video_seconds=sum(s['duration'] for s in videos)
prime_jp=sum(max(0,min(86400,s['start']+s['duration'])-max(64800,s['start'])) for s in videos if by_id[s['contentId']]['isJapaneseAnime'])
counts=Counter(s['contentId'] for s in videos)
def groups(items):return {i['series'] if i['kind']=='episode' and i.get('series') else i['id'] for i in items}
metrics={'checkedAt':datetime.now(timezone.utc).isoformat(),'beforeVideos':len(old),'addedVideos':len(new),'catalogueVideos':len(catalog),'actuallyEmbedTestedTotal':len({r['youtubeId'] for r in proof}),'actuallyEmbedVerifiedNew':sum(any(p['youtubeId']==i['youtubeId'] and p['actualPlayback'] for p in proof) for i in new),'onAirUniqueVideos':len(active),'onAirNewVideos':sum(i['youtubeId'] not in old_ids for i in active),'japaneseCatalogueVideos':sum(i['isJapaneseAnime'] for i in catalog),'japaneseOnAirVideos':sum(i['isJapaneseAnime'] for i in active),'japaneseCommercialEpisodesAndFilms':sum(i['isJapaneseAnime'] and i['kind'] in ['episode','film'] for i in catalog),'japaneseAcademicShorts':sum(i['isJapaneseAnime'] and i['kind']=='short' for i in catalog),'distinctTitlesOrSeries':len(groups(catalog)),'distinctOnAirTitlesOrSeries':len(groups(active)),'uniqueContentSeconds':sum(i['durationSeconds'] for i in catalog),'uniqueOnAirContentSeconds':sum(i['durationSeconds'] for i in active),'japaneseBroadcastSeconds':jp,'japanesePercentEntire24h':round(jp/86400*100,4),'japanesePercentVideoTime':round(jp/video_seconds*100,4),'japanesePercentPrime18to24':round(prime_jp/21600*100,4),'strict1995to2008JapaneseVideos':sum(i['isJapaneseAnime'] and 1995<=i['year']<=2008 for i in catalog),'slots':len(slots),'videoSlots':len(videos),'identSlots':sum(s['type']=='ident' for s in slots),'continuityFillSeconds':sum(s['duration'] for s in slots if s.get('variant')=='continuity'),'maxDailyPlays':max(counts.values()),'titleDefinition':'Episódios agrupados por série; filmes e curtas completos contam como obras individuais. GEIDAI/Seika são antologias, não uma série narrativa única.'}
metrics['uniqueContentHHMMSS']=stamp(metrics['uniqueContentSeconds']);metrics['uniqueOnAirContentHHMMSS']=stamp(metrics['uniqueOnAirContentSeconds'])
out=ROOT/'docs/evidence/dt002';out.mkdir(parents=True,exist_ok=True);(out/'editorial-metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (ROOT/'docs/DT-002-VERIFICATION.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['id','youtubeId','title','series','episode','year','seconds','onAir','japaneseAnimation','status','metadataSubtitles','channel','source','evidence'])
    for i in catalog:writer.writerow([i['id'],i['youtubeId'],i['title'],i.get('series'),i.get('episodeNumber'),i['year'],i['durationSeconds'],i['broadcastEnabled'],i['isJapaneseAnime'],'VERIFICADO (desktop; amostra de reprodução)',','.join(i['verification'].get('subtitleLanguages',[])),i.get('legitimacy',{}).get('channelUrl',i['creator']),i['sourceUrl'],i['verification']['playbackEvidence']])
lines=['# DT-002 — acervo integrado e verificado','','Classificação VERIFICADO = iframe oficial efetivamente reproduziu nesta conexão, em Chrome desktop headless, com ID, duração compatível, estado playing e tempo avançando. Não implica TV, disponibilidade mundial, autorização de reupload ou reprodução integral assistida.','','| Obra | Série/episódio | Ano | Duração | No ar | Origem |','|---|---|---:|---|---|---|']
for i in catalog:lines.append(f"| {i['title'].replace('|','/')} | {i.get('series') or 'Obra independente'} / {i.get('episodeNumber') or '—'} | {i['year']} | {stamp(i['durationSeconds'])} | {'Sim' if i['broadcastEnabled'] else 'Reserva'} | {i['sourceUrl']} |")
(ROOT/'docs/DT-002-CATALOG.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
backup=Path('C:/Users/padoka77/disk-television-backups/DT-002-before-20261110-102715/manifest.json')
if backup.exists():
    manifest=json.loads(backup.read_text(encoding='utf-8'))['files'];protected=['index.html','legal.html','styles.css','src/app.js','src/playout.js','src/schedule.js','assets/logo.svg','assets/logo.png','assets/favicon.svg'];result={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==manifest[p]['sha256'] for p in protected};(out/'preservation.json').write_text(json.dumps({'unchanged':result,'allPreserved':all(result.values()),'backupManifest':str(backup)},indent=2)+'\n',encoding='utf-8');assert all(result.values()),'Protected DT-001 runtime/identity changed'
print(json.dumps(metrics,ensure_ascii=False,indent=2))
