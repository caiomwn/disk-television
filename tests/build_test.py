"""Production is a self-contained static tree, not the development server."""
from pathlib import Path
import json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
class BuildTests(unittest.TestCase):
    def test_build_contains_relative_bundle_audio_and_no_private_workspace(self):
        self.assertTrue((ROOT/'tools/build.py').is_file(),'production builder missing')
        result=subprocess.run([sys.executable,str(ROOT/'tools/build.py')],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        out=ROOT/'_site';html=(out/'index.html').read_text(encoding='utf-8')
        self.assertIn('./app.bundle.js',html);self.assertNotIn('type="module"',html)
        for name in ['index.html','legal.html','styles.css','presentation.css','app.bundle.js','data/catalog.json','data/schedule.json','.nojekyll','release.json']:
            self.assertTrue((out/name).is_file(),name)
        self.assertFalse((out/'.venv').exists());self.assertFalse((out/'node_modules').exists());self.assertFalse((out/'research').exists())
        self.assertTrue(json.loads((out/'release.json').read_text())['files'])
        bundle=(out/'app.bundle.js').read_text(encoding='utf-8')
        self.assertNotIn('C:\\Users\\padoka77',bundle)
        self.assertNotIn('BEGIN PRIVATE KEY',bundle)

if __name__=='__main__':unittest.main(verbosity=2)
