from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from config import (
    METRICS_FILE,
    MODELS_DIR,
    PREDICTIONS_FILE,
)

# =====================================================
# PREPARAÇÃO
# =====================================================

MODELS_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# CARREGA DADOS
# =====================================================

if not METRICS_FILE.exists():
    print("Arquivo de métricas não encontrado.")
    exit()

df = pd.read_csv(METRICS_FILE)

metricas = [
    "memory",
    "cpu",
    "network_receive",
    "network_transmit",
]

# verifica colunas

for coluna in metricas:
    if coluna not in df.columns:
        print(f"Coluna '{coluna}' não encontrada.")
        exit()

# remove linhas inválidas

df = df.dropna()

if len(df) < 10:
    print("Poucos dados para treinamento.")
    exit()

# =====================================================
# TREINAMENTO
# =====================================================

X = np.arange(len(df)).reshape(-1, 1)
proximo = np.array([[len(df)]])

previsoes = {}

print("=" * 60)
print("TREINAMENTO DOS MODELOS")
print("=" * 60)

for coluna in metricas:

    modelo = LinearRegression()

    y = df[coluna].values

    modelo.fit(X, y)

    previsao = float(modelo.predict(proximo)[0])

    previsoes[coluna] = previsao

    joblib.dump(
        modelo,
        MODELS_DIR / f"{coluna}.joblib"
    )

    print(f"\nMétrica: {coluna}")
    print(f"Coeficiente : {modelo.coef_[0]:.6f}")
    print(f"Intercepto  : {modelo.intercept_:.6f}")
    print(f"Próximo valor previsto : {previsao:.6f}")

# =====================================================
# SALVA PREVISÕES
# =====================================================

resultado = pd.DataFrame([{

    "timestamp": pd.Timestamp.now(),

    "memory": previsoes["memory"],

    "cpu": previsoes["cpu"],

    "network_receive": previsoes["network_receive"],

    "network_transmit": previsoes["network_transmit"]

}])

resultado.to_csv(
    PREDICTIONS_FILE,
    index=False
)

print("\nModelos atualizados com sucesso.")
print(f"Previsões: {PREDICTIONS_FILE}")
print(f"Modelos : {MODELS_DIR}")
print("=" * 60)