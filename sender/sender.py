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
from typing import Dict, Optional
import logging

import requests
from requests import Response, RequestException


class EventSender:
    """
    Cliente HTTP responsável por enviar eventos de detecção
    para o serviço backend risk-monitor-api.
    """

    def __init__( 
        self,
        api_url: str,
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Inicializa o componente de envio de eventos.

        Args:
            api_url (str):
                URL do endpoint da API responsável por receber os eventos.

            timeout (int):
                Timeout máximo da requisição HTTP em segundos.

            logger (logging.Logger, optional):
                Logger utilizado para registro de eventos do módulo.
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

        O envio consiste em um payload estruturado acompanhado
        de um arquivo de evidência visual anexado à requisição.

        Args:
            payload (Dict[str, str]):
                Dados estruturados do evento de detecção.

            evidence_path (Path):
                Caminho para o arquivo de imagem da evidência.

        Returns:
            bool:
                True caso o envio seja bem-sucedido,
                False em caso de falha.
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