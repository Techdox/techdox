"""Build and test without touching production or requiring a persistent server."""
import functools
import http.server
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

with tempfile.TemporaryDirectory(prefix='techdox-test-') as directory:
    subprocess.run([os.environ.get('HUGO_BIN', 'hugo'), '--gc', '--minify', '--destination', directory], cwd=ROOT, check=True)
    handler = functools.partial(QuietHandler, directory=directory)
    with http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        env = {**os.environ, 'BLOG_BUILD': directory, 'BLOG_TEST_URL': f'http://127.0.0.1:{server.server_port}'}
        try:
            result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_reading_*.py', '-v'], cwd=ROOT, env=env)
        finally:
            server.shutdown()
            thread.join()
        sys.exit(result.returncode)
