"""
webcam.py

Módulo responsável exclusivamente pela captura de frames da webcam.

Este módulo implementa a camada de aquisição de vídeo do sistema
edge-risk-monitor, abstraindo o acesso ao dispositivo físico de captura
(webcam) por meio da biblioteca OpenCV.

Responsabilidades:
- Inicializar o dispositivo de vídeo
- Capturar frames
- Liberar recursos da webcam
"""

from typing import Optional
import logging

import cv2
import numpy as np

from utils.logging_global import log_system


class Webcam:
    """
    Abstração da webcam utilizando OpenCV.

    Esta classe encapsula o ciclo de vida do dispositivo de captura:
    abertura, leitura de frames e liberação de recursos.
    """

    def __init__(self, index: int = 0, width: int = 640, height: int = 480) -> None:
        """
        Inicializa a webcam.

        Args:
            index (int):
                Índice do dispositivo de vídeo.
            width (int):
                Largura do frame.
            height (int):
                Altura do frame.
        """
        self.index = index
        self.width = width
        self.height = height
        self._cap: Optional[cv2.VideoCapture] = None

    def open(self) -> bool:
        """
        Abre e configura a webcam.

        Returns:
            bool:
                True se inicializada com sucesso, False caso contrário.
        """
        try:
            self._cap = cv2.VideoCapture(self.index)

            if not self._cap.isOpened():
                log_system(logging.ERROR, "Falha ao abrir webcam", index=self.index)
                return False

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            log_system(
                logging.INFO,
                "Webcam inicializada",
                index=self.index,
                width=self.width,
                height=self.height,
            )
            return True

        except Exception as exc:
            log_system(
                logging.ERROR,
                "Exceção ao inicializar webcam",
                error=str(exc),
            )
            return False

    def read(self) -> Optional[np.ndarray]:
        """
        Captura um frame da webcam.

        Returns:
            Optional[np.ndarray]:
                Frame BGR (OpenCV) ou None em caso de falha.
        """
        try:
            if self._cap is None or not self._cap.isOpened():
                log_system(logging.WARNING, "Webcam não inicializada")
                return None

            ret, frame = self._cap.read()
            if not ret:
                log_system(logging.WARNING, "Falha ao capturar frame")
                return None

            return frame

        except Exception as exc:
            log_system(
                logging.ERROR,
                "Exceção durante captura de frame",
                error=str(exc),
            )
            return None

    def release(self) -> None:
        """
        Libera o recurso da webcam.
        """
        try:
            if self._cap is not None:
                self._cap.release()
                log_system(logging.INFO, "Webcam liberada")
        except Exception as exc:
            log_system(
                logging.ERROR,
                "Exceção ao liberar webcam",
                error=str(exc),
            )
