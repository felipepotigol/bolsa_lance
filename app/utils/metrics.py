from pathlib import Path

import pandas as pd

from config import (
    METRICS_FILE,
    PREDICTIONS_FILE,
)

# =====================================================
# MÉTRICAS
# =====================================================

def load_metrics():

    if not Path(METRICS_FILE).exists():
        return pd.DataFrame()

    try:

        df = pd.read_csv(METRICS_FILE)

        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        df["memory_mb"] = (
            df["memory"] / 1024 / 1024
        )

        df["download_mb"] = (
            df["network_receive"] / 1024 / 1024
        )

        df["upload_mb"] = (
            df["network_transmit"] / 1024 / 1024
        )

        return df

    except Exception:

        return pd.DataFrame()


# =====================================================
# PREVISÕES
# =====================================================

def load_predictions():

    if not Path(PREDICTIONS_FILE).exists():
        return pd.DataFrame()

    try:

        return pd.read_csv(PREDICTIONS_FILE)

    except Exception:

        return pd.DataFrame()


# =====================================================
# ÚLTIMA MÉTRICA
# =====================================================

def latest_metrics():

    df = load_metrics()

    if df.empty:
        return None

    return df.iloc[-1]


# =====================================================
# ÚLTIMA PREVISÃO
# =====================================================

def latest_predictions():

    df = load_predictions()

    if df.empty:
        return None

    return df.iloc[-1]


# =====================================================
# ESTATÍSTICAS
# =====================================================

def statistics():

    df = load_metrics()

    if df.empty:

        return {

            "memory_mean": 0,
            "memory_max": 0,
            "memory_min": 0,

            "cpu_mean": 0,
            "cpu_max": 0,
            "cpu_min": 0,

            "download_mean": 0,
            "download_max": 0,
            "download_min": 0,

            "upload_mean": 0,
            "upload_max": 0,
            "upload_min": 0

        }

    return {

        "memory_mean": df["memory_mb"].mean(),
        "memory_max": df["memory_mb"].max(),
        "memory_min": df["memory_mb"].min(),

        "cpu_mean": df["cpu"].mean(),
        "cpu_max": df["cpu"].max(),
        "cpu_min": df["cpu"].min(),

        "download_mean": df["download_mb"].mean(),
        "download_max": df["download_mb"].max(),
        "download_min": df["download_mb"].min(),

        "upload_mean": df["upload_mb"].mean(),
        "upload_max": df["upload_mb"].max(),
        "upload_min": df["upload_mb"].min()

    }