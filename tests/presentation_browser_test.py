"""DT-003 presentation experiment; same production clock/data, labelled API double."""
import functools,http.server,threading,unittest
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT,FAKE_YOUTUBE

class PresentationBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/disk-television/'
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.page=self.browser.new_page(viewport={'width':1920,'height':1080});self.errors=[];self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;")
        self.page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
    def tearDown(self):self.page.close()
    def test_initial_selection_switch_and_session_persistence(self):
        self.page.goto(self.url);self.page.locator('#tune:not([disabled])').wait_for()
        self.assertEqual(self.page.locator('#gate [data-presentation]').count(),3,'three presentation choices must exist')
        self.page.locator('#gate [data-presentation="A"]').click();self.page.locator('#tune').click();self.page.wait_for_function('window.__ytCalls?.length===1')
        first=self.page.evaluate('window.__ytCalls[0].videoId')
        offset=self.page.evaluate('window.__ytCalls[0].startSeconds')
        self.page.locator('#presentation-open').click();self.assertTrue(self.page.locator('#presentation-dialog').is_visible());self.assertFalse(self.page.locator('#player-shell').is_visible())
        self.page.evaluate('window.__nowMs+=30000')
        self.page.locator('#presentation-dialog [data-presentation="C"]').click();self.page.locator('#presentation-close').click()
        self.page.wait_for_function('window.__ytCalls.length===2')
        self.assertEqual(self.page.evaluate('window.__ytCalls.at(-1).videoId'),first)
        self.assertEqual(self.page.evaluate('window.__ytCalls.at(-1).startSeconds'),offset+30)
        self.assertEqual(self.page.locator('#app').get_attribute('data-presentation'),'C')
        self.page.reload();self.page.locator('#tune:not([disabled])').wait_for()
        self.assertEqual(self.page.locator('#app').get_attribute('data-presentation'),'C')
        self.assertEqual(self.errors,[])

    def test_modes_leave_official_player_uncovered(self):
        self.page.goto(self.url);self.page.locator('#tune:not([disabled])').wait_for();self.page.locator('#tune').click();self.page.wait_for_function('window.__ytCalls?.length===1')
        for mode in ['A','B','C']:
            self.page.locator('#presentation-open').click();self.page.locator(f'#presentation-dialog [data-presentation="{mode}"]').click();self.page.locator('#presentation-close').click()
            self.page.wait_for_function("!document.getElementById('player-shell').hidden")
            geometry=self.page.locator('#youtube-player').evaluate('''e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,points:[[r.left+3,r.top+3],[r.right-3,r.top+3],[r.left+3,r.bottom-3],[r.right-3,r.bottom-3],[r.left+r.width/2,r.top+r.height/2]].every(([x,y])=>document.elementFromPoint(x,y)===e)}}''')
            self.assertGreaterEqual(geometry['width'],200);self.assertGreaterEqual(geometry['height'],200);self.assertTrue(geometry['points'],mode+' overlays the official iframe')
            if mode=='C':
                self.assertTrue(self.page.evaluate('''()=>{const f=document.getElementById('youtube-player').getBoundingClientRect();return [...document.querySelectorAll('.experimental-mark')].every(e=>{const r=e.getBoundingClientRect();return r.right<=f.left||r.left>=f.right||r.bottom<=f.top||r.top>=f.bottom})}'''))
        self.assertEqual(self.errors,[])

    def test_clean_mode_hides_chrome_but_keeps_reveal_control_outside_player(self):
        self.page.goto(self.url);self.page.locator('#tune:not([disabled])').wait_for();self.page.locator('#gate [data-presentation="A"]').click();self.page.locator('#tune').click();self.page.wait_for_function('window.__ytCalls?.length===1')
        before=self.page.locator('#youtube-player').bounding_box()['height']
        self.page.wait_for_function("document.getElementById('app').dataset.chrome==='hidden'",timeout=7000)
        after=self.page.locator('#youtube-player').bounding_box()['height']
        self.assertGreater(after,before);self.assertTrue(self.page.locator('#reveal-controls').is_visible())
        self.page.locator('#reveal-controls').click();self.assertEqual(self.page.locator('#app').get_attribute('data-chrome'),'visible')
        self.page.locator('#presentation-open').click();self.page.keyboard.press('ArrowRight');self.page.keyboard.press('Escape');self.assertFalse(self.page.locator('#presentation-dialog').is_visible())
        self.page.locator('#presentation-open').click()
        self.page.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Unidentified',keyCode:39,bubbles:true}))")
        self.assertEqual(self.page.evaluate('document.activeElement.dataset.presentation'),'B')
        self.page.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Unidentified',keyCode:10009,bubbles:true}))")
        self.assertFalse(self.page.locator('#presentation-dialog').is_visible())
        self.assertEqual(self.errors,[])

if __name__=='__main__':unittest.main(verbosity=2)
