"""Verify deployed Pages bytes and real current-clock playback at its HTTPS origin."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,time,urllib.request
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
GH=os.environ.get('GH_EXECUTABLE') or shutil.which('gh')
URL='https://caiomwn.github.io/disk-television/'
OUT=ROOT/'docs/evidence/launch/public-site.json'
result={'checkedAt':datetime.now(timezone.utc).isoformat(),'url':URL,'mockedYouTube':False,'clockSimulated':False,'physicalSamsung':False,'pageErrors':[]}
def api(path):
    if GH:
        p=subprocess.run([GH,'api',path],capture_output=True,text=True,encoding='utf-8',timeout=30);p.check_returncode();return json.loads(p.stdout)
    request=urllib.request.Request('https://api.github.com/'+path,headers={'User-Agent':'DISK-TELEVISION-public-release-verifier'})
    return json.load(urllib.request.urlopen(request,timeout=30))
def read(name):
    r=urllib.request.urlopen(urllib.request.Request(URL+name,headers={'Cache-Control':'no-cache','User-Agent':'DISK-TELEVISION-launch-verifier'}),timeout=30)
    assert r.status==200;return r.read()
try:
    for attempt in range(24):
        pages=api('repos/caiomwn/disk-television/pages');runs=api('repos/caiomwn/disk-television/actions/runs?per_page=3')['workflow_runs']
        head=api('repos/caiomwn/disk-television/git/ref/heads/gh-pages')['object']['sha']
        matching=[r for r in runs if r['head_sha']==head and r['name']=='pages build and deployment']
        if pages['status']=='built' and matching and matching[0]['conclusion']=='success':break
        time.sleep(5)
    else:raise RuntimeError('Exact-head Pages deployment not successful within verification window')
    result['pages']={'status':pages['status'],'source':pages['source'],'httpsEnforced':pages['https_enforced'],'head':head,'workflowUrl':matching[0]['html_url'],'conclusion':matching[0]['conclusion']}
    manifest=json.loads(read('release.json'));local=json.loads((ROOT/'_site/release.json').read_text())
    assert manifest==local,'Deployed release manifest differs from validated artifact'
    mismatches=[]
    for name,expected in manifest['files'].items():
        if hashlib.sha256(read(name)).hexdigest()!=expected:mismatches.append(name)
    assert not mismatches,str(mismatches)
    result['version']=manifest['version'];result['verifiedResourceHashes']=len(manifest['files']);result['manifestMatches']=True
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        page=browser.new_page(viewport={'width':1920,'height':1080});page.on('pageerror',lambda e:result['pageErrors'].append(str(e)))
        page.add_init_script("""window.__requestedLoads=[];let ready;Object.defineProperty(window,'onYouTubeIframeAPIReady',{configurable:true,get:()=>ready,set(fn){ready=()=>{const Original=YT.Player;YT.Player=function(id,opts){const previous=opts.events.onReady;opts.events.onReady=e=>{const original=e.target.loadVideoById.bind(e.target);e.target.loadVideoById=spec=>{window.__requestedLoads.push(spec);return original(spec);};previous(e);};const instance=new Original(id,opts);window.__livePlayer=instance;return instance;};fn();};}});""")
        response=page.goto(URL);assert response.status==200
        page.locator('#tune:not([disabled])').click()
        samples=[]
        for attempt in range(90):
            page.wait_for_timeout(1500)
            s=page.evaluate("()=>({state:window.__livePlayer?.getPlayerState?.()??null,time:window.__livePlayer?.getCurrentTime?.()??0,videoId:window.__livePlayer?.getVideoData?.().video_id??null,duration:window.__livePlayer?.getDuration?.()??0,title:document.getElementById('now-title').textContent,elapsed:Number(document.getElementById('stage').dataset.elapsed),slotType:document.getElementById('stage').dataset.slotType})")
            samples.append(s)
            result['samples']=samples
            result['requestedLoads']=page.evaluate('window.__requestedLoads')
            result['stationState']=page.locator('#station-state').text_content()
            result['receptionMessage']=page.locator('#reception-text').text_content()
            if attempt>20 and page.locator('#continuity').is_visible() and page.locator('#continuity').get_attribute('data-variant')=='unavailable':
                page.screenshot(path=str(ROOT/'docs/evidence/launch/public-failure.png'),full_page=True)
                raise RuntimeError('Public playback fell back: '+result['receptionMessage'])
            catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'));item=next((x for x in catalog if x['youtubeId']==s['videoId']),None)
            if len(samples)>1 and item and all(x['state']==1 and x['videoId']==item['youtubeId'] and abs(x['duration']-item['durationSeconds'])<=max(5,item['durationSeconds']*.01) and abs(x['time']-x['elapsed'])<=12 for x in samples[-2:]) and samples[-1]['time']>samples[-2]['time']+.5:break
        else:raise RuntimeError('Current-clock playback not confirmed on public origin')
        result['samples']=samples;result['playbackConfirmed']=True;result['requestedLoads']=page.evaluate('window.__requestedLoads');assert result['requestedLoads']
        result['uncovered']=page.locator('#youtube-player').evaluate('e=>{const r=e.getBoundingClientRect();return [[r.left+3,r.top+3],[r.right-3,r.top+3],[r.left+3,r.bottom-3],[r.right-3,r.bottom-3],[r.left+r.width/2,r.top+r.height/2]].every(([x,y])=>document.elementFromPoint(x,y)===e)}');assert result['uncovered']
        page.locator('#guide-open').click();assert page.locator('#guide').is_visible();assert not page.locator('#player-shell').is_visible()
        page.locator('#guide-close').click();page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'",timeout=30000)
        result['guideAndReturnConfirmed']=True
        page.screenshot(path=str(ROOT/'docs/evidence/launch/public-on-air.png'),full_page=True)
        result['audioReadyVariants']=page.locator('#app').get_attribute('data-audio-variants')
        assert not result['pageErrors'];browser.close()
    result['success']=True
except Exception as e:result['success']=False;result['error']=str(e)
finally:
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result.get('success') else 1)
