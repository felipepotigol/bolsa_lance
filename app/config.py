from pathlib import Path

# =====================================================
# DIRETÓRIOS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MODELS_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# ARQUIVOS
# =====================================================

METRICS_FILE = DATA_DIR / "metrics.csv"

PREDICTIONS_FILE = DATA_DIR / "predictions.csv"

FLOWER_STATUS_FILE = DATA_DIR / "flower_status.json"

# =====================================================
# PROMETHEUS
# =====================================================

PROMETHEUS_HOST = "localhost"

PROMETHEUS_PORT = 9090

PROMETHEUS_URL = (
    f"http://{PROMETHEUS_HOST}:{PROMETHEUS_PORT}/api/v1/query"
)

# =====================================================
# FLOWER
# =====================================================

# ==========================================
# FLOWER
# ==========================================

FLOWER_SERVER_HOST = "0.0.0.0"

FLOWER_CLIENT_HOST = "127.0.0.1"

FLOWER_PORT = 8081

SERVER_ADDRESS = f"{FLOWER_CLIENT_HOST}:{FLOWER_PORT}"
# =====================================================
# COLETA
# =====================================================

UPDATE_TIME = 5

REQUEST_TIMEOUT = 5

# =====================================================
# DASHBOARD
# =====================================================

DASHBOARD_REFRESH = 5

# =====================================================
# MODELOS
# =====================================================

TARGETS = [

    "memory",

    "cpu",

    "network_receive",

    "network_transmit"

]

# =====================================================
# PROMQL
# =====================================================

MEMORY_QUERY = (
    "avg(container_memory_usage_bytes)"
)

CPU_QUERY = (
    "avg(rate(container_cpu_usage_seconds_total[1m]))"
)

NETWORK_RECEIVE_QUERY = (
    "sum(container_network_receive_bytes_total)"
)

NETWORK_TRANSMIT_QUERY = (
    "sum(container_network_transmit_bytes_total)"
)