"""Verify the same local server used by ABRIR-LOCAL.cmd."""
from pathlib import Path
import subprocess,sys,unittest,urllib.request
ROOT=Path(__file__).resolve().parents[1]

class LauncherTests(unittest.TestCase):
    def test_local_server_binds_then_serves_the_application(self):
        self.assertTrue((ROOT/'tools/serve.py').is_file(),'local server implementation missing')
        process=subprocess.Popen([sys.executable,str(ROOT/'tools/serve.py'),'--port','0','--no-open'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
        try:
            url=process.stdout.readline().strip()
            self.assertTrue(url.startswith('http://127.0.0.1:'))
            with urllib.request.urlopen(url,timeout=10) as response:
                self.assertEqual(response.status,200)
                self.assertIn('DISK TELEVISION',response.read().decode('utf-8'))
            with urllib.request.urlopen(url+'data/schedule.json',timeout=10) as response:
                self.assertEqual(response.status,200)
        finally:
            process.terminate();process.communicate(timeout=10)

if __name__=='__main__':unittest.main(verbosity=2)
