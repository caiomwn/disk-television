"""Real Web Audio decode/start; only YouTube is doubled in this integration test."""
import functools,http.server,json,threading,unittest
from playwright.sync_api import sync_playwright
from browser_test import Handler,ROOT,FAKE_YOUTUBE
class AudioBrowserTests(unittest.TestCase):
    def test_real_local_audio_offsets_mute_and_dialogs_in_production(self):
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'_site')));threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as pw:
                browser=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
                page=browser.new_page(viewport={'width':1280,'height':720});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.add_init_script('''window.__nowMs=Date.parse('2026-11-10T03:00:02Z');Date.now=()=>window.__nowMs;window.__actualAudioStarts=[];const original=AudioBufferSourceNode.prototype.start;AudioBufferSourceNode.prototype.start=function(when,offset,duration){window.__actualAudioStarts.push({when,offset,duration,bufferDuration:this.buffer.duration,sampleRate:this.buffer.sampleRate,channels:this.buffer.numberOfChannels});return original.call(this,when,offset,duration);};''')
                page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
                page.goto(f'http://127.0.0.1:{server.server_port}/disk-television/');page.locator('#tune:not([disabled])').click()
                page.wait_for_function("document.getElementById('app').dataset.audioStarts==='1'",timeout=10000)
                page.wait_for_function("document.getElementById('app').dataset.audioVariants.split(',').length===3")
                self.assertEqual(page.evaluate('window.__actualAudioStarts[0].offset'),2)
                page.locator('#sound').click();page.wait_for_function("document.getElementById('app').dataset.audioActive==='false'")
                page.evaluate("window.__nowMs=Date.parse('2026-11-10T03:00:05Z')");page.locator('#sound').click();page.wait_for_function('window.__actualAudioStarts.length===2')
                self.assertEqual(page.evaluate('window.__actualAudioStarts[1].offset'),5)
                page.locator('#guide-open').click();page.wait_for_function("document.getElementById('app').dataset.audioActive==='false'")
                page.evaluate('window.__nowMs+=1000');page.locator('#guide-close').click();page.wait_for_function('window.__actualAudioStarts.length===3');self.assertEqual(page.evaluate('window.__actualAudioStarts[2].offset'),6)
                page.locator('#presentation-open').click();page.wait_for_function("document.getElementById('app').dataset.audioActive==='false'")
                page.evaluate('window.__nowMs+=1000');page.locator('#presentation-close').click();page.wait_for_function('window.__actualAudioStarts.length===4');self.assertEqual(page.evaluate('window.__actualAudioStarts[3].offset'),7)
                page.evaluate("window.__nowMs=Date.parse('2026-11-10T03:00:18Z')");page.wait_for_function('window.__ytCalls?.length===1');page.wait_for_function("document.getElementById('app').dataset.audioActive==='false'")
                evidence={'test':'real Chrome Web Audio; fake YouTube only','decodedAndStarted':page.evaluate('window.__actualAudioStarts'),'contextState':page.locator('#app').get_attribute('data-audio-state'),'readyVariants':page.locator('#app').get_attribute('data-audio-variants'),'errors':errors,'humanListening':False,'physicalSamsung':False}
                (ROOT/'docs/evidence/launch/audio-browser.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
                self.assertEqual(errors,[]);browser.close()
        finally:server.shutdown();server.server_close()
if __name__=='__main__':unittest.main(verbosity=2)
