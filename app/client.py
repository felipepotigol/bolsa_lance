import flwr as fl
import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.linear_model import LinearRegression

from config import (
    METRICS_FILE,
    MODELS_DIR,
    SERVER_ADDRESS,
)

# =====================================================
# VERIFICAÇÕES
# =====================================================

if not METRICS_FILE.exists():

    raise FileNotFoundError(
        f"Arquivo não encontrado:\n{METRICS_FILE}"
    )

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# LEITURA DOS DADOS
# =====================================================

df = pd.read_csv(METRICS_FILE)

df = df.dropna()

if len(df) < 10:

    raise Exception(
        "Poucos dados para treinamento."
    )

# =====================================================
# PREPARAÇÃO
# =====================================================

TARGETS = [

    "memory",

    "cpu",

    "network_receive",

    "network_transmit"

]

X = np.arange(
    len(df)
).reshape(-1, 1)

models = {}

# =====================================================
# TREINAMENTO LOCAL
# =====================================================

print("=" * 60)
print("TREINAMENTO LOCAL")
print("=" * 60)

for coluna in TARGETS:

    y = df[coluna].values

    modelo = LinearRegression()

    modelo.fit(
        X,
        y
    )

    models[coluna] = modelo

    joblib.dump(

        modelo,

        MODELS_DIR / f"{coluna}.joblib"

    )

    print()

    print(f"Modelo: {coluna}")

    print(f"Coeficiente : {modelo.coef_[0]}")

    print(f"Intercepto  : {modelo.intercept_}")

print()

print("=" * 60)
print("Modelos locais treinados.")
print("=" * 60)

# =====================================================
# CLIENTE FLOWER
# =====================================================


class FederatedClient(fl.client.NumPyClient):

    def get_parameters(self, config):

        parametros = []

        for coluna in TARGETS:

            modelo = models[coluna]

            parametros.append(
                modelo.coef_
            )

            parametros.append(
                np.array(
                    [modelo.intercept_]
                )
            )

        return parametros

    def fit(self, parameters, config):

        print()

        print("Recebendo parâmetros do servidor...")

        indice = 0

        for coluna in TARGETS:

            modelo = models[coluna]

            modelo.coef_ = parameters[indice]

            modelo.intercept_ = parameters[indice + 1][0]

            indice += 2

            modelo.fit(
                X,
                df[coluna].values
            )

            joblib.dump(

                modelo,

                MODELS_DIR / f"{coluna}.joblib"

            )

            print(f"Modelo atualizado: {coluna}")

        parametros = []

        for coluna in TARGETS:

            modelo = models[coluna]

            parametros.append(
                modelo.coef_
            )

            parametros.append(
                np.array(
                    [modelo.intercept_]
                )
            )

        return parametros, len(X), {}

    def evaluate(self, parameters, config):

        erros = []

        for coluna in TARGETS:

            pred = models[coluna].predict(X)

            mse = np.mean(

                (pred - df[coluna].values) ** 2

            )

            erros.append(mse)

        loss = float(

            np.mean(erros)

        )

        print()

        print(f"Loss médio: {loss}")

        return loss, len(X), {}


# =====================================================
# EXECUÇÃO
# =====================================================

print()

print("=" * 60)
print("CLIENTE FLOWER")
print("=" * 60)

fl.client.start_client(

    server_address=SERVER_ADDRESS,

    client=FederatedClient().to_client()

)