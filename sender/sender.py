"""
sender.py

Responsável pelo envio de eventos de detecção do projeto
edge-risk-monitor para o backend risk-monitor-api.

Este módulo encapsula a comunicação HTTP com a API externa,
realizando o envio de payload estruturado juntamente com
evidências visuais associadas ao evento detectado.

Não realiza validação semântica de payload, persistência
local ou controle de estado. Seu escopo é estritamente
o despacho de eventos para o backend.

Escopo:
- Envio de payload estruturado no formato HTTP
- Anexação de evidência visual (imagem)
- Tratamento de falhas de comunicação com a API
- Registro de logs de sucesso e erro
"""

from pathlib import Path
from typing import Dict
import logging

import requests
from requests import Response, RequestException

logger = logging.getLogger(__name__)

class EventSender:
    """
    Cliente HTTP responsável por enviar eventos de detecção
    para o serviço backend risk-monitor-api.

    Esta classe é stateless e assume que o payload recebido
    já foi validado e estruturado por camadas superiores
    da aplicação.
    """

    def __init__(self, api_url: str, timeout: int = 10) -> None:
        """
        Inicializa o componente de envio de eventos.

        Args:
            api_url (str):
                URL do endpoint da API responsável por receber os eventos.

            timeout (int):
                Timeout máximo da requisição HTTP em segundos.
        """
        self.api_url = api_url
        self.timeout = timeout

    def send_event(
        self,
        payload: Dict[str, str],
        evidence_path: Path,
    ) -> bool:
        """
        Envia um evento de detecção para o backend.

        O envio consiste em um payload estruturado acompanhado
        de um arquivo de evidência visual anexado à requisição.

        O payload deve ser construído externamente e conter,
        no mínimo, os campos exigidos pela API (ex.: mac, date,
        class, etc.).

        Args:
            payload (Dict[str, str]):
                Dados estruturados do evento de detecção.

            evidence_path (Path):
                Caminho absoluto para o arquivo de imagem da evidência.

        Returns:
            bool:
                True caso o envio seja bem-sucedido,
                False em caso de falha.
        """
        if not evidence_path.exists():
            logger.error(
                "Arquivo de evidência não encontrado para envio",
                extra={"path": str(evidence_path)},
            )
            return False

        try:
            with evidence_path.open("rb") as image_file:
                files = {
                    "evidence": image_file,
                }

                response: Response = requests.post(
                    url=self.api_url,
                    data=payload,
                    files=files,
                    timeout=self.timeout,
                )

            if response.status_code in (200, 201):
                logger.info(
                    "Evento enviado com sucesso para a API",
                    extra={
                        "api_url": self.api_url,
                        "status_code": response.status_code,
                    },
                )
                return True

            logger.warning(
                "Falha ao enviar evento para a API",
                extra={
                    "api_url": self.api_url,
                    "status_code": response.status_code,
                    "response": response.text,
                },
            )
            return False

        except RequestException as exc:
            logger.error(
                "Erro de comunicação com a API de eventos",
                extra={
                    "api_url": self.api_url,
                    "error": str(exc),
                },
            )
            return False