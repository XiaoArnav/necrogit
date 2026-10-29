"""
Unit & Integration Tests: app.server
Zero external dependencies (pure Python unittest & urllib).
"""

import unittest
import threading
import urllib.request
import urllib.parse
import json
import os
import sys
import time
from http.server import ThreadingHTTPServer

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.server import NecroGitHandler
from app.git_archaeology import GitArchaeologist
from app.engine import SeanceEngine


class TestNecroGitServer(unittest.TestCase):
    server = None
    server_thread = None
    port = 7788
    base_url = f"http://127.0.0.1:{port}"

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        public_dir = os.path.join(base_dir, "public")
        assets_dir = os.path.join(base_dir, "assets")

        archaeologist = GitArchaeologist(base_dir)
        engine = SeanceEngine()

        NecroGitHandler.archaeologist = archaeologist
        NecroGitHandler.engine = engine
        NecroGitHandler.public_dir = public_dir
        NecroGitHandler.assets_dir = assets_dir

        cls.server = ThreadingHTTPServer(("127.0.0.1", cls.port), NecroGitHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.15)  # Wait for socket to bind

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    def test_api_status(self):
        """Verify GET /api/status returns 200 and valid JSON."""
        url = f"{self.base_url}/api/status"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "online")
            self.assertIn("inference", data)

    def test_api_graveyard(self):
        """Verify GET /api/graveyard returns 200 and deceased artifacts."""
        url = f"{self.base_url}/api/graveyard"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("deleted_files", data)
            self.assertIn("deleted_functions", data)

    def test_api_seance_post(self):
        """Verify POST /api/seance returns 200 with eulogy and validation."""
        url = f"{self.base_url}/api/seance"
        payload = {
            "entity_type": "function",
            "name": "fast_inverse_sqrt()",
            "file_path": "src/q_math.c",
            "death_commit": "c51b980a",
            "death_author": "John Carmack",
            "death_date": "1999-12-10",
            "death_message": "refactor: sse",
            "birth_commit": "0001",
            "birth_author": "Carmack",
            "lines_lost": 16
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("eulogy", data)
            self.assertIn("validation", data)
            self.assertTrue(data["validation"]["passed"])

    def test_static_files(self):
        """Verify index.html, style.css, and app.js serve with 200 OK and proper MIME types."""
        files = [
            ("/", "text/html"),
            ("/index.html", "text/html"),
            ("/style.css", "text/css"),
            ("/app.js", "javascript")
        ]

        for path, expected_mime in files:
            url = f"{self.base_url}{path}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200, f"Failed for {path}")
                content_type = resp.headers.get("Content-Type", "")
                self.assertIn(expected_mime, content_type, f"MIME mismatch for {path}: {content_type}")


if __name__ == "__main__":
    unittest.main()
