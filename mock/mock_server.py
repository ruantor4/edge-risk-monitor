from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class MockRiskAPIHandler(BaseHTTPRequestHandler):
    """
    Simula o endpoint HTTP de recebimento de eventos de risco.

    Este handler é utilizado exclusivamente em ambiente de
    desenvolvimento para validar o envio de requisições HTTP
    pelo edge sem dependência do backend real.
    """
    
    def do_POST(self) -> None:
        """
        Manipula requisições HTTP POST recebidas pelo mock server.

        Lê o corpo da requisição, registra informações básicas
        para debug e retorna uma resposta HTTP simulando sucesso.
        """
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        logging.info("POST recebido em %s", self.path)
        logging.info("Headers:\n%s", self.headers)
        logging.info("Body size: %d bytes", len(body))

        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format: str, *args) -> None:
        """
        Sobrescreve o método padrão de logging do BaseHTTPRequestHandler
        para evitar logs duplicados no stdout.
        """
        # Evita log duplicado no stdout
        return


def run(host: str = "localhost", port: int = 8001) -> None:
    """
    Inicializa e executa o mock server HTTP.

    O servidor é iniciado com logging básico e permanece
    escutando requisições até ser interrompido manualmente.
    """
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
