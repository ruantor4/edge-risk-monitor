"""
main.py

Ponto de entrada do sistema edge-risk-monitor.

Responsabilidades:
- Criar diretórios necessários (logs)
- Orquestrar o fluxo inicial
- Validar funcionamento da webcam

Este arquivo NÃO deve ser importado por outros módulos.
"""

from pathlib import Path
import time
import logging

from webcam.webcam import Webcam
from utils.logging_global import log_system


def main() -> None:
    """
    Função principal da aplicação.

    Executa um loop simples de captura de frames apenas
    para validação do funcionamento da webcam.
    """
    # Criação centralizada da pasta de logs
    Path("logs").mkdir(exist_ok=True)

    log_system(logging.INFO, "Iniciando edge-risk-monitor (teste de webcam)")

    webcam = Webcam(index=0, width=640, height=480)

    if not webcam.open():
        log_system(logging.ERROR, "Não foi possível inicializar a webcam")
        return

    try:
        for _ in range(50):
            webcam.read()
            time.sleep(0.05)

    finally:
        webcam.release()
        log_system(logging.INFO, "Aplicação finalizada")


if __name__ == "__main__":
    main()
