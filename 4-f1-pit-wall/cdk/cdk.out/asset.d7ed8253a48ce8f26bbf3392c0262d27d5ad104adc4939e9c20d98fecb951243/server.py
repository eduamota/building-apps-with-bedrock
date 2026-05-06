"""Local development server for F1 Pit Wall agent."""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, ".")
from agents.supervisor import create_supervisor_agent

print("Creating supervisor agent...")
agent = create_supervisor_agent()
print("✅ Agent ready")


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            message = body.get("message", "")

            if not message:
                self._respond(400, {"error": "message field is required"})
                return

            print(f"\n📨 Query: {message}")
            result = agent(message)
            print(f"✅ Response generated")

            # Extract text from result - handle both string and structured responses
            msg = result.message
            if isinstance(msg, dict):
                content = msg.get("content", [])
                text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
            elif isinstance(msg, str):
                text = msg
            else:
                text = str(msg)

            # Remove <thinking>...</thinking> tags
            import re
            text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL).strip()

            self._respond(200, {"response": text, "session_id": body.get("session_id", "default")})
        else:
            self._respond(404, {"error": "Not found"})

    def _respond(self, code, data):
        self.send_response(code)
        self._cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass  # Suppress default logging


if __name__ == "__main__":
    port = 8080
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"🏎️  F1 Pit Wall API running at http://localhost:{port}/chat")
    print("Press Ctrl+C to stop\n")
    server.serve_forever()
