from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

METRICS_FILE = DATA_DIR / "metrics.csv"
PREDICTIONS_FILE = DATA_DIR / "predictions.csv"


def load_metrics():

    if not METRICS_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(METRICS_FILE)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["memory_mb"] = df["memory"] / 1024 / 1024

    df["download_mb"] = df["network_receive"] / 1024 / 1024

    df["upload_mb"] = df["network_transmit"] / 1024 / 1024

    return df


def load_predictions():

    if not PREDICTIONS_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(PREDICTIONS_FILE)


def latest_metrics():

    df = load_metrics()

    if df.empty:
        return None

    return df.iloc[-1]


def latest_predictions():

    df = load_predictions()

    if df.empty:
        return None

    return df.iloc[-1]


def statistics():

    df = load_metrics()

    if df.empty:
        return {}

    return {

        "memory_mean": df["memory_mb"].mean(),
        "memory_max": df["memory_mb"].max(),
        "memory_min": df["memory_mb"].min(),

        "cpu_mean": df["cpu"].mean(),
        "cpu_max": df["cpu"].max(),
        "cpu_min": df["cpu"].min(),

        "download_mean": df["download_mb"].mean(),
        "upload_mean": df["upload_mb"].mean()

    }