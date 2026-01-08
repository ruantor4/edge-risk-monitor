"""
system.py

Funções auxiliares relacionadas ao sistema operacional
utilizadas pelo projeto edge-risk-monitor.

Este módulo concentra utilitários de baixo nível que fornecem
informações do ambiente de execução, sem depender de serviços
externos ou de outras camadas da aplicação.

Não realiza I/O, logging ou integração com APIs. Seu escopo é
estritamente a obtenção de informações locais do sistema.

Escopo:
- Obtenção do endereço MAC do dispositivo local
"""

import uuid


def get_mac_address() -> str:
    """
    Obtém o endereço MAC do dispositivo local.

    O endereço é derivado a partir do identificador retornado
    pela biblioteca padrão `uuid`, sendo formatado no padrão
    hexadecimal com separador por dois pontos.

    Returns:
        str:
            Endereço MAC no formato XX:XX:XX:XX:XX:XX.
    """
    mac = uuid.getnode()
    mac_hex = ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    return mac_hex.upper()