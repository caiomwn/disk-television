"""Development preview only. GitHub Pages does not run or need this server."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import webbrowser

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Abrir a DISK TELEVISION localmente.')
parser.add_argument('--port',type=int,default=8080)
parser.add_argument('--no-open',action='store_true')
args=parser.parse_args()
try:
    server=ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
except OSError as error:
    raise SystemExit(f'Não foi possível abrir a porta {args.port}: {error}. Tente --port 8081.')
url=f'http://127.0.0.1:{server.server_port}/'
print(url,flush=True)
if not args.no_open:webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
