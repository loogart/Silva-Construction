from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,io
ROOT=Path(__file__).resolve().parents[1]
class Preview(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
 def log_request(self,code="-",size="-"):
  if isinstance(code,int) and code>=400:print(self.path,code,flush=True)
 def send_head(self):
  path=Path(self.translate_path(self.path))
  if path.is_dir():path=path/'index.html'
  if path.is_file() and path.suffix=='.html':
   body=path.read_bytes().replace(b'</body>',b'<script src="/review/ready.js"></script></body>')
   self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();return io.BytesIO(body)
  return super().send_head()
 def end_headers(self):
  # Preserve the original files byte-for-byte; block third-party scripts during comparison.
  self.send_header('Content-Security-Policy',"script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-src 'self' https://www.google.com; object-src 'none'")
  self.send_header('Cache-Control','no-store');super().end_headers()
print('Silva comparison: http://localhost:8765/review/',flush=True)
ThreadingHTTPServer(('127.0.0.1',8765),Preview).serve_forever()
