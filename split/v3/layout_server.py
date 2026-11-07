#!/usr/bin/env python3
"""Serve the layout page and accept layout.json / config.yaml updates."""

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import layout_to_config

HERE = layout_to_config.HERE


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 5_000_000:
            self._json(413, {"ok": False, "error": "layout is too large"})
            return
        try:
            layout = json.loads(self.rfile.read(length) or b"{}")
            if self.path == "/api/layout":
                keymap_count = layout_to_config.save_layout(layout)
                message = "Saved layout.json."
                if keymap_count is not None:
                    message += f" Wrote keymap.json ({keymap_count} keys)."
            elif self.path == "/api/config":
                message = layout_to_config.apply_config(layout)["message"]
            else:
                self._json(404, {"ok": False, "error": "unknown path"})
                return
        except Exception as exc:
            self._json(400, {"ok": False, "error": str(exc)})
            return
        self._json(200, {"ok": True, "message": message})

    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8765), Handler)
    print("layout server on http://0.0.0.0:8765", flush=True)
    server.serve_forever()
