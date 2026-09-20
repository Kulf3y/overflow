import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from overflow.policy import validate_policy
from overflow.privacy import redact_text
from overflow.security import scan_text


def route_request(method, path, payload=None):
    if method == "GET" and path == "/":
        return 200, {
            "name": "Overflow Gateway",
            "status": "early development"
        }

    if method == "GET" and path == "/v1/health":
        return 200, {
            "status": "ok"
        }

    if method == "POST" and path == "/v1/check":
        if not isinstance(payload, dict):
            return 400, {"error": "payload must be a JSON object"}

        text = payload.get("text")

        if not isinstance(text, str):
            return 400, {"error": "text must be a string"}

        report = redact_text(text)

        return 200, {
            "redacted": report.output,
            "counts": report.counts
        }

    if method == "POST" and path == "/v1/security":
        if not isinstance(payload, dict):
            return 400, {"error": "payload must be a JSON object"}

        text = payload.get("text")

        if not isinstance(text, str):
            return 400, {"error": "text must be a string"}

        report = scan_text(text)

        return 200, {
            "allowed": report.allowed,
            "reasons": report.reasons,
            "counts": report.counts
        }

    if method == "POST" and path == "/v1/policy/validate":
        if not isinstance(payload, dict):
            return 400, {"error": "payload must be a JSON object"}

        policy = payload.get("policy", payload)
        errors = validate_policy(policy)

        if errors:
            return 400, {
                "valid": False,
                "errors": errors
            }

        return 200, {
            "valid": True
        }

    return 404, {"error": "not found"}


class OverflowGatewayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send_json(self, status, data):
        body = json.dumps(data, sort_keys=True).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length_header = self.headers.get("Content-Length", "0")

        try:
            length = int(length_header)
        except ValueError:
            return None

        if length <= 0:
            return {}

        raw = self.rfile.read(length)

        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    def do_GET(self):
        path = self.path.split("?")[0]
        status, data = route_request("GET", path)
        self._send_json(status, data)

    def do_POST(self):
        path = self.path.split("?")[0]
        payload = self._read_json()

        if payload is None:
            self._send_json(400, {"error": "invalid JSON"})
            return

        status, data = route_request("POST", path, payload)
        self._send_json(status, data)

    def log_message(self, format, *args):
        pass


def serve(host="127.0.0.1", port=8080):
    server = ThreadingHTTPServer((host, port), OverflowGatewayHandler)
    print(f"Overflow gateway listening on http://{host}:{port}")
    server.serve_forever()
