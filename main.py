"""
main.py

Main de TESTE com:
- Webcam
- Detector YOLO
- Bounding box
- Debounce temporal (anti-piscada)
"""

from pathlib import Path
import logging
import time

import cv2

from detector.detector import Detector
from webcam.webcam import Webcam
from utils.logging_global import log_system


# ==============================
# CONFIGURAÇÃO DE DEBOUNCE
# ==============================
DETECT_FRAMES_REQUIRED = 3
CLEAR_FRAMES_REQUIRED = 5


def main() -> None:
    Path("logs").mkdir(exist_ok=True)

    log_system(
        logging.INFO,
        "Iniciando edge-risk-monitor (teste webcam + detector + debounce)",
    )

    webcam = Webcam(index=0, width=640, height=480)

    if not webcam.open():
        log_system(logging.ERROR, "Falha ao inicializar webcam")
        return

    detector = Detector(
        model_path=Path("models/yolo_mouse.pt"),
        target_class="mouse",
        confidence_threshold=0.4,
    )

    # ==============================
    # ESTADO DO DEBOUNCE
    # ==============================
    detect_counter = 0
    clear_counter = 0
    risk_active = False
    last_bbox = None
    last_label = ""

    try:
        while True:
            frame = webcam.read()
            if frame is None:
                continue

            result = detector.detect(frame)

            if result.get("detected"):
                # SEMPRE atualiza bbox e label
                last_bbox = result["bbox"]
                last_label = (
                    f"RISCO: {result['class_name']} "
                    f"({result['confidence']:.2f})"
                )

                detect_counter += 1
                clear_counter = 0

                if detect_counter >= DETECT_FRAMES_REQUIRED:
                    risk_active = True

            else:
                detect_counter = 0
                clear_counter += 1

                if clear_counter >= CLEAR_FRAMES_REQUIRED:
                    risk_active = False
                    last_bbox = None
                    last_label = ""

            # ==============================
            # OVERLAY VISUAL
            # ==============================
            if risk_active and last_bbox:
                x1, y1, x2, y2 = map(int, last_bbox)

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    last_label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

                cv2.putText(
                    frame,
                    "OBJETO DE RISCO DETECTADO",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("edge-risk-monitor", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(0.01)

    finally:
        webcam.release()
        cv2.destroyAllWindows()
        log_system(logging.INFO, "Aplicação finalizada")


if __name__ == "__main__":
    main()
