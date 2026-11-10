"""Asset and package integrity checks, independent of YouTube/network."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

class AssetTests(unittest.TestCase):
    def test_png_is_real_large_rgba_with_transparency(self):
        path=ROOT/'assets/logo.png'
        self.assertEqual(path.read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
        with Image.open(path) as image:
            self.assertEqual(image.format,'PNG');self.assertEqual(image.mode,'RGBA')
            self.assertEqual(image.size,(2400,1050));self.assertEqual(image.getchannel('A').getextrema(),(0,255))
        with Image.open(path) as image:
            image.verify()
    def test_svg_source_is_editable_and_has_no_external_assets(self):
        for name in ['logo.svg','favicon.svg']:
            root=ET.parse(ROOT/'assets'/name).getroot()
            self.assertTrue(root.tag.endswith('svg'))
            self.assertTrue(root.attrib.get('viewBox'))
            self.assertGreater(len(root.findall('.//{http://www.w3.org/2000/svg}path')),10)
            text=(ROOT/'assets'/name).read_text(encoding='utf-8')
            self.assertNotIn('<image',text);self.assertNotIn('@import',text)
    def test_static_page_resources_are_relative_and_exist(self):
        text=(ROOT/'index.html').read_text(encoding='utf-8')
        for resource in re.findall(r'(?:src|href)="([^"]+)"',text):
            self.assertTrue(resource.startswith('./'),resource)
            self.assertTrue((ROOT/resource).is_file(),resource)
        self.assertTrue((ROOT/'.nojekyll').is_file())
    def test_catalog_has_explicit_verification_and_valid_tokens(self):
        catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
        original=json.loads((ROOT/'tests/fixtures/dt001/catalog.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(catalog),len(original))
        self.assertTrue({item['youtubeId'] for item in original}.issubset({item['youtubeId'] for item in catalog}))
        self.assertEqual(len({item['id'] for item in catalog}),len(catalog))
        for item in catalog:
            self.assertRegex(item['youtubeId'],r'^[A-Za-z0-9_-]{11}$')
            self.assertEqual(item['sourceUrl'],'https://www.youtube.com/watch?v='+item['youtubeId'])
            for field in ['checkedAt','method','embeddability','regionalAvailability']:
                self.assertTrue(item['verification'][field])

if __name__=='__main__':unittest.main(verbosity=2)
