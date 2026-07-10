from pathlib import Path

# ==========================================
# DIRETÓRIOS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MODELS_DIR = BASE_DIR / "models"

DOCKER_DIR = BASE_DIR / "docker"

# ==========================================
# ARQUIVOS
# ==========================================

METRICS_FILE = DATA_DIR / "metrics.csv"

PREDICTIONS_FILE = DATA_DIR / "predictions.csv"

# ==========================================
# PROMETHEUS
# ==========================================

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

# ==========================================
# FLOWER
# ==========================================

FLOWER_SERVER = "127.0.0.1:8081"

# ==========================================
# CONFIGURAÇÕES
# ==========================================

UPDATE_TIME = 10