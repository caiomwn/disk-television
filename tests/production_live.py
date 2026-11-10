"""Real production bundle/YouTube in A/B/C; no API or catalogue doubles."""
import functools,http.server,json,shutil,subprocess,threading
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT
code="""import fs from 'node:fs';import {compileSchedule,locate} from './src/schedule.js';const c=JSON.parse(fs.readFileSync('data/catalog.json')),s=JSON.parse(fs.readFileSync('data/schedule.json'));const slots=compileSchedule(s,c),at=locate(slots,Date.parse(s.epoch),Date.parse('2026-11-10T03:00:48Z'));const next=slots.slice(at.index+1).find(x=>x.type==='video');console.log(JSON.stringify({current:at.slot,offset:at.elapsed,next,catalog:c}));"""
expected=json.loads(subprocess.run([shutil.which('node'),'--input-type=module','-e',code],cwd=ROOT,capture_output=True,text=True,check=True).stdout)
items={x['id']:x for x in expected['catalog']}
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'_site')));threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/disk-television/'
out=ROOT/'docs/evidence/launch';out.mkdir(parents=True,exist_ok=True);records=[]
def playback(page,slot):
    samples=[];duration=items[slot['contentId']]['durationSeconds']
    for attempt in range(18):
        page.wait_for_timeout(1000)
        samples.append(page.evaluate("()=>({state:window.__livePlayer?.getPlayerState?.()??null,time:window.__livePlayer?.getCurrentTime?.()??null,videoId:window.__livePlayer?.getVideoData?.().video_id??null,duration:window.__livePlayer?.getDuration?.()??0})"))
        if len(samples)>1 and all(x['state']==1 and x['videoId']==slot['videoId'] and abs(x['duration']-duration)<=max(5,duration*.01) for x in samples[-2:]) and samples[-1]['time']>samples[-2]['time']+.5:return {'confirmed':True,'samples':samples}
    return {'confirmed':False,'samples':samples}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        for mode in ['A','B','C']:
            page=browser.new_page(viewport={'width':1920,'height':1080})
            record={'mode':mode,'realYouTube':True,'mocked':False,'productionBundle':True,'physicalSamsung':False,'pageErrors':[]}
            page.on('pageerror',lambda e,record=record:record['pageErrors'].append(str(e)))
            page.add_init_script("""window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;let ready;Object.defineProperty(window,'onYouTubeIframeAPIReady',{configurable:true,get:()=>ready,set(fn){ready=()=>{const Original=YT.Player;YT.Player=function(id,opts){const instance=new Original(id,opts);window.__livePlayer=instance;return instance;};fn();};}});""")
            page.goto(url);page.locator('#tune:not([disabled])').wait_for()
            if mode=='B':page.screenshot(path=str(out/'tuning.png'),full_page=True)
            page.locator(f'#gate [data-presentation="{mode}"]').click();page.locator('#tune').click()
            try:
                page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'",timeout=25000)
                record['firstPlayback']=playback(page,expected['current'])
                record['playingObserved']=record['firstPlayback']['confirmed'];record['requestedOffset']=expected['offset']
                if mode=='B' and record['playingObserved']:
                    page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
                    page.wait_for_function("document.getElementById('stage').dataset.slotType==='ident'")
                    record['linkObserved']=page.locator('#continuity').is_visible();record['linkRole']=page.locator('#continuity').get_attribute('data-role');record['nextAnnounced']=page.locator('#ident-title').text_content()
                    page.wait_for_timeout(900)  # Capture the settled animation, not its first fade-in frame.
                    page.screenshot(path=str(out/'programme-link.png'),full_page=True)
                    page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
                    page.wait_for_function("document.getElementById('stage').dataset.slotType==='video'")
                    record['automaticNextPlayback']=playback(page,expected['next'])
                if mode=='A':page.wait_for_function("document.getElementById('app').dataset.chrome==='hidden'",timeout=7000)
            except Exception as e:record['playingObserved']=False;record['error']=str(e)
            record['title']=page.locator('#now-title').text_content();record['frame']=page.locator('#youtube-player').bounding_box()
            record['uncovered']=page.locator('#youtube-player').evaluate('e=>{const r=e.getBoundingClientRect();return [[r.left+3,r.top+3],[r.right-3,r.top+3],[r.left+3,r.bottom-3],[r.right-3,r.bottom-3],[r.left+r.width/2,r.top+r.height/2]].every(([x,y])=>document.elementFromPoint(x,y)===e)}')
            record['screenshot']=f'docs/evidence/launch/player-{mode}.png';page.screenshot(path=str(ROOT/record['screenshot']),full_page=True)
            records.append(record);print(json.dumps(record,ensure_ascii=False),flush=True);page.close()
        browser.close()
finally:
    server.shutdown();server.server_close();(out/'presentation-live.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if len(records)==3 and all(r['playingObserved'] and r['uncovered'] and not r['pageErrors'] for r in records) and next(r for r in records if r['mode']=='B').get('automaticNextPlayback',{}).get('confirmed') else 1)
