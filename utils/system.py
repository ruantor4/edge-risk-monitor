
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
        str:
            Identificador no formato hexadecimal
            XX:XX:XX:XX:XX:XX (uppercase).
    """
    mac = uuid.getnode()
    mac_hex = ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    return mac_hex.upper()

