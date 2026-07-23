from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from config import METRICS_FILE


# ============================================
# PASTA DOS MODELOS CENTRALIZADOS
# ============================================

MODELS_DIR = Path("models/centralized")
MODELS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================
# CARREGA DADOS
# ============================================

df = pd.read_csv(METRICS_FILE)

if len(df) < 2:
    raise Exception("Poucos dados para treinamento.")


# ============================================
# VARIÁVEIS
# ============================================

targets = [
    "memory",
    "cpu",
    "network_receive",
    "network_transmit",
]


results = {}


# ============================================
# TREINAMENTO
# ============================================

for target in targets:

    X = df.index.values.reshape(-1, 1)

    y = df[target].values

    model = LinearRegression()

    model.fit(X, y)

    pred = model.predict(X)

    mae = mean_absolute_error(y, pred)

    rmse = mean_squared_error(y, pred) ** 0.5

    r2 = r2_score(y, pred)

    joblib.dump(
        model,
        MODELS_DIR / f"{target}.joblib"
    )

    results[target] = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }

    print("=" * 50)
    print(target.upper())
    print(f"Coeficiente : {model.coef_[0]}")
    print(f"Intercepto  : {model.intercept_}")
    print(f"MAE         : {mae}")
    print(f"RMSE        : {rmse}")
    print(f"R²          : {r2}")


# ============================================
# SALVA RESULTADOS
# ============================================

with open(
    MODELS_DIR / "results.json",
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        results,
        f,
        indent=4,
    )


print("\nModelo centralizado treinado com sucesso.")
