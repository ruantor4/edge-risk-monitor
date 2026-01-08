"""
settings.py

Arquivo de configuração central do projeto edge-risk-monitor.

Este módulo atua como a fonte única de verdade (single source of truth)
para parâmetros globais, configurações de captura, inferência,
controle de estado e integração externa do monitoramento de risco.

Responsabilidades:
- Centralizar configurações globais da aplicação
- Definir parâmetros de captura da câmera
- Declarar configurações do modelo de detecção
- Controlar regras de debounce de detecção
- Definir diretórios de saída de artefatos
- Centralizar configurações de integração com API externa
"""
from pathlib import Path


# ============================================================
# APLICAÇÃO
# ============================================================

# Nome identificador da aplicação
APP_NAME = "edge-risk-monitor"


# ============================================================
# CONFIGURAÇÕES DE CÂMERA
# ============================================================

# Índice do dispositivo de câmera utilizado
CAMERA_INDEX = 0

# Resolução dos frames capturados
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ============================================================
# CONFIGURAÇÕES DO DETECTOR
# ============================================================

# Caminho para o modelo de detecção utilizado na inferência
MODEL_PATH = Path("models/yolo_mouse.pt")

# Classe alvo monitorada pelo sistema
TARGET_CLASS = "mouse"

# Limiar mínimo de confiança para considerar uma detecção válida
CONFIDENCE_THRESHOLD = 0.4

# ============================================================
# CONTROLE DE DEBOUNCE DE DETECÇÃO
# ============================================================

# Número mínimo de frames consecutivos com detecção válida
# para confirmação do estado de risco
DETECT_FRAMES_REQUIRED = 3

# Número mínimo de frames consecutivos sem detecção
# para limpeza do estado de risco
CLEAR_FRAMES_REQUIRED = 5

# ============================================================
# OUTPUTS E ARTEFATOS GERADOS
# ============================================================

# Diretório base para armazenamento de artefatos de detecção
OUTPUT_DIR = Path("outputs/detection")

# ============================================================
# INTEGRAÇÃO COM API EXTERNA
# ============================================================

API_URL = "http://localhost:8001/api/events/"