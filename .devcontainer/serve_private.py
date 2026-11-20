#!/usr/bin/env python3
"""Serve website files after verifying the owner and private Codespaces port."""

import functools
import http.server
import json
import os
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
OWNER = "mt-hagar"
OWNER_ID = 229219657
PORT = 8088
FILES = frozenset({
    "index.html", "site.webmanifest", "favicon.ico",
    "apple-touch-icon.png", "apple-touch-icon-precomposed.png",
    "assets/favicon-16x16.png", "assets/favicon-32x32.png",
    "assets/hagrad-cardiac-heart-render.png",
    "assets/hagrad-ccta-iq-summary-screenshot.png",
    "assets/hagrad-heart-icon-192.png", "assets/hagrad-heart-icon.png",
    "assets/hagrad-noncalcified-plaque-profile.jpg",
    "assets/hagrad-qca-analysis-screenshot.png",
    "assets/hagrad-stent-analyzer-demo.mp4",
    "assets/noise-power-spectrum-workflow.jpg",
})


def gh(*args):
    # Never print credentials, signed URLs, or CLI error bodies.
    return subprocess.run(["gh", *args], check=True, capture_output=True,
                          text=True, timeout=30).stdout


def verify_gateway(name):
    if not name or os.environ.get("CODESPACES") != "true":
        raise RuntimeError("Start inside the owner's GitHub Codespace.")
    me = json.loads(gh("api", "user"))
    space = json.loads(gh("api", f"user/codespaces/{name}"))
    if (me.get("id") != OWNER_ID or me.get("login") != OWNER
            or space.get("owner", {}).get("id") != OWNER_ID
            or space.get("repository", {}).get("full_name") != f"{OWNER}/hagrad-website"
            or space.get("repository", {}).get("private") is not True):
        raise RuntimeError("Only mt-hagar's private website Codespace is allowed.")
    gh("codespace", "ports", "visibility", f"{PORT}:private", "-c", name)
    ports = json.loads(gh("codespace", "ports", "-c", name,
                         "--json", "sourcePort,visibility"))
    if not any(p.get("sourcePort") == PORT and p.get("visibility") == "private"
               for p in ports):
        raise RuntimeError("Private port verification failed.")
    if any(p.get("visibility") != "private" for p in ports):
        raise RuntimeError("Remove non-private forwarded ports before starting.")


class SiteHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = unquote(urlsplit(self.path).path)
        name = "index.html" if path == "/" else path.removeprefix("/")
        target = ROOT / name
        if (name not in FILES or not target.is_file()
                or any(p.is_symlink() for p in (target, *target.parents))):
            self.send_error(404)
            return None
        self.path = "/" + name
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def log_message(self, format, *args):
        pass


def main():
    try:
        verify_gateway(os.environ.get("CODESPACE_NAME"))
    except (RuntimeError, subprocess.SubprocessError, OSError, ValueError):
        raise SystemExit("Access verification failed. No server started. See PRIVATE_ACCESS.md.")
    handler = functools.partial(SiteHandler, directory=str(ROOT))
    print("Owner and private port verified. Serving static website on loopback port 8088.")
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
