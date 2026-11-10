"""Local Chromium integration tests. YouTube is a labelled test double here.
Run with .venv/Scripts/python.exe tests/browser_test.py
"""
import contextlib
import functools
import http.server
import json
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/disk-television/'):
            self.path = self.path[len('/disk-television'):]
        else:
            self.send_error(404)
            return
        super().do_GET()
    def log_message(self, *args):
        pass

FAKE_YOUTUBE = """
window.__ytCalls=[];
window.YT={Player:class {
 constructor(id,opts){this.opts=opts;this.time=0;this.muted=false;
 window.__fakePlayer=this;
 const frame=document.createElement('iframe');frame.id=id;frame.title='YouTube test double';
 document.getElementById(id).replaceWith(frame);
 setTimeout(()=>opts.events.onReady({target:this}),10);}
 loadVideoById(arg){window.__ytCalls.push(arg);this.time=arg.startSeconds;
 setTimeout(()=>this.opts.events.onStateChange({data:1}),10);}
 stopVideo(){} getCurrentTime(){return this.time;} getPlayerState(){return 1;}
 getVideoData(){return {video_id:window.__ytCalls.at(-1)?.videoId};}
 seekTo(t){this.time=t;} mute(){this.muted=true;} unMute(){this.muted=false;}
 isMuted(){return this.muted;} playVideo(){} destroy(){}
}};
setTimeout(()=>window.onYouTubeIframeAPIReady(),0);
"""

