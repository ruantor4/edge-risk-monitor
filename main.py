"""
main.py

Ponto de entrada oficial do pipeline de monitoramento
do projeto edge-risk-monitor.

Responsabilidades:
- Orquestrar a execução do monitoramento em tempo real
- Inicializar o sistema de logging
- Inicializar componentes centrais do sistema
- Executar inferência, decisão de risco e envio de eventos
  de forma determinística

Este módulo NÃO implementa regras de detecção, filtros,
persistência ou envio. Ele apenas orquestra componentes
já validados.
"""

Ponto de entrada oficial do pipeline de monitoramento
do projeto edge-risk-monitor.

Responsabilidades:
- Orquestrar a execução do monitoramento em tempo real
- Inicializar o sistema de logging
- Inicializar componentes centrais do sistema
- Executar inferência, decisão de risco e envio de eventos
  de forma determinística

Este módulo NÃO implementa regras de detecção, filtros,
persistência ou envio. Ele apenas orquestra componentes
já validados.
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from pathlib import Path

import cv2

from config.settings import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MODEL_PATH,
    TARGET_CLASS,
    CONFIDENCE_THRESHOLD,
    CONFIDENCE_WINDOW_SIZE,
    RISK_CONFIRM_MEAN_THRESHOLD,
    RISK_CLEAR_MEAN_THRESHOLD,
    VISUAL_HOLD_FRAMES,
    CONFIDENCE_WINDOW_SIZE,
    RISK_CONFIRM_MEAN_THRESHOLD,
    RISK_CLEAR_MEAN_THRESHOLD,
    VISUAL_HOLD_FRAMES,
    OUTPUT_DIR,
    API_BASE_URL,
    API_USERNAME,
    API_PASSWORD,
)

from utils.system import get_mac_address
from utils.logging_global import setup_logging
from webcam.webcam import Webcam
from detector.detector import Detector
from evidence.saver import EvidenceSaver
from sender.sender import EventSender

# >>> INTEGRAÇÃO API
from utils.auth import authenticate

