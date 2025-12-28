"""
logging_global.py

Módulo responsável por prover a função global de logging do sistema
edge-risk-monitor.

Este módulo centraliza:
- Configuração global do logging
- Função log_system(), utilizada por TODOS os módulos

Regras arquiteturais:
- Nenhum outro módulo deve configurar logging
- main.py e módulos internos apenas chamam log_system()
- Evita dependência circular com main.py
"""

import logging
import sys
from typing import Any


# Configuração global do logging do sistema
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def log_system(level: int, message: str, **context: Any) -> None:
    """
    Registra mensagens de log de forma padronizada no sistema.

    Args:
        level (int):
            Nível do log (logging.INFO, logging.WARNING,
            logging.ERROR, etc).

        message (str):
            Mensagem principal a ser registrada.

        **context (Any):
            Contexto adicional estruturado que será anexado ao log.
    """
    if context:
        message = f"{message} | context={context}"

    logging.log(level, message)
