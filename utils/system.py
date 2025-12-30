"""
system.py

Funções auxiliares relacionadas ao sistema operacional.
"""

import uuid


def get_mac_address() -> str:
    """
    Obtém o endereço MAC do dispositivo local.

    Returns:
        str: Endereço MAC no formato XX:XX:XX:XX:XX:XX
    """
    mac = uuid.getnode()
    mac_hex = ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    return mac_hex.upper()