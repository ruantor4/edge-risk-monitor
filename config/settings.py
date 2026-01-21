"""
settings.py

Arquivo de configuração central do projeto Edge Risk Monitor.

Este arquivo define:
- Configurações globais da aplicação
- Parâmetros de captura da câmera
- Configurações do modelo de detecção
- Regras de decisão e debounce de risco
- Filtros geométricos de bounding box
- Persistência visual de detecções
- Diretórios de saída de artefatos
- Integração com API externa de monitoramento
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

# PATHS DO PROJETO

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parents[1]


# CONFIGURAÇÕES DA APLICAÇÃO

# Nome identificador da aplicação
# Nome identificador da aplicação
APP_NAME = "edge-risk-monitor"

# Diretório de logs da aplicação
LOGS_DIR = BASE_DIR / "logs"

# ============================================================
# CONFIGURAÇÕES DE CÂMERA
# ============================================================

# CONFIGURAÇÕES DE CÂMERA

# Índice do dispositivo de câmera utilizado
CAMERA_INDEX = 0

# Resolução dos frames capturados

# Resolução dos frames capturados
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# CONFIGURAÇÕES DO DETECTOR

# Caminho para o modelo de detecção utilizado na inferência
MODEL_PATH = BASE_DIR / "models" / "yolo_mouse.pt"

# Classe alvo monitorada pelo sistema
TARGET_CLASS = "mouse"

# Limiar mínimo de confiança para considerar uma detecção válida
CONFIDENCE_THRESHOLD = 0.50

# CONTROLE DE DEBOUNCE DE DETECÇÃO (LEGADO / DESATIVADO)

# Número mínimo de frames consecutivos com detecção válida
# para confirmação do estado de risco
# DETECT_FRAMES_REQUIRED = 6

# Número mínimo de frames consecutivos sem detecção
# para limpeza do estado de risco
# CLEAR_FRAMES_REQUIRED = 8


# CONTROLE AVANÇADO DE DECISÃO DE RISCO (ANTI-FALSO POSITIVO)

# Tamanho da janela deslizante de confiança (frames)
CONFIDENCE_WINDOW_SIZE = 6

# Média mínima de confiança para confirmar risco
RISK_CONFIRM_MEAN_THRESHOLD = 0.55

# Média máxima de confiança para limpar risco
RISK_CLEAR_MEAN_THRESHOLD = 0.30


# CONTROLE DE PERSISTÊNCIA VISUAL (OVERLAY)

# Quantidade de frames que o bounding box permanece visível
# após a última detecção válida
VISUAL_HOLD_FRAMES = 5


# FILTROS GEOMÉTRICOS DE BOUNDING BOX (ANTI-FALSO POSITIVO)

# Área máxima permitida da bounding box (normalizada 0–1)
MAX_BOX_AREA = 0.30

# Largura máxima permitida da bounding box (normalizada)
MAX_BOX_WIDTH = 0.60

# Altura máxima permitida da bounding box (normalizada)
MAX_BOX_HEIGHT = 0.60

# Proporção mínima e máxima (width / height)
MIN_BOX_PROPORTION = 0.30
MAX_BOX_PROPORTION = 3.00


# OUTPUTS E ARTEFATOS GERADOS

# Diretório base para armazenamento de artefatos de detecção
OUTPUT_DIR = BASE_DIR / "outputs" / "detection"


# CONFIGURAÇÕES DE INTEGRAÇÃO COM API EXTERNA

# URL base da API de monitoramento
API_BASE_URL = "http://127.0.0.1:8000"

# Credenciais de autenticação da API
API_USERNAME = "root"
API_PASSWORD = "root"

# Endpoint de envio de eventos de monitoramento
API_MONITORING_ENDPOINT = f"{API_BASE_URL}/api/monitoring/"