"""
system.py

Funções auxiliares relacionadas ao sistema operacional
utilizadas pelo projeto edge-risk-monitor.

Este módulo concentra utilitários de baixo nível que fornecem
informações locais do ambiente de execução, sem depender de
serviços externos ou de outras camadas da aplicação.

Não realiza:
- I/O em disco
- logging
- integração com APIs externas

Seu escopo é estritamente a obtenção de informações locais
necessárias para identificação e operação do edge.

Escopo:
- Obtenção de identificador único do dispositivo local (MAC lógico)
"""

import uuid


def get_mac_address() -> str:
    """
    Obtém um identificador de hardware do dispositivo local,
    utilizado como identificador lógico do edge.

    O valor é derivado a partir de `uuid.getnode()`, que normalmente
    retorna o endereço MAC de uma interface de rede. Em ambientes
    virtualizados ou restritos, pode retornar um identificador
    pseudoaleatório estável.

    Este identificador é utilizado para:
    - identificar unicamente o dispositivo edge
    - correlacionar eventos enviados ao backend
    - garantir rastreabilidade entre evidências e origem

    Returns:
        str:
            Identificador no formato hexadecimal
            XX:XX:XX:XX:XX:XX (uppercase).
    """
    mac = uuid.getnode()
    mac_hex = ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    return mac_hex.upper()
