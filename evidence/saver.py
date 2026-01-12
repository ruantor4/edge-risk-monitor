"""
evidence/saver.py

Responsável pelo salvamento de evidências visuais
geradas pelo projeto edge-risk-monitor.

Este módulo encapsula exclusivamente a lógica de persistência
de frames de imagem no sistema de arquivos, atuando como
componente de apoio à inferência e análise de risco.

Não realiza inferência, controle de estado ou integração
com APIs externas. Seu escopo é estritamente o armazenamento
de evidências visuais.

Escopo:
- Validação do diretório de saída de evidências
- Persistência de frames como arquivos de imagem
- Geração de nomes de arquivos baseados em timestamp
- Registro de logs de sucesso e falha no salvamento
"""
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)

class EvidenceSaver:
    """
    Inicializa o gerenciador de salvamento de evidências.

    Args:
        output_dir (Path):
            Diretório onde as evidências visuais serão armazenadas.

        logger (logging.Logger, optional):
            Logger utilizado para registro de eventos do módulo.

    Raises:
        FileNotFoundError:
            Caso o diretório de saída de evidências não exista.
    """

    def __init__(
        self,
        output_dir: Path) -> None:
        """
        Inicializa o gerenciador de evidências.

        Args:
            output_dir (Path): Diretório onde as evidências serão salvas.
            logger (logging.Logger, optional): Logger do módulo.

        Raises:
            FileNotFoundError: Caso o diretório de saída não exista.
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, frame) -> Path:
        """
        Persiste um frame como evidência visual no sistema de arquivos.

        O arquivo é salvo utilizando um nome baseado em timestamp,
        garantindo unicidade e rastreabilidade temporal.

        Args:
            frame:
                Frame capturado pela câmera no formato OpenCV (BGR).

        Returns:
            Path:
                Caminho absoluto do arquivo de evidência salvo.

        Raises:
            IOError:
                Caso a evidência não possa ser salva no disco.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"evidence_{timestamp}.jpg"
        file_path = (self.output_dir / filename)

        if not cv2.imwrite(str(file_path), frame):
            logger.error(
                "Falha ao salvar evidência visual",
                extra={"path": str(file_path)},
            )
            raise IOError(f"Erro ao salvar evidência em {file_path}")

        logger.info(
            "Evidência visual salva com sucesso",
            extra={"path": str(file_path)},
        )

        return file_path