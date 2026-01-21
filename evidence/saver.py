from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)

class EvidenceSaver:
    """
    Gerencia o salvamento de evidências visuais geradas pelo edge.

    Esta classe é responsável exclusivamente pela persistência
    de frames de imagem no sistema de arquivos, não realizando
    inferência, controle de estado ou integração externa.
    """

    def __init__(
        self,
        output_dir: Path) -> None:
        """
        Inicializa o gerenciador de evidências.

        Parameters
        ----------
        output_dir : Path
            Diretório onde as evidências visuais serão armazenadas.
        """
        self.output_dir = output_dir
        
        # Garante a existência do diretório de saída
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, frame) -> Path:
        """
        Persiste um frame como evidência visual no sistema de arquivos.

        O arquivo é salvo utilizando um nome baseado em timestamp,
        garantindo unicidade e rastreabilidade temporal.

        Parameters
        ----------
        frame
            Frame capturado pela câmera no formato OpenCV (BGR).

        Returns
        -------
        Path
            Caminho absoluto do arquivo de evidência salvo.

        Raises
        ------
        IOError
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