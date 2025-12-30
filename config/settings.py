"""
settings.py

Configurações centralizadas do edge-risk-monitor.
"""

from pathlib import Path


# APLICAÇÃO

APP_NAME = "edge-risk-monitor"



# CAMERA

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# DETECTOR

MODEL_PATH = Path("models/yolo_mouse.pt")
TARGET_CLASS = "mouse"
CONFIDENCE_THRESHOLD = 0.4



# DEBOUNCE

DETECT_FRAMES_REQUIRED = 3
CLEAR_FRAMES_REQUIRED = 5



# OUTPUTS

OUTPUT_DIR = Path("outputs/detection")



# API

API_URL = "http://localhost:8001/api/events/"