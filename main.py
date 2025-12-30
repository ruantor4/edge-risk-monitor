"""
main.py

Edge Risk Monitor:
- Webcam
- Detector YOLO
- Bounding box
- Debounce temporal (anti-piscada)
- Envio de evento (edge → API)
"""

from pathlib import Path
import logging
import time
from datetime import datetime

import cv2

from detector.detector import Detector
from webcam.webcam import Webcam
from sender.sender import EventSender
from utils.logging_global import log_system
from utils.system import get_mac_address


# ==============================
# CONFIGURAÇÕES
# ==============================
DETECT_FRAMES_REQUIRED = 3
CLEAR_FRAMES_REQUIRED = 5

EVIDENCE_DIR = Path("evidence/detections")
API_URL = "http://localhost:8001/api/events/"  # mock ou API real


def main() -> None:
    Path("logs").mkdir(exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    log_system(
        logging.INFO,
        "Iniciando edge-risk-monitor (inferência em tempo real)",
    )

    # ==============================
    # INICIALIZAÇÕES
    # ==============================
    webcam = Webcam(index=0, width=640, height=480)
    if not webcam.open():
        log_system(logging.ERROR, "Falha ao inicializar webcam")
        return

    detector = Detector(
        model_path=Path("models/yolo_mouse.pt"),
        target_class="mouse",
        confidence_threshold=0.4,
    )

    sender = EventSender(api_url=API_URL)
    mac_address = get_mac_address()

    # ==============================
    # ESTADO DO SISTEMA
    # ==============================
    detect_counter = 0
    clear_counter = 0

    risk_active = False
    event_sent = False

    last_bbox = None
    last_label = ""

    try:
        while True:
            frame = webcam.read()
            if frame is None:
                continue

            result = detector.detect(frame)

            # ==============================
            # LÓGICA DE DETECÇÃO + DEBOUNCE
            # ==============================
            if result.get("detected"):
                detect_counter += 1
                clear_counter = 0

                last_bbox = result["bbox"]
                last_label = (
                    f"RISCO: {result['class_name']} "
                    f"({result['confidence']:.2f})"
                )

                if detect_counter >= DETECT_FRAMES_REQUIRED:
                    if not risk_active:
                        log_system(
                            logging.INFO,
                            "Risco confirmado após debounce",
                            context={
                                "detect_counter": detect_counter,
                                "confidence": result["confidence"],
                            },
                        )
                    risk_active = True

            else:
                clear_counter += 1
                detect_counter = 0

                if clear_counter >= CLEAR_FRAMES_REQUIRED:
                    if risk_active:
                        log_system(logging.INFO, "Risco limpo")
                    risk_active = False
                    event_sent = False
                    last_bbox = None
                    last_label = ""

            # ==============================
            # ENVIO DO EVENTO (UMA VEZ)
            # ==============================
            if risk_active and not event_sent:
                log_system(logging.INFO, "Disparo de evento de risco")

                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                evidence_path = (
                    EVIDENCE_DIR / f"risk_{int(time.time())}.jpg"
                )

                cv2.imwrite(str(evidence_path), frame)

                payload = {
                    "mac": mac_address,
                    "date": timestamp,
                    "class": result["class_name"],
                }

                success = sender.send_event(
                    payload=payload,
                    evidence_path=evidence_path,
                )

                if success:
                    log_system(logging.INFO, "Evento enviado com sucesso")
                    event_sent = True
                else:
                    log_system(logging.ERROR, "Falha ao enviar evento")

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
