"""
mock_server.py

Mock HTTP server para simular o risk-monitor-api
durante o desenvolvimento do edge-risk-monitor.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class MockRiskAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        logging.info("POST recebido em %s", self.path)
        logging.info("Headers:\n%s", self.headers)
        logging.info("Body size: %d bytes", len(body))

        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format: str, *args) -> None:
        # Evita log duplicado no stdout
        return


def run(host: str = "localhost", port: int = 8001) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | MOCK | %(levelname)s | %(message)s",
    )

    server = HTTPServer((host, port), MockRiskAPIHandler)
    logging.info("Mock risk-monitor-api rodando em http://%s:%d", host, port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Mock server finalizado")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
