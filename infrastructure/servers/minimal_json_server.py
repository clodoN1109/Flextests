import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 3132
FILE_PATH: Path = Path(sys.argv[1])
FILENAME = FILE_PATH.name

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == f"/{FILENAME}":
            if os.path.exists(FILE_PATH):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                with open(FILE_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, f"{FILENAME} not found on server.")
        elif self.path == "/favicon.ico":
            # Suppress favicon errors
            self.end_headers()
        else:
            self.send_error(404, "File not found.")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {FILENAME} at http://localhost:{PORT}/{FILENAME}")
        httpd.serve_forever()

