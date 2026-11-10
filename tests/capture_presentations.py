"""Capture actual YouTube playback in all three presentations, no API double."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/disk-television/'
out=ROOT/'docs/evidence/launch';out.mkdir(parents=True,exist_ok=True);records=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        for mode in ['A','B','C']:
            page=browser.new_page(viewport={'width':1920,'height':1080})
            page.add_init_script("Date.now=()=>Date.parse('2026-11-10T03:00:48Z');")
            page.goto(url);page.locator('#tune:not([disabled])').wait_for()
            if mode=='B':page.screenshot(path=str(out/'tuning.png'),full_page=True)
            page.locator(f'#gate [data-presentation="{mode}"]').click();page.locator('#tune').click()
            record={'mode':mode,'realYouTube':True,'mocked':False,'pageErrors':[]}
            page.on('pageerror',lambda e:record['pageErrors'].append(str(e)))
            try:
                page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'",timeout=25000)
                page.wait_for_timeout(5000 if mode=='A' else 1500)
                record['playingObserved']=True
            except Exception as e:record['playingObserved']=False;record['error']=str(e)
            record['title']=page.locator('#now-title').inner_text()
            record['frame']=page.locator('#youtube-player').bounding_box()
            record['uncovered']=page.locator('#youtube-player').evaluate('e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===e}')
            record['screenshot']=f'docs/evidence/launch/player-{mode}.png';page.screenshot(path=str(ROOT/record['screenshot']),full_page=True)
            records.append(record);print(json.dumps(record,ensure_ascii=False),flush=True);page.close()
        browser.close()
finally:
    server.shutdown();server.server_close();(out/'presentation-live.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['playingObserved'] and r['uncovered'] and not r['pageErrors'] for r in records) else 1)
