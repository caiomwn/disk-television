"""Evidence classifier tests: metadata and mere player readiness are not playback."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class EmbedEvidenceTests(unittest.TestCase):
    def load_classifier(self):
        path=ROOT/'tools/verify_embeds.py'
        self.assertTrue(path.is_file(),'embed verifier missing')
        spec=importlib.util.spec_from_file_location('embed_verifier',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module.playback_confirmed
    def test_requires_matching_video_real_content_duration_and_advancing_time(self):
        classify=self.load_classifier()
        good=[{'state':1,'videoId':'abcdefghijk','duration':1440,'time':5.2},{'state':1,'videoId':'abcdefghijk','duration':1440,'time':6.3}]
        self.assertTrue(classify('abcdefghijk',1440,good,[]))
        for bad in [[],good[:1],[{**s,'videoId':'ABCDEFGHIJK'} for s in good],[{**s,'state':3} for s in good],[{**s,'duration':30} for s in good],[{**s,'time':5.2} for s in good]]:
            self.assertFalse(classify('abcdefghijk',1440,bad,[]))
        self.assertFalse(classify('abcdefghijk',1440,good,[150]))

if __name__=='__main__':unittest.main(verbosity=2)