setup_logging()
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Executa o pipeline oficial de monitoramento de risco.
    """

    # ====================================================
    # ETAPA 1 – PREPARAÇÃO DO AMBIENTE E INICIALIZAÇÃO
    # ====================================================
    logger.info("Iniciando pipeline oficial de monitoramento de risco")
    
    try:
        webcam = Webcam(
            index=CAMERA_INDEX,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
        )
        
        if not webcam.open():
            logger.error("Falha ao inicializar webcam")
            return
    """
    Executa o pipeline oficial de monitoramento de risco.
    """

    # ====================================================
    # ETAPA 1 – PREPARAÇÃO DO AMBIENTE E INICIALIZAÇÃO
    # ====================================================
    logger.info("Iniciando pipeline oficial de monitoramento de risco")
    
    try:
        webcam = Webcam(
            index=CAMERA_INDEX,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
        )
        
        if not webcam.open():
            logger.error("Falha ao inicializar webcam")
            return

        detector = Detector(
            model_path=MODEL_PATH,
            target_class=TARGET_CLASS,
            confidence_threshold=CONFIDENCE_THRESHOLD,
        )
        detector = Detector(
            model_path=MODEL_PATH,
            target_class=TARGET_CLASS,
            confidence_threshold=CONFIDENCE_THRESHOLD,
        )

        evidence_saver = EvidenceSaver(output_dir=OUTPUT_DIR)
        
        # Integração com API
        access_token = authenticate(
            api_base_url=API_BASE_URL,
            username=API_USERNAME,
            password=API_PASSWORD,
        )
        
        monitoring_endpoint = f"{API_BASE_URL}/api/monitoring/"
        
        event_sender = EventSender(
            api_url=monitoring_endpoint,
            access_token=access_token,
        )

        mac_address = get_mac_address()
        mac_address = get_mac_address()

        logger.info("Componentes inicializados com sucesso")

        # ====================================================
        # ETAPA 2 – ESTADO DO SISTEMA
        # ====================================================

        confidence_window: list[float] = []
        logger.info("Componentes inicializados com sucesso")

        # ====================================================
        # ETAPA 2 – ESTADO DO SISTEMA
        # ====================================================

        confidence_window: list[float] = []

        risk_active = False
        event_sent = False
        risk_active = False
        event_sent = False

        last_bbox = None
        last_label = ""
        visual_hold_counter = 0

        # ====================================================
        # ETAPA 3 – LOOP PRINCIPAL
        # ====================================================

        logger.info("Iniciando loop principal de inferência")

        last_bbox = None
        last_label = ""
        visual_hold_counter = 0

        # ====================================================
        # ETAPA 3 – LOOP PRINCIPAL
        # ====================================================

        logger.info("Iniciando loop principal de inferência")

        while True:
            frame = webcam.read()
            if frame is None:
                continue

            detection = detector.detect(frame)
            detection = detector.detect(frame)

            # ====================================================
            # CONTROLE VISUAL
            # ====================================================

            if detection.get("detected"):
                last_bbox = detection["bbox"]
            # ====================================================
            # CONTROLE VISUAL
            # ====================================================

            if detection.get("detected"):
                last_bbox = detection["bbox"]
                last_label = (
                    f"OBJETO DE RISCO: {detection['class_name']} "
                    f"({detection['confidence']:.2f})"
                    f"OBJETO DE RISCO: {detection['class_name']} "
                    f"({detection['confidence']:.2f})"
                )
                visual_hold_counter = VISUAL_HOLD_FRAMES
                visual_hold_counter = VISUAL_HOLD_FRAMES
            else:
                if visual_hold_counter > 0:
                    visual_hold_counter -= 1
                else:
                if visual_hold_counter > 0:
                    visual_hold_counter -= 1
                else:
                    last_bbox = None
                    last_label = ""

            # ====================================================
            # DECISÃO DE RISCO (MÉDIA)
            # ====================================================

            confidence = (
                detection["confidence"]
                if detection.get("detected")
                else 0.0
            )

            confidence_window.append(confidence)
            if len(confidence_window) > CONFIDENCE_WINDOW_SIZE:
                confidence_window.pop(0)

            mean_confidence = sum(confidence_window) / len(confidence_window)

            if mean_confidence >= RISK_CONFIRM_MEAN_THRESHOLD:
                if not risk_active:
                    logger.info(
                        "Risco confirmado por média de confiança",
                        extra={"mean_confidence": mean_confidence},
                    )
                risk_active = True

            elif mean_confidence <= RISK_CLEAR_MEAN_THRESHOLD:
                if risk_active:
                    logger.info(
                        "Risco limpo por queda da confiança média",
                        extra={"mean_confidence": mean_confidence},
                    )
                risk_active = False
                event_sent = False

            # ====================================================
            # ENVIO DE EVENTO
            # ====================================================
            # ====================================================
            # DECISÃO DE RISCO (MÉDIA)
            # ====================================================

            confidence = (
                detection["confidence"]
                if detection.get("detected")
                else 0.0
            )

            confidence_window.append(confidence)
            if len(confidence_window) > CONFIDENCE_WINDOW_SIZE:
                confidence_window.pop(0)

            mean_confidence = sum(confidence_window) / len(confidence_window)

            if mean_confidence >= RISK_CONFIRM_MEAN_THRESHOLD:
                if not risk_active:
                    logger.info(
                        "Risco confirmado por média de confiança",
                        extra={"mean_confidence": mean_confidence},
                    )
                risk_active = True

            elif mean_confidence <= RISK_CLEAR_MEAN_THRESHOLD:
                if risk_active:
                    logger.info(
                        "Risco limpo por queda da confiança média",
                        extra={"mean_confidence": mean_confidence},
                    )
                risk_active = False
                event_sent = False

            # ====================================================
            # ENVIO DE EVENTO
            # ====================================================

            if risk_active and not event_sent:
                logger.info("Disparo de evento de risco")
                logger.info("Disparo de evento de risco")

                timestamp = datetime.now().isoformat()
                evidence_path = evidence_saver.save(frame)

                payload = {
                    "mac_address": mac_address,
                    "detected_class": detection.get("class_name", ""),
                    "detected_at": timestamp,
                }

                success = event_sender.send_event(
                success = event_sender.send_event(
                    payload=payload,
                    evidence_path=evidence_path,
                )

                if success:
                    logger.info("Evento enviado com sucesso")
                    logger.info("Evento enviado com sucesso")
                    event_sent = True
                else:
                    logger.error("Falha ao enviar evento")
                    logger.error("Falha ao enviar evento")

            # ====================================================
            # OVERLAY
            # ====================================================
            # ====================================================
            # OVERLAY
            # ====================================================

            if last_bbox:
            if last_bbox:
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
                    "OBJETO DE RISCO",
                    "OBJETO DE RISCO",
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

    except Exception as exc:
        logger.error(
            "Falha na execução do pipeline de monitoramento",
            extra={"error": str(exc)},
        )
        raise

    except Exception as exc:
        logger.error(
            "Falha na execução do pipeline de monitoramento",
            extra={"error": str(exc)},
        )
        raise

    finally:
        try:
            webcam.release()
            cv2.destroyAllWindows()
        
        except Exception:
            pass

        logger.info("Pipeline oficial de monitoramento finalizado")
        try:
            webcam.release()
            cv2.destroyAllWindows()
        
        except Exception:
            pass

        logger.info("Pipeline oficial de monitoramento finalizado")


if __name__ == "__main__":
    main()
