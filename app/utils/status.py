from pathlib import Path
import json
import requests

from config import (
    PROMETHEUS_HOST,
    PROMETHEUS_PORT,
    METRICS_FILE,
    PREDICTIONS_FILE,
    MODELS_DIR,
    FLOWER_STATUS_FILE,
)

# =====================================================
# STATUS GERAL
# =====================================================

def get_status():

    status = {}

    # Prometheus
    try:

        response = requests.get(
            f"http://{PROMETHEUS_HOST}:{PROMETHEUS_PORT}",
            timeout=2
        )

        status["Prometheus"] = (
            response.status_code == 200
        )

    except Exception:

        status["Prometheus"] = False

    # Arquivo de métricas

    status["Metrics"] = (
        Path(METRICS_FILE).exists()
    )

    # Modelos treinados

    modelos = [

        MODELS_DIR / "memory.joblib",

        MODELS_DIR / "cpu.joblib",

        MODELS_DIR / "network_receive.joblib",

        MODELS_DIR / "network_transmit.joblib"

    ]

    status["Models"] = all(
        arquivo.exists()
        for arquivo in modelos
    )

    # Previsões

    status["Predictions"] = (
        Path(PREDICTIONS_FILE).exists()
    )

    return status


# =====================================================
# STATUS FLOWER
# =====================================================

def get_flower_status():

    if Path(FLOWER_STATUS_FILE).exists():

        try:

            with open(
                FLOWER_STATUS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                dados = json.load(f)

            return {

                "running": dados.get(
                    "running",
                    False
                ),

                "strategy": dados.get(
                    "strategy",
                    "-"
                ),

                "round": dados.get(
                    "round",
                    0
                ),

                "clients": dados.get(
                    "clients",
                    0
                ),

                "started_at": dados.get(
                    "started_at",
                    "-"
                ),

                "last_update": dados.get(
                    "last_update",
                    "-"
                ),

                "training_time": dados.get(
                    "training_time",
                    0
                )

            }

        except Exception:

            pass

    return {

        "running": False,

        "strategy": "-",

        "round": 0,

        "clients": 0,

        "started_at": "-",

        "last_update": "-",

        "training_time": 0

    }