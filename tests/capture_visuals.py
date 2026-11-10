"""Capture original receiver/idents using the explicitly mocked API."""
import functools,http.server,threading
from browser_test import Handler,ROOT,FAKE_YOUTUBE
from playwright.sync_api import sync_playwright

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/disk-television/'
out=ROOT/'docs'/'evidence';out.mkdir(parents=True,exist_ok=True)
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        for name,iso,tune in [('receiver','2026-11-10T03:00:03Z',False),('ident-night','2026-11-10T03:00:03Z',True),('ident-next','2026-11-10T03:00:19Z',True),('ident-station','2026-11-10T11:00:03Z',True)]:
            page=browser.new_page(viewport={'width':1920,'height':1080})
            page.add_init_script(f"Date.now=()=>Date.parse('{iso}');")
            page.route('**/iframe_api',lambda r:r.fulfill(content_type='application/javascript',body=FAKE_YOUTUBE))
            page.goto(url);page.locator('#tune:not([disabled])').wait_for()
            if tune:page.locator('#tune').click()
            page.wait_for_timeout(1400)
            page.screenshot(path=str(out/f'{name}.png'),full_page=True)
            print(f'{name}: {page.locator("#ident-title").text_content()}')
            page.close()
        browser.close()
finally:
    server.shutdown();server.server_close()
