"""
NecroGit - Zero-Dependency HTTP Gateway & Streaming Séance Server
Module: app.server

Serves the Amber Phosphor CRT & Marigold Ofrenda web portal and provides
REST + Server-Sent Events (SSE) endpoints for code archaeology and AI séances.

Zero external dependencies (Python Standard Library only).
"""

import os
import sys

# Ensure repository root is on sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
import argparse
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional

from app.git_archaeology import GitArchaeologist, DeathCertificate
from app.engine import SeanceEngine


class NecroGitHandler(BaseHTTPRequestHandler):
    """HTTP request handler for NecroGit web app and REST API."""

    archaeologist: GitArchaeologist = None
    engine: SeanceEngine = None
    public_dir: str = ""
    assets_dir: str = ""

    # Suppress default log messages to keep terminal clean; print structured messages instead
    def log_message(self, format, *args):
        # Only log non-200 or API calls
        if "GET /api/" in format % args or "POST /api/" in format % args or " 404 " in format % args or " 500 " in format % args:
            sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {format % args}\n")

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Cache-Control")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, s-maxage=0")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # REST API Routes
        if path == "/api/status":
            self.handle_api_status()
        elif path == "/api/graveyard":
            self.handle_api_graveyard()
        elif path == "/api/diff":
            self.handle_api_diff(query)
        elif path.startswith("/assets/"):
            self.handle_asset_file(path[8:])
        else:
            # Static web app files
            self.handle_static_file(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/seance":
            self.handle_api_seance(query)
        else:
            self.send_error(404, "Endpoint Not Found")

    # -------------------------------------------------------------
    # API Handlers
    # -------------------------------------------------------------

    def handle_api_status(self):
        """Returns operational status of git repo and Ollama inference."""
        ollama_status = self.engine.check_ollama()
        payload = {
            "status": "online",
            "server": "NecroGit/1.0",
            "repo_name": os.path.basename(self.archaeologist.repo_path),
            "is_git_repository": self.archaeologist.is_git,
            "inference": ollama_status,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.send_json(payload)

    def handle_api_graveyard(self):
        """Excavates and returns the complete deceased code graveyard."""
        try:
            graveyard = self.archaeologist.get_full_graveyard()
            self.send_json(graveyard)
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_api_diff(self, query: Dict[str, list]):
        """Returns git diff or resurrected code for a specific commit and file."""
        commit = query.get("commit", [""])[0]
        file_path = query.get("file", [""])[0]

        if not commit or not file_path:
            self.send_json({"error": "Missing 'commit' or 'file' query parameter"}, status=400)
            return

        diff = self.archaeologist._get_commit_diff_for_file(commit, file_path)
        code = self.archaeologist._get_file_before_commit(commit, file_path)

        self.send_json({
            "commit": commit,
            "file_path": file_path,
            "diff": diff,
            "resurrected_code": code
        })

    def handle_api_seance(self, query: Dict[str, list]):
        """
        Conducts a spectral séance for an entity.
        Supports both standard JSON response and Server-Sent Events (SSE) streaming.
        """
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                cert = json.loads(body)
            except Exception:
                self.send_json({"error": "Invalid JSON body"}, status=400)
                return
        else:
            self.send_json({"error": "Missing request body"}, status=400)
            return

        # Check if client requested streaming
        is_stream = (
            query.get("stream", ["false"])[0].lower() in ("true", "1") or
            "text/event-stream" in self.headers.get("Accept", "")
        )

        if is_stream:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self._send_cors_headers()
            self.end_headers()

            # Stream spectral tokens
            for token in self.engine.stream_seance(cert):
                event_data = json.dumps({"token": token})
                self.wfile.write(f"data: {event_data}\n\n".encode("utf-8"))
                self.wfile.flush()
                # Slight atmospheric cadence for deterministic tokens
                time.sleep(0.015)

            # Signal completion
            self.wfile.write(b"data: {\"done\": true}\n\n")
            self.wfile.flush()
        else:
            result = self.engine.generate_seance(cert)
            self.send_json(result)

    def send_json(self, data: Any, status: int = 200):
        """Helper to send JSON response."""
        encoded = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(encoded)

    # -------------------------------------------------------------
    # Static File Handlers
    # -------------------------------------------------------------

    def handle_static_file(self, req_path: str):
        """Serves HTML, CSS, JS from public directory."""
        if req_path in ("/", ""):
            req_path = "/index.html"

        # Sanitize path to prevent directory traversal
        clean_path = os.path.normpath(req_path.lstrip("/"))
        file_path = os.path.join(self.public_dir, clean_path)

        if not os.path.isfile(file_path):
            self.send_error(404, f"File Not Found: {req_path}")
            return

        self._serve_file(file_path)

    def handle_asset_file(self, req_path: str):
        """Serves assets from assets directory."""
        clean_path = os.path.normpath(req_path.lstrip("/"))
        file_path = os.path.join(self.assets_dir, clean_path)

        if not os.path.isfile(file_path):
            self.send_error(404, f"Asset Not Found: {req_path}")
            return

        self._serve_file(file_path)

    def _serve_file(self, file_path: str):
        """Streams a static file to the client with appropriate headers."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"
        if mime_type.startswith("text/") or mime_type == "application/javascript":
            mime_type += "; charset=utf-8"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")


def run_server(
    port: int = 7777,
    host: str = "0.0.0.0",
    repo_path: str = ".",
    ollama_url: str = "http://localhost:11434",
    model: str = "gemma2:2b"
):
    """Launches the NecroGit ThreadingHTTPServer daemon."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    public_dir = os.path.join(base_dir, "public")
    assets_dir = os.path.join(base_dir, "assets")

    archaeologist = GitArchaeologist(repo_path)
    engine = SeanceEngine(ollama_url=ollama_url, model=model)

    NecroGitHandler.archaeologist = archaeologist
    NecroGitHandler.engine = engine
    NecroGitHandler.public_dir = public_dir
    NecroGitHandler.assets_dir = assets_dir

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, NecroGitHandler)

    status = engine.check_ollama()
    mode_str = "Gemma 2 (Local Ollama)" if status["model_ready"] else "Heuristic Necromancer (Air-Gapped Fallback)"

    print("=" * 64)
    print("🕯️  NECROGIT // THE FORENSIC GIT SÉANCE & OFRENDA DAEMON")
    print("=" * 64)
    print(f"📡 Web Portal:     http://localhost:{port}")
    print(f"🪦 Repository:     {os.path.abspath(repo_path)}")
    print(f"🧠 AI Mode:        {mode_str}")
    print(f"🔌 Ollama URL:     {ollama_url} ({'ONLINE' if status['online'] else 'OFFLINE'})")
    print(f"📦 Zero External Dependencies: Pure Python 3 Standard Library")
    print("=" * 64)
    print("Press Ctrl+C to dismiss the spirits and halt the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🕯️ Extinguishing altar candles. NecroGit daemon halted.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NecroGit Zero-Dependency HTTP Gateway & Séance Daemon")
    parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 7777)), help="Port to listen on (default: 7777)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to bind to (default: 0.0.0.0)")
    parser.add_argument("--repo", type=str, default=".", help="Path to git repository to excavate (default: .)")
    parser.add_argument("--ollama-url", type=str, default="http://localhost:11434", help="Ollama base URL (default: http://localhost:11434)")
    parser.add_argument("--model", type=str, default="gemma2:2b", help="Gemma model name (default: gemma2:2b)")

    args = parser.parse_args()
    run_server(
        port=args.port,
        host=args.host,
        repo_path=args.repo,
        ollama_url=args.ollama_url,
        model=args.model
    )
