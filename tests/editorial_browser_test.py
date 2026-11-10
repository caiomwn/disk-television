"""Production DT-002 data integration; only the external API is a test double."""
import functools,http.server,json,shutil,subprocess,threading,unittest
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT,FAKE_YOUTUBE

class EditorialBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
        cls.config=json.loads((ROOT/'data/schedule.json').read_text(encoding='utf-8'))
        code="import fs from 'node:fs';import {compileSchedule} from './src/schedule.js';console.log(JSON.stringify(compileSchedule(JSON.parse(fs.readFileSync('data/schedule.json')),JSON.parse(fs.readFileSync('data/catalog.json')))));"
        compiled=subprocess.run([shutil.which('node'),'--input-type=module','-e',code],cwd=ROOT,capture_output=True,text=True,check=True)
        cls.slots=json.loads(compiled.stdout)
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/disk-television/'
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.page=self.browser.new_page(viewport={'width':1920,'height':1080});self.errors=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
    def tearDown(self):self.page.close()
    def join_rayearth(self):
        self.item=next(i for i in self.catalog if i.get('series')=='Magic Knight Rayearth' and i.get('episodeNumber')==1)
        self.slot=next(s for s in self.slots if s.get('contentId')==self.item['id'])
        self.page.add_init_script(f"window.__nowMs=Date.parse({json.dumps(self.config['epoch'])})+{self.slot['start']*1000+120000};Date.now=()=>window.__nowMs;")
        self.page.goto(self.url);self.page.locator('#tune').click();self.page.wait_for_function('window.__ytCalls?.length===1')
    def test_production_join_reopen_guide_and_unavailable_fallback(self):
        self.join_rayearth()
        self.assertEqual(self.page.evaluate('window.__ytCalls[0].videoId'),self.item['youtubeId'])
        self.assertEqual(self.page.evaluate('window.__ytCalls[0].startSeconds'),120)
        self.assertEqual(self.page.locator('#now-title').inner_text(),self.item['title'])
        self.page.reload();self.page.locator('#tune').click();self.page.wait_for_function('window.__ytCalls?.length===1')
        self.assertEqual(self.page.evaluate('window.__ytCalls[0].startSeconds'),120)
        self.page.keyboard.press('g')
        self.assertEqual(self.page.locator('.guide-row.current h3').inner_text(),self.item['title'])
        self.assertEqual(self.page.locator('.guide-row').count(),len(self.slots))
        self.page.keyboard.press('Escape')
        self.page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'")
        self.page.evaluate('window.__fakePlayer.opts.events.onError({data:150})')
        self.assertTrue(self.page.locator('#continuity').is_visible())
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        self.page.wait_for_function("document.getElementById('stage').dataset.slotType==='ident'")
        self.page.wait_for_function("document.getElementById('continuity').dataset.variant==='next'")
        self.assertTrue(self.page.locator('#continuity').is_visible())
        self.assertEqual(self.page.locator('#continuity').get_attribute('data-role'),'programme-link')
        self.assertEqual(self.page.evaluate("(Number(document.getElementById('stage').dataset.endMs)-Number(document.getElementById('stage').dataset.startMs))/1000"),4)
        index=self.slots.index(self.slot)
        following=next(s for s in self.slots[index+1:] if s['type']=='video')
        next_item=next(i for i in self.catalog if i['id']==following['contentId'])
        self.assertEqual(self.page.locator('#ident-title').inner_text(),next_item['title'])
        calls=self.page.evaluate('window.__ytCalls.length')
        self.page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        self.page.wait_for_function("document.getElementById('stage').dataset.slotType==='video'")
        self.page.wait_for_function(f"window.__ytCalls.length==={calls+1} && window.__ytCalls.at(-1).videoId==={json.dumps(next_item['youtubeId'])}")
        self.assertEqual(self.errors,[])
    def test_production_midnight_restarts_clock_cycle_not_catalogue(self):
        self.join_rayearth()
        self.page.evaluate(f"window.__nowMs=Date.parse({json.dumps(self.config['epoch'])})+86400000-1")
        self.page.wait_for_function("document.getElementById('stage').dataset.slotId==='"+self.slots[-1]['id']+"'")
        self.page.evaluate('window.__nowMs+=1')
        self.page.wait_for_function("document.getElementById('stage').dataset.slotId==='"+self.slots[0]['id']+"'")
        self.assertEqual(self.page.locator('#continuity').get_attribute('data-variant'),'night')
        self.assertEqual(self.errors,[])

if __name__=='__main__':unittest.main(verbosity=2)
