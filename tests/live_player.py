"""Network-dependent diagnostic; never substitutes fake playback for YouTube.
Uses real installed Chrome. Writes evidence, exits 1 if playback unconfirmed.
"""
import functools
import http.server
import json
from pathlib import Path
import threading
import time
from playwright.sync_api import sync_playwright
from browser_test import Handler, ROOT

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/disk-television/'
evidence=ROOT/'docs'/'evidence';evidence.mkdir(parents=True,exist_ok=True)
result={'url':url,'browser':'installed Google Chrome, headless','officialPlayer':True,'mockedYouTube':False,'events':[],'console':[],'networkFailures':[]}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        page=browser.new_page(viewport={'width':1920,'height':1080})
        # This legacy regression keeps the original DT-001 programme sequence.
        for name in ['catalog.json','schedule.json']:
            body=(ROOT/'tests/fixtures/dt001'/name).read_text(encoding='utf-8')
            page.route('**/data/'+name,lambda route,request,body=body:route.fulfill(content_type='application/json',body=body))
        page.on('console',lambda msg: result['console'].append({'type':msg.type,'text':msg.text[:500]}))
        page.on('requestfailed',lambda req: result['networkFailures'].append({'url':req.url[:250],'error':req.failure}))
        page.add_init_script("""
          window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;
          window.__liveEvents=[];
          let ready;
          Object.defineProperty(window,'onYouTubeIframeAPIReady',{configurable:true,get:()=>ready,set(fn){
            ready=()=>{const Original=YT.Player;YT.Player=function(id,opts){
              for(const key of ['onReady','onStateChange','onError','onAutoplayBlocked']){
                const previous=opts.events[key];opts.events[key]=e=>{window.__liveEvents.push({event:key,code:e.data??null});previous?.(e);};
              }
              const instance=new Original(id,opts);window.__livePlayer=instance;return instance;
            };fn();};
          }});
        """)
        page.goto(url)
        page.get_by_role('button',name='Sintonizar CH 99',exact=True).click()
        samples=[]
        for i in range(12):
            page.wait_for_timeout(2500)
            sample=page.evaluate("""()=>({state:window.__livePlayer?.getPlayerState?.()??null,time:window.__livePlayer?.getCurrentTime?.()??null,videoId:window.__livePlayer?.getVideoData?.().video_id??null,status:document.getElementById('station-state').textContent,message:document.getElementById('reception-text').textContent})""")
            samples.append(sample)
            if sample['state']==1 and len(samples)>1 and samples[-2]['state']==1 and sample['time']>samples[-2]['time']+.5:
                break
            if 'indisponível' in sample['message']:
                break
        result['samples']=samples
        result['playbackConfirmed']=bool(len(samples)>1 and samples[-1]['state']==1 and samples[-2]['state']==1 and samples[-1]['time']>samples[-2]['time']+.5)
        if result['playbackConfirmed']:
            page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
            page.wait_for_function("document.getElementById('stage').dataset.slotType==='ident'")
            result['stationTransitionObserved']=page.locator('#continuity').is_visible()
            page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
            page.wait_for_function("document.getElementById('continuity').dataset.variant==='next'")
            result['nextAnnounced']=page.locator('#ident-title').inner_text()
            page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
            next_samples=[]
            for i in range(10):
                page.wait_for_timeout(2000)
                sample=page.evaluate("""()=>({state:window.__livePlayer?.getPlayerState?.(),time:window.__livePlayer?.getCurrentTime?.(),videoId:window.__livePlayer?.getVideoData?.().video_id})""")
                next_samples.append(sample)
                if len(next_samples)>1 and sample.get('videoId')=='TLkA0RELQ1g' and sample.get('state')==1 and next_samples[-2].get('state')==1 and sample.get('time',0)>next_samples[-2].get('time',0)+.5:break
            result['nextVideoSamples']=next_samples
            result['automaticNextPlaybackConfirmed']=bool(len(next_samples)>1 and next_samples[-1].get('videoId')=='TLkA0RELQ1g' and next_samples[-1].get('state')==1 and next_samples[-1].get('time',0)>next_samples[-2].get('time',0)+.5)
        result['events']=page.evaluate('window.__liveEvents')
        result['iframeSrc']=page.locator('#youtube-player').get_attribute('src')
        page.screenshot(path=str(evidence/'live-player.png'),full_page=True)
        result['screenshot']='docs/evidence/live-player.png'
        browser.close()
except Exception as error:
    result['error']=str(error);result['playbackConfirmed']=False
finally:
    server.shutdown();server.server_close()
    (evidence/'live-player.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['console','networkFailures']},ensure_ascii=False,indent=2))
raise SystemExit(0 if result['playbackConfirmed'] and result.get('automaticNextPlaybackConfirmed') else 1)
