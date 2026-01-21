from typing import Dict, Any, Optional
from pathlib import Path
import logging

import numpy as np
from ultralytics import YOLO

from config.settings import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MAX_BOX_AREA,
    MAX_BOX_WIDTH,
    MAX_BOX_HEIGHT,
    MIN_BOX_PROPORTION,
    MAX_BOX_PROPORTION,
)

logger = logging.getLogger(__name__)


class Detector:
    """
    Executa inferência de objetos de risco utilizando um modelo YOLO.

    Esta classe encapsula exclusivamente a lógica de inferência,
    não sendo responsável por captura de vídeo, controle de estado,
    debounce ou envio de eventos.
    """

    def __init__(
        self,
        model_path: Path,
        target_class: str = "mouse",
        confidence_threshold: float = 0.5,
    ) -> None:
        """
        Inicializa o detector YOLO.

        Parameters
        ----------
        model_path : Path
            Caminho para o arquivo do modelo YOLO treinado.
        target_class : str
            Nome da classe alvo a ser monitorada.
        confidence_threshold : float
            Limiar mínimo de confiança para considerar
            uma detecção válida.
        """
        self.model_path = model_path
        self.target_class = target_class
        self.confidence_threshold = confidence_threshold
        self.model: Optional[YOLO] = None

        # Carrega o modelo no momento da inicialização
        self._load_model()

    def _load_model(self) -> None:
        """
        Carrega o modelo YOLO a partir do caminho informado.

        Raises
        ------
        FileNotFoundError
            Caso o arquivo do modelo não exista.
        Exception
            Propaga qualquer erro ocorrido durante o carregamento.
        """
        try:
            # Valida existência física do arquivo do modelo
            if not self.model_path.exists():
                logger.error(
                    "Arquivo de modelo YOLO não encontrado",
                    extra={"path": str(self.model_path)},
                )
                raise FileNotFoundError(self.model_path)

            # Inicializa o modelo YOLO
            self.model = YOLO(str(self.model_path))

            logger.info(
                "Modelo YOLO carregado com sucesso",
                extra={"model_path": str(self.model_path)},
            )

        except Exception as exc:
            logger.error(
                "Falha ao carregar modelo YOLO",
                extra={"error": str(exc)},
            )
            raise


    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Executa inferência em um frame e retorna a melhor detecção válida.

        Parameters
        ----------
        frame : np.ndarray
            Frame capturado da webcam no formato BGR (OpenCV).

        Returns
        -------
        Dict[str, Any]
            Dicionário contendo os dados da detecção ou
            {"detected": False} quando nenhuma detecção válida ocorre.
        """
        # Garante que o modelo foi corretamente inicializado
        if self.model is None:
            logger.error("Modelo YOLO não inicializado")
            return {"detected": False}

        # Armazena a melhor detecção válida do frame
        best_detection: Optional[Dict[str, Any]] = None
        best_confidence: float = 0.0

        try:
            # Executa inferência YOLO sobre o frame
            results = self.model(frame, imgsz=640, verbose=False)

            for result in results:
                boxes = result.boxes
                names = result.names
                
                # Frame sem bounding boxes
                if boxes is None:
                    continue

                for box in boxes:
                    # Score de confiança da detecção
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # Classe detectada
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = names.get(class_id, "unknown")

                    # Filtra apenas a classe de interesse
                    if class_name != self.target_class:
                        continue
                    
                    # Aplica limiar mínimo de confiança
                    if confidence < self.confidence_threshold:
                        continue
                    
                    # Coordenadas absolutas da bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()

                    # Dimensões da bounding box em pixels
                    box_width_px = x2 - x1
                    box_height_px = y2 - y1

                    # Normalização das dimensões (0–1)
                    box_width = box_width_px / FRAME_WIDTH
                    box_height = box_height_px / FRAME_HEIGHT
                    box_area = box_width * box_height

                    # filtro por área máxima.
                    if box_area > MAX_BOX_AREA:
                        continue

                    # Largura / altura máximas permitidas
                    if box_width > MAX_BOX_WIDTH or box_height > MAX_BOX_HEIGHT:
                        continue

                    # Filtro por proporção (aspect ratio)
                    proportion = (
                        box_width / box_height if box_height > 0 else 0.0
                    )
                    if (
                        proportion < MIN_BOX_PROPORTION
                        or proportion > MAX_BOX_PROPORTION
                    ):
                        continue
                    
                    # Seleciona a detecção com maior confiança válida        
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_detection = {
                            "detected": True,
                            "class_id": class_id,
                            "class_name": class_name,
                            "confidence": confidence,
                            "bbox": [x1, y1, x2, y2],
                        }
            
            # Retorna a melhor detecção encontrada no frame
            if best_detection:
                logger.info(
                    "Objeto de risco detectado",
                    extra={
                        "class_name": best_detection["class_name"],
                        "confidence": best_detection["confidence"],
                        "bbox": best_detection["bbox"],
                    },
                )
                return best_detection
            
            # Nenhuma detecção válida
            return {"detected": False}

        except Exception as exc:
            logger.error(
                "Erro durante inferência YOLO",
                extra={"error": str(exc)},
            )
            return {"detected": False}
