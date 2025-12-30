"""
sender.py

Responsável por enviar eventos de detecção do edge-risk-monitor
para o backend risk-monitor-api (Django REST API).

Este módulo:
- Envia payload estruturado (JSON)
- Anexa evidência (imagem)
- Trata erros de comunicação
- Registra logs de sucesso e falha
"""

from pathlib import Path
from typing import Dict, Optional
import logging

import requests
from requests import Response, RequestException


class EventSender:
    """
    Cliente HTTP responsável por enviar eventos de detecção
    para o risk-monitor-api.
    """

    def __init__(
        self,
        api_url: str,
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Inicializa o sender.

        Args:
            api_url (str): URL do endpoint da API.
            timeout (int): Timeout da requisição HTTP em segundos.
            logger (logging.Logger, optional): Logger customizado.
        """
        self.api_url = api_url
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    def send_event(
        self,
        payload: Dict[str, str],
        evidence_path: Path,
    ) -> bool:
        """
        Envia um evento de detecção para o backend.

        Args:
            payload (Dict[str, str]): Dados do evento (mac, date, class).
            evidence_path (Path): Caminho da imagem de evidência.

        Returns:
            bool: True se o envio foi bem-sucedido, False caso contrário.
        """
        if not evidence_path.exists():
            self.logger.error(
                "Arquivo de evidência não encontrado: %s",
                evidence_path,
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
                self.logger.info(
                    "Evento enviado com sucesso para a API (%s)",
                    response.status_code,
                )
                return True

            self.logger.warning(
                "Falha ao enviar evento. Status: %s | Resposta: %s",
                response.status_code,
                response.text,
            )
            return False

        except RequestException as exc:
            self.logger.error(
                "Erro de comunicação com a API: %s",
                exc,
                exc_info=True,
            )
            return False