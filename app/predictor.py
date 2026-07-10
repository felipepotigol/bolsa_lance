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

Path(MODELS_DIR).mkdir(
    parents=True,
    exist_ok=True
)

Path(PREDICTIONS_FILE).parent.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# CARREGA DADOS
# =====================================================

if not Path(METRICS_FILE).exists():

    print("Arquivo de métricas não encontrado.")
    exit()

df = pd.read_csv("data/metrics.csv")

if len(df) < 5:

    print("Poucos dados para treinamento.")
    exit()

# =====================================================
# PREPARA X
# =====================================================

X = np.arange(len(df)).reshape(-1, 1)

proximo = np.array([[len(df)]])

# =====================================================
# TREINAMENTO
# =====================================================

metricas = [

    "memory",

    "cpu",

    "network_receive",

    "network_transmit"

]

previsoes = {}

print("=" * 60)
print("TREINAMENTO DOS MODELOS")
print("=" * 60)

for metrica in metricas:

    modelo = LinearRegression()

    y = df[metrica].values

    modelo.fit(X, y)

    previsao = float(

        modelo.predict(proximo)[0]

    )

    previsoes[metrica] = previsao

    arquivo_modelo = MODELS_DIR / f"{metrica}.joblib"

    joblib.dump(

        modelo,

        arquivo_modelo

    )

    print(f"{metrica}")

    print(f"Coeficiente : {modelo.coef_[0]}")

    print(f"Intercepto  : {modelo.intercept_}")

    print(f"Próximo valor: {previsao}")

    print("-" * 60)

# =====================================================
# SALVA PREVISÕES
# =====================================================

resultado = pd.DataFrame([{

    "memory":

        previsoes["memory"],

    "cpu":

        previsoes["cpu"],

    "network_receive":

        previsoes["network_receive"],

    "network_transmit":

        previsoes["network_transmit"]

}])

resultado.to_csv(

    PREDICTIONS_FILE,

    index=False

)

print()

print("=" * 60)

print("Previsões salvas em:")

print(PREDICTIONS_FILE)

print()

print("Modelos salvos em:")

print(MODELS_DIR)

print("=" * 60)