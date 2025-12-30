"""
evidence/saver.py

Módulo responsável pelo salvamento de evidências visuais
geradas pelo edge-risk-monitor.
"""

from pathlib import Path
from typing import Optional
import logging
import time

import cv2


class EvidenceSaver:
    """
    Responsável por persistir frames de imagem como evidências
    no sistema de arquivos.
    """

    def __init__(
        self,
        output_dir: Path,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Inicializa o gerenciador de evidências.

        Args:
            output_dir (Path): Diretório onde as evidências serão salvas.
            logger (logging.Logger, optional): Logger do módulo.

        Raises:
            FileNotFoundError: Caso o diretório de saída não exista.
        """
        self.output_dir = output_dir
        self.logger = logger or logging.getLogger(__name__)

        if not self.output_dir.exists():
            raise FileNotFoundError(
                f"Diretório de evidência não encontrado: {self.output_dir}"
            )

    def save(self, frame) -> Path:
        """
        Salva um frame como evidência visual.

        Args:
            frame: Frame capturado pela webcam (OpenCV).

        Returns:
            Path: Caminho do arquivo salvo.

        Raises:
            IOError: Caso a evidência não possa ser salva.
        """
        filename = f"detection_{int(time.time())}.jpg"
        file_path = self.output_dir / filename

        if not cv2.imwrite(str(file_path), frame):
            self.logger.error(
                "Falha ao salvar evidência",
                extra={"path": str(file_path)},
            )
            raise IOError(f"Erro ao salvar evidência em {file_path}")

        self.logger.info(
            "Evidência salva com sucesso",
            extra={"path": str(file_path)},
        )

        return file_path
