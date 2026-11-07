#!/usr/bin/env python3
"""Uncrustables line - LOCAL private-app server (no Cloudflare account needed).

Serves the keyframes in worker/frames/ over plain http on your network, the way
the Glance private-app docs describe for a Raspberry Pi. Same behaviour as
worker/_worker.js: one keyframe per STEP seconds, looping. The machine running
this has to stay on and reachable from the Glance, so the Cloudflare worker is
the better home for it long term.

  python3 serve.py              # http://<this-machine's-ip>:8787/
  python3 serve.py --port 9000 --step 60

Paste http://<ip>:8787/ into Glance Setup > Apps > Private Apps with the
refresh interval equal to --step. Needs only the standard library.
"""
import argparse
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

FRAMES_DIR = Path(__file__).parent / "worker" / "frames"
FRAMES = [p.read_bytes() for p in sorted(FRAMES_DIR.glob("k*.png"))]
STEP = 60


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        n = len(FRAMES)
        if "frame" in q and q["frame"][0] != "":
            try:
                idx = int(q["frame"][0]) % n
            except ValueError:
                idx = 0
        else:
            try:
                step = max(1, int(q.get("step", [STEP])[0]))
            except ValueError:
                step = STEP
            idx = int(time.time() // step) % n
        body = FRAMES[idx]
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, max-age=0")
        self.send_header("X-Frame-Index", str(idx))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(time.strftime("%H:%M:%S"), self.client_address[0], fmt % args)


def main():
    global STEP
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--step", type=int, default=60, help="seconds per keyframe (match the Glance refresh)")
    args = ap.parse_args()
    STEP = args.step
    if not FRAMES:
        raise SystemExit(f"no keyframes in {FRAMES_DIR}; run build_worker.py first")
    print(f"serving {len(FRAMES)} keyframes, one per {STEP}s, on http://0.0.0.0:{args.port}/  (Ctrl+C to stop)")
    ThreadingHTTPServer(("0.0.0.0", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
