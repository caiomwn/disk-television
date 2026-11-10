"""DT-002 editorial build. Runtime remains JSON-only and unchanged.
Default: write proposals. --apply also installs catalogue/24-hour schedule.
Only actual confirmed embeds are eligible; no network or media downloads here.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,data):
    target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    original=read('tests/fixtures/dt001/catalog.json')
    source=read('research/dt002/selected-for-playback.json')
    proof={r['youtubeId']:r for r in read('docs/evidence/dt002/playback-results.json')}
    captions={r['youtubeId']:r for r in read('research/dt002/caption-audit.json')}
    catalog=[];seen=set()
    for item in original+source:
        if item['youtubeId'] in seen:continue
        seen.add(item['youtubeId']);item=copy.deepcopy(item);record=proof.get(item['youtubeId'])
        if not record or not record.get('actualPlayback'):continue
        if record['expectedDurationSeconds']!=item['durationSeconds']:raise ValueError('Duration evidence mismatch: '+item['id'])
        old=item['id'] in {i['id'] for i in original}
        item.setdefault('kind','short');item.setdefault('isJapaneseAnime',False);item.setdefault('series',None);item.setdefault('episodeNumber',None)
        item.setdefault('editorialTags',['independent-animation','DT-001-archive'])
        item['completeWork']=True
        if item.get('series')=="Magic User's Club TV":
            item['season']=2
            item['seasonNote']='Numeração do publicador Nozomi: OVA = Season 1; TV de 1999 = Season 2. A janela TV começa no episódio 1.'
        item['verification']['metadataCheckedAt']=item['verification']['checkedAt']
        item['verification'].update({'checkedAt':record['checkedAt'],'status':'VERIFIED','actualPlayback':True,'playbackEvidence':'docs/evidence/dt002/playback-results.json','verificationScope':'Official embed, desktop Chrome headless, current connection only; not full-length viewing or Smart TV certification.'})
        item['verification']['embeddability']={'iframePlaybackTested':True,'actualPlaybackConfirmed':True,'metadata':item['verification'].get('embeddability')}
        audit=captions.get(item['youtubeId'])
        if audit and not audit.get('error'):
            if audit['durationSeconds']!=item['durationSeconds'] or audit['channelId']!=item['legitimacy']['channelId']:raise ValueError('Independent metadata mismatch: '+item['id'])
            item['verification']['subtitleLanguages']=audit['manualSubtitleLanguages']
            item['verification']['automaticCaptionLanguages']=audit['automaticCaptionLanguages']
            item['verification']['subtitleEvidence']='research/dt002/caption-audit.json; listed manual tracks, not translations inferred from an English Dub title.'
        item['editorialMaxDailyPlays']=2 if old or item['kind']=='episode' else 1 if item['kind']=='film' else 3
        if item['series']=='The Amazing Digital Circus':item['editorialMaxDailyPlays']=1
        item['broadcastEnabled']=False
        catalog.append(item)
    by_id={i['id']:i for i in catalog}
    if len(by_id)!=len(catalog):raise ValueError('Duplicate catalogue slug')
    def eps(series,first,last):
        rows=sorted([i for i in catalog if i.get('series')==series and i.get('episodeNumber') is not None and first<=i['episodeNumber']<=last],key=lambda i:i['episodeNumber'])
        if [i['episodeNumber'] for i in rows]!=list(range(first,last+1)):raise ValueError('No complete verified episode window: '+series)
        return [i['id'] for i in rows]
    jp_shorts=[i['id'] for i in catalog if i['isJapaneseAnime'] and i['kind']=='short']
    best=['dt002-alt-best-friend'];circus=['dt002-alt-the-amazing-digital-circus-pilot']
    old_morning=['spring','big-buck-bunny','caminandes-gran-dillama','caminandes-llamigos']
    filler=jp_shorts+old_morning+['coffee-run','charge','tears-of-steel','sintel','elephants-dream','cosmos-laundromat']+best
    # Narrative windows progress across daytime blocks. Prime time is an explicit encore.
    definitions=[
      (0,10800,'AFTER HOURS',jp_shorts+['sintel','elephants-dream','cosmos-laundromat']+best+circus,[], 'Curtas de autor, pesadelo e surrealismo digital. Obras adultas; não é faixa infantil.'),
      (10800,23400,'MORNING FREQUENCY',eps('Sonic X',1,6)+eps("Magic User's Club TV",1,2)+['spring'],[], 'Aventura leve e descoberta magical-school Y2K. Magic é a série TV de 1999; a OVA anterior não está disponível integralmente nesta conexão.'),
      (23400,36000,'ANIME ARCHIVE',eps('Kenichi: The Mightiest Disciple',1,3)+eps('Magic Knight Rayearth',1,4)+['big-buck-bunny','caminandes-gran-dillama','caminandes-llamigos'],[], 'Janela de estreia: Kenichi 1–3 e Rayearth 1–4. Curtas complementares em vez de trailers.'),
      (36000,48600,'MOE SIGNAL',eps('Magic Knight Rayearth',5,8)+eps("Magic User's Club TV",1,2)+eps('Sonic X',1,2),["Magic User's Club TV",'Sonic X'], 'Rayearth continua de 5 a 8, depois das estreias 1–4. Reprises declaradas de Magic TV 1–2 e Sonic 1–2.'),
      (48600,64800,'CYBERIA',eps('Mobile Suit Gundam SEED',1,3)+eps('Mobile Suit Gundam 00',1,1)+eps('Mobile Suit Gundam SEED',1,3)+eps('Mobile Suit Gundam 00',1,1)+eps('Sonic X',3,4)+['tears-of-steel','charge','coffee-run']+best,['Mobile Suit Gundam SEED','Mobile Suit Gundam 00'], 'Mecha e tecnologia. SEED 1–3 em duas sessões e piloto 00; Sonic 3–4 completa a reprise iniciada antes. Não promete temporada completa.'),
      (64800,77400,'MOE SIGNAL / ENCORE',eps('Magic Knight Rayearth',1,8),['Magic Knight Rayearth'],'Reprise noturna em ordem dos oito primeiros episódios de Rayearth; o clássico de 1994 é uma escolha deliberada próxima ao recorte de gosto.'),
      (77400,86400,'CINE DISK',[next(i['id'] for i in catalog if i['kind']=='film' and i['isJapaneseAnime'])],[], 'Sessão de longa completo: Char’s Counterattack (1988), edição oficial com faixas de legenda EN/PT-BR listadas. Clássico contextual da franquia, não filme de 2000.')
    ]
    config=copy.deepcopy(read('tests/fixtures/dt001/schedule.json'));config['blocks']=[]
    config['editorialNote']='DT-002: anime oficial e animação japonesa no centro; faixas narrativas e reprises explicitadas. Apenas embeds observados em desktop entram no ar. Horário de Brasília, ciclo diário de 86400 segundos. Gundam pode expirar em 31/03/2027 e requer revalidação.'
    config['verificationPolicy']='Only VERIFIED + actualPlayback=true; blocked/unverified candidates remain in research, never silently substituted.'
    counts=Counter();planning=[]
    def cost(item_id,cursor):return by_id[item_id]['durationSeconds']+config['idents']['night' if cursor<21600 else 'station']+config['idents']['next']
    for start,end,label,base,reprises,note in definitions:
        rotation=[];cursor=start
        for item_id in base:
            if item_id not in by_id:raise ValueError('Unverified base item: '+item_id)
            if counts[item_id]>=by_id[item_id]['editorialMaxDailyPlays']:raise ValueError('Daily play cap in base: '+item_id)
            size=cost(item_id,cursor)
            if cursor+size>end:raise ValueError(f'Editorial base does not fit {label}: {end-cursor} remains before {item_id}')
            rotation.append(item_id);counts[item_id]+=1;cursor+=size
        while True:
            candidates=[i for i in filler if i in by_id and counts[i]<by_id[i]['editorialMaxDailyPlays'] and cursor+cost(i,cursor)<=end]
            if not candidates:break
            # Japanese shorts before international encores; spread plays across titles.
            item_id=min(candidates,key=lambda i:(not by_id[i]['isJapaneseAnime'],counts[i],-cost(i,cursor),filler.index(i)))
            rotation.append(item_id);counts[item_id]+=1;cursor+=cost(item_id,cursor)
        if not rotation or end-cursor>=cost(rotation[0],cursor):raise ValueError('Rotation would loop unexpectedly in '+label)
        config['blocks'].append({'start':start,'label':label,'rotation':rotation,'editorialNote':note,'explicitReprises':reprises})
        planning.append({'label':label,'start':start,'end':end,'programmes':len(rotation),'continuityFillSeconds':end-cursor})
    for item in catalog:
        item['broadcastEnabled']=counts[item['id']]>0
        if not item['broadcastEnabled']:
            item['offAirReason']='Verified reserve. SEED Destiny is held until an appropriate narrative window follows the original series.' if item['series']=='Mobile Suit Gundam SEED Destiny' else 'Verified catalogue reserve, not selected for this 24-hour edition.'
    if any(not i['isJapaneseAnime'] for i in catalog if i['id'].startswith('dt002-dist-') and i.get('countryOfOrigin')=='JP'):raise ValueError('Origin classification mismatch')
    write('research/dt002/proposed-catalog.json',catalog);write('research/dt002/proposed-schedule.json',config);write('research/dt002/editorial-plan.json',planning)
    if args.apply:write('data/catalog.json',catalog);write('data/schedule.json',config)
    print(json.dumps({'applied':args.apply,'catalogue':len(catalog),'newItems':len(catalog)-len(original),'onAirUnique':sum(i['broadcastEnabled'] for i in catalog),'japaneseItems':sum(i['isJapaneseAnime'] for i in catalog),'blocks':planning,'maxDailyPlays':max(counts.values()),'allCounts':dict(counts)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