class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/disk-television/'
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.page=self.browser.new_page(viewport={'width':1920,'height':1080})
        self.errors=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
        # Freeze the DT-001 scenarios; production DT-002 data has separate tests.
        for name in ['catalog.json','schedule.json']:
            body=(ROOT/'tests/fixtures/dt001'/name).read_text(encoding='utf-8')
            self.page.route('**/data/'+name,lambda route,request,body=body:route.fulfill(content_type='application/json',body=body))
    def tearDown(self):
        self.page.close()
    def test_01_static_site_and_tune_gate(self):
        response=self.page.goto(self.url)
        self.assertEqual(response.status,200)
        self.page.get_by_role('button',name='Sintonizar CH 99',exact=True).wait_for()
        self.assertEqual(self.page.title(),'DISK TELEVISION — CH 99')
        self.assertEqual(self.errors,[])
        self.assertTrue(self.page.locator('img[alt="DISK TELEVISION"]').first.evaluate('(e)=>e.complete && e.naturalWidth>0'))

    def test_02_join_reload_and_guide(self):
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.goto(self.url)
        self.page.get_by_role('button',name='Sintonizar CH 99',exact=True).click()
        self.page.wait_for_function('window.__ytCalls?.length===1')
        self.assertEqual(self.page.evaluate('window.__ytCalls[0].startSeconds'),22)
        title=self.page.locator('#now-title').inner_text()
        self.assertTrue(title)
        self.page.reload()
        self.page.get_by_role('button',name='Sintonizar CH 99',exact=True).click()
        self.page.wait_for_function('window.__ytCalls?.length===1')
        self.assertEqual(self.page.evaluate('window.__ytCalls[0].startSeconds'),22)
        self.assertEqual(self.page.locator('#now-title').inner_text(),title)
        self.page.keyboard.press('g')
        self.assertTrue(self.page.locator('#guide').is_visible())
        self.assertEqual(self.page.locator('.guide-row.current').count(),1)
        self.assertGreater(self.page.locator('.guide-row').count(),40)
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#guide').is_visible())
        self.assertEqual(self.errors,[])

    def test_03_unavailable_ident_transition_and_midnight(self):
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.goto(self.url)
        self.page.get_by_role('button',name='Sintonizar CH 99',exact=True).click()
        self.page.wait_for_function('window.__ytCalls?.length===1')
        self.page.evaluate('window.__fakePlayer.opts.events.onError({data:150})')
        self.assertTrue(self.page.locator('#continuity').is_visible())
        self.assertIn('indisponível',self.page.locator('#reception-text').inner_text())
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        self.page.wait_for_function("document.getElementById('stage').dataset.slotType==='ident'")
        self.assertEqual(self.page.locator('#continuity').get_attribute('data-variant'),'night')
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        self.page.wait_for_function("document.getElementById('continuity').dataset.variant==='next'")
        self.assertIn('Elephants Dream',self.page.locator('#ident-title').inner_text())
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        self.page.wait_for_function('window.__ytCalls?.length===2')
        self.assertEqual(self.page.evaluate('window.__ytCalls[1].startSeconds'),0)
        self.page.evaluate("window.__nowMs=Date.parse('2026-11-11T03:00:01Z')")
        self.page.wait_for_function("document.getElementById('clock').textContent==='00:00:01'")
        self.assertEqual(self.page.locator('#stage').get_attribute('data-slot-type'),'ident')
        self.assertEqual(self.errors,[])

    def test_04_api_recovers_automatically_in_next_attraction(self):
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.unroute('**/iframe_api')
        attempts=[]
        def api_route(route):
            attempts.append(1)
            if len(attempts)==1: route.abort()
            else: route.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE)
        self.page.route('**/iframe_api',api_route)
        self.page.goto(self.url)
        self.page.get_by_role('button',name='Sintonizar CH 99',exact=True).click()
        self.page.wait_for_function("document.getElementById('reception-text').textContent.includes('indisponível')")
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)+26000")
        self.page.wait_for_function('window.__ytCalls?.length===1',timeout=6000)
        self.assertEqual(len(attempts),2)
        self.assertEqual(self.errors,[])

    def test_05_autoplay_blocked_sound_focus_and_guide_resync(self):
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.goto(self.url);self.page.locator('#tune').click()
        self.page.wait_for_function('window.__ytCalls?.length===1')
        self.page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'")
        self.page.evaluate('window.__fakePlayer.opts.events.onAutoplayBlocked({})')
        self.assertIn('bloqueou',self.page.locator('#reception-text').inner_text())
        self.page.locator('#retry').click()
        self.page.wait_for_function('window.__ytCalls.length===2')
        self.page.locator('#sound').click()
        self.assertTrue(self.page.evaluate('window.__fakePlayer.muted'))
        self.assertEqual(self.page.locator('#sound').get_attribute('aria-pressed'),'true')
        self.page.locator('#guide-open').click()
        self.assertFalse(self.page.locator('#player-shell').is_visible())
        self.page.keyboard.press('Tab')
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'guide-list')
        self.page.keyboard.press('Tab')
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'guide-close')
        self.page.evaluate('window.__nowMs+=30000')
        self.page.keyboard.press('Escape')
        self.page.wait_for_function('window.__ytCalls.length===3')
        self.assertEqual(self.page.evaluate('window.__ytCalls.at(-1).startSeconds'),52)
        self.page.keyboard.press('ArrowRight')
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'sound')
        self.assertEqual(self.errors,[])

    def test_06_mobile_and_reduced_motion(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.emulate_media(reduced_motion='reduce')
        self.page.goto(self.url)
        self.page.locator('#tune').click()
        self.page.wait_for_function('document.getElementById("gate").hidden')
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
        self.page.locator('#guide-open').click()
        self.assertTrue(self.page.locator('#guide-close').is_visible())
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
        self.assertEqual(self.errors,[])

    def test_07_bad_catalog_reports_configuration_error(self):
        self.page.route('**/data/catalog.json',lambda r:r.fulfill(content_type='application/json',body='[]'))
        self.page.goto(self.url)
        self.page.wait_for_function("document.getElementById('boot-message').textContent.includes('Falha de sintonia')")
        self.assertTrue(self.page.locator('#tune').is_disabled())
        self.assertEqual(self.errors,[])

    def test_08_offscreen_player_defers_next_load_then_resyncs(self):
        self.page.set_viewport_size({'width':640,'height':320})
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.goto(self.url);self.page.locator('#tune').click()
        self.page.wait_for_function('window.__ytCalls?.length===1')
        self.page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
        ratio=self.page.locator('#stage').evaluate('(e)=>{const r=e.getBoundingClientRect();return Math.max(0,Math.min(innerHeight,r.bottom)-Math.max(0,r.top))/r.height}')
        self.assertLessEqual(ratio,.5,'offscreen trigger did not reach the target geometry')
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)+28000")
        self.page.wait_for_function("document.getElementById('now-title').textContent==='Elephants Dream'")
        self.page.wait_for_timeout(500)
        self.assertEqual(self.page.evaluate('window.__ytCalls.length'),1,'must not automatically load while <= half visible')
        self.page.evaluate('window.scrollTo(0,0)')
        self.page.wait_for_function('window.__ytCalls.length===2')
        self.assertEqual(self.page.evaluate('window.__ytCalls.at(-1).startSeconds'),2)
        self.assertEqual(self.errors,[])

    def test_09_terms_privacy_accessible_before_tuning_and_no_early_youtube(self):
        requests=[]
        self.page.on('request',lambda r: requests.append(r.url))
        self.page.goto(self.url)
        self.page.locator('#tune:not([disabled])').wait_for()
        self.assertTrue(self.page.locator('#legal-note').is_visible())
        self.assertTrue(self.page.locator('#legal-link').is_visible())
        self.assertFalse(any('/iframe_api' in url for url in requests))
        self.page.locator('#legal-link').click()
        self.page.get_by_role('heading',name='Termos e privacidade',exact=True).wait_for()
        self.assertEqual(self.page.locator('a[href="https://www.youtube.com/t/terms"]').count(),1)
        self.assertEqual(self.page.locator('a[href="https://policies.google.com/privacy"]').count(),1)
        self.assertIn('cookies',self.page.locator('main').inner_text())
        self.page.get_by_role('link',name='Voltar ao CH 99',exact=True).click()
        self.page.locator('#tune:not([disabled])').wait_for()
        self.assertEqual(self.errors,[])

if __name__=='__main__':
    unittest.main(verbosity=2)
