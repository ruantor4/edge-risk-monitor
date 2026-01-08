"""
logging_global.py

Módulo responsável por prover a infraestrutura global de logging
do projeto edge-risk-monitor.

Este módulo centraliza a configuração do sistema de logging e
disponibiliza a função log_system(), utilizada por todos os
componentes da aplicação.

Regras arquiteturais:
- Nenhum outro módulo deve configurar logging
- main.py e módulos internos apenas utilizam log_system()
- Evita dependência circular com o ponto de entrada da aplicação

Escopo:
- Configuração global do logging do sistema
- Definição de handlers de saída (stdout e arquivo)
- Padronização do formato das mensagens de log
- Registro de mensagens com contexto estruturado
"""

import logging
import sys
from typing import Any


# ============================================================
# CONFIGURAÇÃO GLOBAL DO LOGGING
# ============================================================

# Configuração central do sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),                     
        logging.FileHandler("logs/edge-risk-monitor.log",    
                            encoding="utf-8"),
    ],
)

# ============================================================
# FUNÇÃO GLOBAL DE LOG
# ============================================================

def log_system(level: int, message: str, **context: Any) -> None:
    """
    Registra mensagens de log de forma padronizada no sistema.

    Esta função deve ser utilizada por todos os módulos do projeto,
    garantindo consistência no formato e no tratamento de logs.

    Args:
        level (int):
            Nível do log (logging.INFO, logging.WARNING,
            logging.ERROR, etc).

        message (str):
            Mensagem principal a ser registrada.

        **context (Any):
            Contexto adicional estruturado anexado à mensagem de log.
    """
    if context:
        message = f"{message} | context={context}"

    logging.log(level, message)
