from typing import Optional
import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class Webcam:
    """
    Abstração da webcam utilizando OpenCV.

    Esta classe encapsula o ciclo de vida do dispositivo de captura,
    incluindo abertura, leitura de frames e liberação de recursos,
    fornecendo uma interface controlada para o sistema.
    """

    def __init__(self, index: int = 0, width: int = 640, height: int = 480) -> None:
        """
        Inicializa a abstração da webcam.

        Parameters
        ----------
        index : int
            Índice do dispositivo de vídeo utilizado.
        width : int
            Largura do frame capturado.
        height : int
            Altura do frame capturado.
        """
        self.index = index
        self.width = width
        self.height = height
        self._cap: Optional[cv2.VideoCapture] = None

    def open(self) -> bool:
        """
        Abre e configura o dispositivo de captura de vídeo.

        Returns
        -------
        bool
            True se a webcam foi inicializada com sucesso,
            False caso contrário.
        """
        try:
            self._cap = cv2.VideoCapture(self.index)

            if not self._cap.isOpened():
                logger.error(
                    "Falha ao abrir webcam",
                    extra={"index": self.index},
                )
                return False

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            logger.info(
                "Webcam inicializada",
                extra={
                    "index": self.index,
                    "width": self.width,
                    "height": self.height,
                }
            )
            return True

        except Exception as exc:
            logger.error(
                "Exceção ao inicializar webcam",
                extra={"error": str(exc)},
            )
            return False

    def read(self) -> Optional[np.ndarray]:
        """
        Captura um frame da webcam.

        Returns
        -------
        Optional[np.ndarray]
            Frame no formato BGR (OpenCV) ou None em caso de falha.
        """
        try:
            if self._cap is None or not self._cap.isOpened():
                logger.warning("Webcam não inicializada")
                return None

            ret, frame = self._cap.read()
            if not ret:
                logger.warning("Falha ao capturar frame")
                return None

            return frame

        except Exception as exc:
            logger.info(
                "Exceção durante captura de frame",
                extra = {"error": str(exc)},
            )
            return None

    def release(self) -> None:
        """
        Libera os recursos associados ao dispositivo de captura.
        """
        try:
            if self._cap is not None:
                self._cap.release()
                logger.info("Webcam liberada")
        
        except Exception as exc:
            logger.error(
                "Exceção ao liberar webcam",
                extra = {"error": str(exc)},
            )
