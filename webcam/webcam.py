"""
webcam.py

Módulo responsável exclusivamente pela captura de frames da webcam
no projeto edge-risk-monitor.

Este módulo implementa a camada de aquisição de vídeo do sistema,
abstraindo o acesso ao dispositivo físico de captura (webcam)
por meio da biblioteca OpenCV.

Não realiza inferência, análise de risco, persistência ou envio
de eventos. Seu escopo é estritamente a aquisição de frames.

Escopo:
- Inicialização do dispositivo de captura de vídeo
- Captura de frames em tempo real
- Configuração de resolução da webcam
- Liberação controlada dos recursos do dispositivo
"""

from typing import Optional
import logging

import cv2
import numpy as np

from utils.logging_global import log_system


class Webcam:
    """
    Abstração da webcam utilizando OpenCV.

    Esta classe encapsula o ciclo de vida do dispositivo de captura,
    incluindo abertura, leitura de frames e liberação de recursos,
    fornecendo uma interface simples e controlada para o restante
    do sistema.
    """

    def __init__(self, index: int = 0, width: int = 640, height: int = 480) -> None:
        """
        Inicializa a abstração da webcam.

        Args:
            index (int):
                Índice do dispositivo de vídeo utilizado.

            width (int):
                Largura do frame capturado.

            height (int):
                Altura do frame capturado.
        """
        self.index = index
        self.width = width
        self.height = height
        self._cap: Optional[cv2.VideoCapture] = None

    def open(self) -> bool:
        """
        Abre e configura o dispositivo de captura de vídeo.

        Inicializa a webcam, aplica as configurações de resolução
        e valida a disponibilidade do dispositivo.

        Returns:
            bool:
                True se a webcam foi inicializada com sucesso,
                False caso contrário.
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
                Frame no formato BGR (OpenCV) ou None em caso de falha
                ou indisponibilidade do dispositivo.
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
        Libera os recursos associados ao dispositivo de captura.

        Deve ser chamada durante o encerramento controlado
        da aplicação para garantir liberação adequada da webcam.
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
