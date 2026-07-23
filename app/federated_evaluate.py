from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from config import (
    METRICS_FILE,
    MODELS_DIR,
)

# ============================================
# PASTA DOS RESULTADOS
# ============================================

RESULTS_DIR = Path("models") / "federated"
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ============================================
# CARREGA DADOS
# ============================================

df = pd.read_csv(METRICS_FILE)

if len(df) < 2:
    raise Exception("Poucos dados para avaliação.")

X = np.arange(len(df)).reshape(-1, 1)

TARGETS = [

    "memory",

    "cpu",

    "network_receive",

    "network_transmit"

]

results = {}

print("=" * 60)
print("AVALIAÇÃO DO MODELO FEDERADO")
print("=" * 60)

# ============================================
# AVALIAÇÃO
# ============================================

for target in TARGETS:

    model_file = MODELS_DIR / f"{target}.joblib"

    if not model_file.exists():
        print(f"Modelo não encontrado: {model_file}")
        continue

    model = joblib.load(model_file)

    y = df[target].values

    pred = model.predict(X)

    mae = mean_absolute_error(
        y,
        pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y,
            pred
        )
    )

    r2 = r2_score(
        y,
        pred
    )

    results[target] = {

        "mae": float(mae),

        "rmse": float(rmse),

        "r2": float(r2)

    }

    print()
    print("=" * 60)
    print(target.upper())
    print("=" * 60)
    print(f"MAE  : {mae}")
    print(f"RMSE : {rmse}")
    print(f"R²   : {r2}")

# ============================================
# SALVA RESULTADOS
# ============================================

arquivo = RESULTS_DIR / "results.json"

with open(
    arquivo,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

print()
print("=" * 60)
print("Resultados salvos em:")
print(arquivo)
print("=" * 60)