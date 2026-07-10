from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

PROMETHEUS_URL = "http://localhost:9090/-/healthy"


# ==========================================
# PROMETHEUS
# ==========================================

def prometheus_online():

    try:
        requests.get(PROMETHEUS_URL, timeout=2)
        return True
    except:
        return False


# ==========================================
# MODELOS TREINADOS
# ==========================================

def modelos_treinados():

    modelos = [
        "memory.joblib",
        "cpu.joblib",
        "network_receive.joblib",
        "network_transmit.joblib"
    ]

    for modelo in modelos:

        if not (MODEL_DIR / modelo).exists():
            return False

    return True


# ==========================================
# PREDICTIONS
# ==========================================

def predictions_ok():

    arquivo = DATA_DIR / "predictions.csv"

    return arquivo.exists()


# ==========================================
# METRICS
# ==========================================

def metrics_ok():

    arquivo = DATA_DIR / "metrics.csv"

    return arquivo.exists()


# ==========================================
# STATUS GERAL
# ==========================================

def get_status():

    return {

        "Prometheus": prometheus_online(),

        "Metrics": metrics_ok(),

        "Predictions": predictions_ok(),

        "Models": modelos_treinados()

    }