"""Fixture-controlled UI tests; live API availability is checked separately."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json,re,shutil,tempfile,threading
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main():
 out=ROOT/'browser-checks';out.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as temporary:
  shutil.copytree(ROOT/'dist',Path(temporary)/'commonslens')
  server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=temporary));threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    data={'batchcomplete':'','query':{'pages':{'1':{'pageid':1,'title':'File:Test Harbour','index':1,'imageinfo':[{'descriptionurl':'https://commons.wikimedia.org/wiki/File:Test_Harbour','mediatype':'BITMAP','extmetadata':{'Artist':{'value':'Test creator'},'LicenseShortName':{'value':'CC BY-SA 4.0'},'LicenseUrl':{'value':'https://creativecommons.org/licenses/by-sa/4.0/'}}}]}}}}
    page.route('https://commons.wikimedia.org/w/api.php?**',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps(data)))
    page.goto(f'http://127.0.0.1:{server.server_port}/commonslens/');expect(page.locator('#presets button')).to_have_count(3)
    page.locator('#query').fill('Harbour');page.locator('#search').click();expect(page.locator('#cards')).to_contain_text('Test Harbour')
    page.get_by_role('button',name='Inspect & credit').click();expect(page.get_by_label('Attribution text')).to_have_value(re.compile('CC BY-SA'))
    page.get_by_role('button',name='Close',exact=True).click();page.get_by_role('button',name='Shortlist',exact=True).click();expect(page.locator('#saved-count')).to_have_text('1')
    with page.expect_download() as dl:page.locator('#save').click()
    receipt=json.loads(Path(dl.value.path()).read_text());assert receipt['schema']=='coolcode.commons.v1'
    page.locator('#search-mode').select_option('nearby')
    page.locator('#near-lat').fill('44.649');page.locator('#near-lon').fill('-63.575')
    # Query is separate from the cached subject search; bypass elapsed debounce deterministically.
    page.wait_for_timeout(1600)
    page.locator('#search').click();expect(page.locator('#status')).to_contain_text('geotagged files')
    expect(page.locator('#next')).to_be_disabled();expect(page.locator('#cards')).to_contain_text('Test Harbour')
    page.screenshot(path=str(out/'desktop.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'mobile overflow';page.screenshot(path=str(out/'mobile.png'),full_page=True)
    assert not errors,errors;browser.close()
  finally:server.shutdown()
 print('Commons Lens browser checks passed')
if __name__=='__main__':main()
