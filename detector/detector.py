"""
detector.py

Módulo responsável exclusivamente pela detecção de objetos de risco
utilizando um modelo YOLO (Ultralytics) em inferência local.

Responsabilidades:
- Carregar o modelo YOLO treinado (.pt)
- Executar inferência sobre frames
- Filtrar classes de interesse
- Retornar resultado estruturado da detecção

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
        Inicializa o detector.

        Args:
            model_path (Path):
                Caminho para o arquivo de pesos do modelo YOLO (.pt).

            target_class (str):
                Nome da classe considerada objeto de risco.

            confidence_threshold (float):
                Threshold mínimo de confiança para considerar
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
        do objeto de risco.

        Args:
            frame (np.ndarray):
                Frame BGR capturado pela webcam.

        Returns:
            Dict[str, Any]:
                Resultado estruturado da detecção.
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
