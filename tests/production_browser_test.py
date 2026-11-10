"""Exercise the actual production bundle under a GitHub Pages repository prefix."""
import functools,http.server,threading,unittest
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT,FAKE_YOUTUBE

class ProductionBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'_site')));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/disk-television/'
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close()
    def test_bundle_subpath_polyfills_refresh_and_failure_recovery(self):
        page=self.browser.new_page(viewport={'width':1280,'height':720});errors=[];missing=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:missing.append(r.url) if r.status>=400 and r.url.startswith(self.url) else None)
        page.add_init_script("window.__nowMs=Date.parse('2026-11-10T03:00:48Z');Date.now=()=>window.__nowMs;delete Array.prototype.at;delete Element.prototype.replaceChildren;delete Promise.allSettled;")
        page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
        response=page.goto(self.url);self.assertEqual(response.status,200)
        page.locator('#tune').click();page.wait_for_function('window.__ytCalls?.length===1')
        offset=page.evaluate('window.__ytCalls[0].startSeconds');self.assertGreater(offset,0)
        self.assertEqual(offset,float(page.locator('#stage').get_attribute('data-elapsed')))
        page.reload();page.locator('#tune').click();page.wait_for_function('window.__ytCalls?.length===1');self.assertEqual(page.evaluate('window.__ytCalls[0].startSeconds'),offset)
        page.wait_for_function("document.getElementById('station-state').textContent==='NO AR'")
        page.evaluate('window.__fakePlayer.opts.events.onError({data:150})');self.assertTrue(page.locator('#continuity').is_visible())
        page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
        page.wait_for_function("document.getElementById('stage').dataset.slotType==='ident'")
        for i in range(3):
            page.evaluate("window.__nowMs=Number(document.getElementById('stage').dataset.endMs)")
            page.wait_for_timeout(300)
            if page.locator('#stage').get_attribute('data-slot-type')=='video':break
        page.wait_for_function('window.__ytCalls.length===2')
        page.locator('#guide-open').click();self.assertTrue(page.locator('#guide').is_visible());page.keyboard.press('Escape');self.assertFalse(page.locator('#guide').is_visible())
        page.locator('#legal-link').click();self.assertEqual(page.title(),'Termos e privacidade — DISK TELEVISION')
        page.reload();self.assertEqual(page.title(),'Termos e privacidade — DISK TELEVISION')
        self.assertEqual(errors,[]);self.assertEqual(missing,[])
        page.close()

if __name__=='__main__':unittest.main(verbosity=2)
