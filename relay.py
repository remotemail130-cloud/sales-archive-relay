# sales-archive-relay — RouterOS -> Google Apps Script relay.
#
# WHY: RouterOS v6 /tool fetch does NOT follow HTTP 302 redirects.
# The Apps Script web app always answers POST /exec with
# "302 Found" to a script.googleusercontent.com echo URL (which only
# accepts GET). fetch reports "failure: closing connection: <302 ...>"
# and the batch never arrives. curl -L and browsers handle it fine
# (302 POST -> GET), urllib does the same — so this tiny relay does
# the hop for the router: the router POSTs here (plain 200, no
# redirect), the relay forwards to the Apps Script URL and returns
# the JSON answer {"ok":true,"added":N,"dup":M} verbatim.
#
# Stdlib only — no dependencies. Runs on Render Free.
# Env var ARCHIVE_URL = the Apps Script /exec URL (set in the Render
# dashboard, never in the repo). GET / answers "OK" (health check).
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib import request as urlreq
from urllib.error import HTTPError, URLError

TARGET = os.environ.get("ARCHIVE_URL", "")
PORT = int(os.environ.get("PORT", "10000"))


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        self._send(200, b"OK")

    def do_POST(self):
        if not TARGET:
            self._send(500, b'{"ok":false,"error":"ARCHIVE_URL not set"}')
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        body = self.rfile.read(n) if n > 0 else b""
        req = urlreq.Request(TARGET, data=body, method="POST",
                             headers={"Content-Type": "text/plain"})
        try:
            # urllib follows the 302 as a GET (like curl -L) and the
            # echo URL returns the doPost JSON answer.
            with urlreq.urlopen(req, timeout=120) as r:
                self._send(r.status, r.read(), "application/json")
        except HTTPError as e:
            self._send(e.code, e.read() or b"")
        except (URLError, TimeoutError) as e:
            self._send(502,
                        ('{"ok":false,"error":%r}' % str(e)).encode())

    def _send(self, code, data, ctype="text/plain"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
