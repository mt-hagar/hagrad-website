import functools
import http.client
import http.server
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import serve_private as site


class GatewayTests(unittest.TestCase):
    def verify(self, *, user_id=site.OWNER_ID, owner_id=site.OWNER_ID,
               private=True, repository="mt-hagar/hagrad-website", ports=None):
        answers = [json.dumps({"id": user_id, "login": site.OWNER}),
                   json.dumps({"owner": {"id": owner_id},
                               "repository": {"full_name": repository, "private": private}}),
                   "", json.dumps(ports if ports is not None else [
                       {"sourcePort": site.PORT, "visibility": "private"}])]
        with patch.dict(os.environ, {"CODESPACES": "true"}), patch.object(site, "gh", side_effect=answers):
            site.verify_gateway("test-codespace")

    def test_owner_private_port(self):
        self.verify()

    def test_wrong_identity_repository_and_visibility(self):
        for args in [{"user_id": 1}, {"owner_id": 1}, {"private": False},
                     {"repository": "mt-hagar/hagrad-viewer"}, {"ports": []},
                     {"ports": [{"sourcePort": site.PORT, "visibility": "public"}]},
                     {"ports": [{"sourcePort": site.PORT, "visibility": "private"},
                                {"sourcePort": 9000, "visibility": "org"}]}]:
            with self.subTest(args=args), self.assertRaises(RuntimeError):
                self.verify(**args)

    def test_outside_codespaces(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(RuntimeError):
            site.verify_gateway("test")

    def test_failed_verification_never_binds(self):
        with patch.object(site, "verify_gateway", side_effect=OSError), \
                patch.object(site.http.server, "ThreadingHTTPServer") as server:
            with self.assertRaises(SystemExit):
                site.main()
            server.assert_not_called()


class StaticFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        (self.root / "index.html").write_text("owner-only website")
        (self.root / "secret.txt").write_text("not served")
        (self.root / "favicon.ico").symlink_to(self.root / "secret.txt")
        self.root_patch = patch.object(site, "ROOT", self.root)
        self.root_patch.start()
        handler = functools.partial(site.SiteHandler, directory=str(self.root))
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.root_patch.stop()
        self.directory.cleanup()

    def request(self, path, method="GET"):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=5)
        try:
            connection.request(method, path)
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def test_home_and_no_store(self):
        for path in ["/", "/index.html", "/?test=1"]:
            status, headers, body = self.request(path)
            self.assertEqual(status, 200)
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertEqual(body, b"owner-only website")
        self.assertEqual(self.request("/", "HEAD")[2], b"")

    def test_no_secrets_traversal_directories_or_symlinks(self):
        for path in ["/.git/config", "/.env", "/.devcontainer/serve_private.py",
                     "/PRIVATE_ACCESS.md", "/secret.txt", "/assets/", "/favicon.ico",
                     "/../secret.txt", "/%2e%2e/secret.txt", "/%2e%2e%2fsecret.txt"]:
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)

    def test_no_upload_signup_or_login_routes(self):
        for path in ["/signup", "/register", "/invite", "/login"]:
            self.assertEqual(self.request(path)[0], 404)
        self.assertEqual(self.request("/", "POST")[0], 501)


if __name__ == "__main__":
    unittest.main()
