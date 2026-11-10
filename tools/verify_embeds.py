"""Real official YouTube embed verifier, never downloads/rehosts media.
A desktop/headless playback observation is not a Smart TV or rights guarantee.
"""
import argparse
from datetime import datetime, timezone
import http.server
import json
from pathlib import Path
import re
import threading
import time

ROOT=Path(__file__).resolve().parents[1]


def playback_confirmed(video_id, expected_duration, samples, errors):
    if errors or not isinstance(expected_duration,(int,float)) or expected_duration<=0:
        return False
    tolerance=max(5,expected_duration*.01)
    for previous,current in zip(samples,samples[1:]):
        if all(sample.get('state')==1 and sample.get('videoId')==video_id
               and abs((sample.get('duration') or 0)-expected_duration)<=tolerance
               for sample in [previous,current]):
            if current.get('time',0)-previous.get('time',0)>.5:
                return True
    return False


HARNESS='''<!doctype html><html><head><meta charset="utf-8"><meta name="referrer" content="strict-origin-when-cross-origin"><title>DISK TELEVISION — QA de incorporação</title><style>body{margin:0;background:#080910;color:white;font:16px Arial}header{height:60px;display:flex;align-items:center;gap:30px;padding:0 24px}#player{width:100%;height:600px}button{padding:10px 20px}</style></head><body><header><span>DISK TELEVISION / QA · player oficial</span><button id="start">Iniciar verificação</button><span id="title"></span></header><div id="player"></div><script>
window.__ready=false;window.__events=[];window.__errors=[];
window.onYouTubeIframeAPIReady=()=>{window.__player=new YT.Player('player',{width:'100%',height:'600',playerVars:{autoplay:0,controls:1,playsinline:1,origin:location.origin,hl:'pt',mute:1},events:{onReady(){__ready=true},onStateChange(e){__events.push({event:'state',code:e.data})},onError(e){__errors.push(e.data)},onAutoplayBlocked(){__events.push({event:'autoplay-blocked'})}}});};
document.getElementById('start').onclick=()=>{window.__activated=true;__player.mute()};
</script><script src="https://www.youtube.com/iframe_api"></script></body></html>'''


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/disk-television/__verify__/':
            self.send_error(404);return
        body=HARNESS.encode('utf-8')
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def log_message(self,*args):pass


def main():
    from playwright.sync_api import sync_playwright
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog');parser.add_argument('--out',default='docs/evidence/dt002/playback-results.json')
    parser.add_argument('--limit',type=int,default=0);parser.add_argument('--timeout',type=float,default=20)
    parser.add_argument('--retry-failed',action='store_true');parser.add_argument('--force',action='store_true')
    args=parser.parse_args()
    source=Path(args.catalog);source=source if source.is_absolute() else ROOT/source
    raw=json.loads(source.read_text(encoding='utf-8'))
    items=raw if isinstance(raw,list) else raw.get('items',raw.get('candidates',[]))
    out=Path(args.out);out=out if out.is_absolute() else ROOT/out;out.parent.mkdir(parents=True,exist_ok=True)
    results=json.loads(out.read_text(encoding='utf-8')) if out.exists() else []
    previous={item['youtubeId']:item for item in results}
    selected=[];seen=set()
    for item in items:
        video_id=item.get('youtubeId','')
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}',video_id):raise SystemExit(f'Invalid original YouTube token: {video_id!r}')
        if video_id in seen:continue
        seen.add(video_id)
        if not args.force and video_id in previous and (not args.retry_failed or previous[video_id].get('actualPlayback')):continue
        selected.append(item)
    if args.limit:selected=selected[:args.limit]
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/disk-television/__verify__/'
    captured=set()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            page=browser.new_page(viewport={'width':1280,'height':720})
            page.goto(url);page.wait_for_function('window.__ready===true',timeout=30000)
            page.locator('#start').click()
            for index,item in enumerate(selected):
                video_id=item['youtubeId'];expected=item['durationSeconds'];offset=min(5,max(0,expected-3))
                record={'youtubeId':video_id,'title':item['title'],'checkedAt':datetime.now(timezone.utc).isoformat(),'actualPlayback':False,'status':'PARTIAL','browser':'Google Chrome installed, headless desktop','origin':url,'requestedOffsetSeconds':offset,'expectedDurationSeconds':expected,'samples':[],'errorEvents':[],'events':[]}
                try:
                    page.evaluate('''arg=>{window.__events=[];window.__errors=[];document.getElementById('title').textContent=arg.title;__player.loadVideoById({videoId:arg.id,startSeconds:arg.offset});}''',{'id':video_id,'offset':offset,'title':item['title']})
                    started=time.monotonic()
                    while time.monotonic()-started<args.timeout:
                        page.wait_for_timeout(1100)
                        sample=page.evaluate('''()=>({state:__player.getPlayerState(),time:__player.getCurrentTime(),duration:__player.getDuration(),videoId:__player.getVideoData()?.video_id??null})''')
                        record['samples'].append(sample);record['errorEvents']=page.evaluate('window.__errors')
                        if record['errorEvents']:break
                        if playback_confirmed(video_id,expected,record['samples'],record['errorEvents']):
                            record['actualPlayback']=True;record['status']='VERIFIED';break
                    record['events']=page.evaluate('window.__events')
                    group=item.get('series') or item.get('creator') or video_id
                    if group not in captured or not record['actualPlayback']:
                        image=out.parent/f'embed-{video_id}.png';page.screenshot(path=str(image));record['screenshot']=str(image.relative_to(ROOT));captured.add(group)
                    page.evaluate('__player.stopVideo()')
                except Exception as error:record['error']=str(error)
                if not record['actualPlayback']:record['limitation']='Embed playback not confirmed on this desktop connection; no region bypass or alternative upload used.'
                previous[video_id]=record
                out.write_text(json.dumps(list(previous.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                print(f"{index+1}/{len(selected)} {record['status']} {video_id} {item['title']} errors={record['errorEvents']}",flush=True)
            browser.close()
    finally:server.shutdown();server.server_close()
    print(json.dumps({'testedThisRun':len(selected),'recordedTotal':len(previous),'verified':sum(r.get('actualPlayback',False) for r in previous.values()),'output':str(out)},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
