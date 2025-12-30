"""
main.py

Edge Risk Monitor:
- Captura de webcam
- Inferência YOLO
- Debounce temporal
- Geração de evidências
- Envio de eventos via API
"""

from pathlib import Path
import logging
import time
from datetime import datetime

import cv2

from config.settings import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MODEL_PATH,
    TARGET_CLASS,
    CONFIDENCE_THRESHOLD,
    DETECT_FRAMES_REQUIRED,
    CLEAR_FRAMES_REQUIRED,
    OUTPUT_DIR,
    API_URL,
)

from detector.detector import Detector
from webcam.webcam import Webcam
from sender.sender import EventSender
from evidence.saver import EvidenceSaver
from utils.logging_global import log_system
from utils.system import get_mac_address


def main() -> None:
   
    # PREPARAÇÃO DE AMBIENTE

    Path("logs").mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log_system(
        logging.INFO,
        "Iniciando edge-risk-monitor (inferência em tempo real)",
    )

  
    # INICIALIZAÇÕES

    webcam = Webcam(
        index=CAMERA_INDEX,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
    )

    if not webcam.open():
        log_system(logging.ERROR, "Falha ao inicializar webcam")
        return

    detector = Detector(
        model_path=MODEL_PATH,
        target_class=TARGET_CLASS,
        confidence_threshold=CONFIDENCE_THRESHOLD,
    )

    sender = EventSender(api_url=API_URL)
    saver = EvidenceSaver(output_dir=OUTPUT_DIR)

    mac_address = get_mac_address()

  
    # ESTADO DO SISTEMA
   
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

     
            # DETECÇÃO + DEBOUNCE
   
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


            # ENVIO DO EVENTO

            if risk_active and not event_sent:
                log_system(logging.INFO, "Disparo de evento de risco")

                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                evidence_path = saver.save(frame)

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


            # OVERLAY VISUAL

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
