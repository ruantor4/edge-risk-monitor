"""
logging_global.py

Infraestrutura global de logging do projeto edge-risk-monitor.
"""

import logging
from datetime import datetime

from config.settings import LOGS_DIR


def setup_logging() -> None:
    """
    Configura o sistema de logging do projeto.

    Esta função deve ser chamada UMA VEZ no início do main.
    Após isso, qualquer módulo pode utilizar logging.getLogger().
    """

    # Garante que o diretório de logs exista
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Data atual para versionamento do arquivo de log
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Arquivo de log diário
    log_file = LOGS_DIR / f"edge-risk-monitor_{date_str}.log"

    # Formato do log
    log_format = "%(asctime)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
