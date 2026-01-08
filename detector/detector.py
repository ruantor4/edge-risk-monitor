"""
detector.py

Responsável pela execução de inferência de objetos de risco
no projeto edge-risk-monitor.

Este módulo encapsula exclusivamente a lógica de inferência
utilizando um modelo YOLO (Ultralytics), operando sobre frames
capturados em tempo real.

Não realiza captura de vídeo, controle de estado, debounce
ou despacho de eventos. Seu escopo é estritamente a detecção.

Escopo:
- Carregamento seguro do modelo YOLO treinado (.pt)
- Execução de inferência sobre frames individuais
- Filtragem por classe alvo e limiar de confiança
- Retorno de resultado estruturado da detecção
"""

from typing import Dict, Any, Optional
from pathlib import Path
import logging

import numpy as np
from ultralytics import YOLO

from utils.logging_global import log_system


class Detector:
    """
    Classe responsável pela inferência de objetos de risco
    utilizando um modelo YOLO.
    """

    def __init__(
        self,
        model_path: Path,
        target_class: str = "mouse",
        confidence_threshold: float = 0.5,
    ) -> None:
        """
        Inicializa o detector de objetos de risco.

        Args:
            model_path (Path):
                Caminho para o arquivo de pesos do modelo YOLO (.pt).

            target_class (str):
                Nome da classe considerada como objeto de risco.

            confidence_threshold (float):
                Limiar mínimo de confiança para considerar
                uma detecção válida.
        """
        self.model_path = model_path
        self.target_class = target_class
        self.confidence_threshold = confidence_threshold
        self.model: Optional[YOLO] = None

        self._load_model()

    def _load_model(self) -> None:
        """
        Carrega o modelo YOLO a partir do arquivo de pesos.

        Realiza validação da existência do arquivo e inicializa
        o objeto de inferência do Ultralytics YOLO.

        Raises:
            FileNotFoundError: Caso o arquivo de modelo não exista.
            Exception: Em caso de falha na inicialização do modelo.
        """
        try:
            if not self.model_path.exists():
                log_system(
                    logging.ERROR,
                    "Arquivo de modelo YOLO não encontrado",
                    path=str(self.model_path),
                )
                raise FileNotFoundError(self.model_path)

            self.model = YOLO(str(self.model_path))

            log_system(
                logging.INFO,
                "Modelo YOLO carregado com sucesso",
                model_path=str(self.model_path),
            )

        except Exception as exc:
            log_system(
                logging.ERROR,
                "Falha ao carregar modelo YOLO",
                error=str(exc),
            )
            raise

    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Executa inferência em um frame e verifica a presença
        do objeto de risco configurado.

        Args:
            frame (np.ndarray):
                Frame BGR capturado pela câmera.

        Returns:
            Dict[str, Any]:
                Estrutura contendo o resultado da detecção.
                Quando positivo, inclui classe, confiança
                e bounding box no espaço do frame original.
        """
        if self.model is None:
            log_system(logging.ERROR, "Modelo YOLO não inicializado")
            return {"detected": False}

        try:
            # Inferência (mantém frame original)
            results = self.model(frame, imgsz=640, verbose=False)

            for result in results:
                boxes = result.boxes
                names = result.names

                if boxes is None:
                    continue

                for box in boxes:
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = names.get(class_id, "unknown")

                    if confidence < self.confidence_threshold:
                        continue

                    if class_name != self.target_class:
                        continue

                    # Bounding box JÁ no espaço do frame original
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()

                    log_system(
                        logging.INFO,
                        "Objeto de risco detectado",
                        class_name=class_name,
                        confidence=confidence,
                        bbox=[x1, y1, x2, y2],
                    )

                    return {
                        "detected": True,
                        "class_id": class_id,
                        "class_name": class_name,
                        "confidence": confidence,
                        "bbox": [x1, y1, x2, y2],
                    }

            return {"detected": False}

        except Exception as exc:
            log_system(
                logging.ERROR,
                "Erro durante inferência YOLO",
                error=str(exc),
            )
            return {"detected": False}
