"""
mock_server.py

Mock HTTP server para simular a API de recebimento de eventos
do projeto edge-risk-monitor durante o desenvolvimento.

Este módulo fornece um servidor HTTP simples, utilizado
exclusivamente em ambiente de desenvolvimento e testes,
permitindo validar o envio de eventos sem dependência
do serviço real de backend.

Não realiza validações de payload, persistência ou
processamento de dados. Seu papel é apenas simular
o endpoint de recebimento.

Escopo:
- Disponibilização de endpoint HTTP para requisições POST
- Registro básico de headers e corpo das requisições recebidas
- Simulação de resposta bem-sucedida da API externa
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class MockRiskAPIHandler(BaseHTTPRequestHandler):
    """
    Handler HTTP responsável por simular o endpoint
    de recebimento de eventos de risco.
    """
    def do_POST(self) -> None:
        """
        Manipula requisições HTTP POST recebidas pelo mock server.

        Lê o corpo da requisição, registra informações básicas
        de debug e retorna uma resposta HTTP de sucesso.
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

    Configura o logging básico e inicia o servidor
    escutando no host e porta informados.

    Args:
        host (str):
            Endereço onde o servidor irá escutar.

        port (int):
            Porta onde o servidor irá escutar.
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
