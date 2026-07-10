import flwr as fl
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression

# ==========================================
# CONFIGURAÇÕES
# ==========================================

DATA_FILE = Path("data") / "metrics.csv"
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(exist_ok=True)

TARGETS = [
    "memory",
    "cpu",
    "network_receive",
    "network_transmit"
]

# ==========================================
# LEITURA DOS DADOS
# ==========================================

df = pd.read_csv(DATA_FILE)

if len(df) < 10:
    raise Exception("Poucos dados para treinamento.")

X = np.arange(len(df)).reshape(-1, 1)

models = {}

for coluna in TARGETS:

    y = df[coluna].values

    model = LinearRegression()
    model.fit(X, y)

    models[coluna] = model

    print(f"\nModelo treinado: {coluna}")
    print("Coef:", model.coef_[0])
    print("Intercepto:", model.intercept_)

# ==========================================
# CLIENTE FLOWER
# ==========================================

class FederatedClient(fl.client.NumPyClient):

    def get_parameters(self, config):

        parametros = []

        for coluna in TARGETS:

            model = models[coluna]

            parametros.append(model.coef_)
            parametros.append(np.array([model.intercept_]))

        return parametros

    def fit(self, parameters, config):

        print("\nRecebendo parâmetros do servidor...")

        indice = 0

        for coluna in TARGETS:

            model = models[coluna]

            model.coef_ = parameters[indice]
            model.intercept_ = parameters[indice + 1][0]

            indice += 2

            model.fit(X, df[coluna].values)

            joblib.dump(
                model,
                MODEL_DIR / f"{coluna}.joblib"
            )

            print(f"Modelo atualizado: {coluna}")

        parametros = []

        for coluna in TARGETS:

            model = models[coluna]

            parametros.append(model.coef_)
            parametros.append(np.array([model.intercept_]))

        return parametros, len(X), {}

    def evaluate(self, parameters, config):

        mse_total = []

        for coluna in TARGETS:

            pred = models[coluna].predict(X)

            mse = np.mean(
                (pred - df[coluna].values) ** 2
            )

            mse_total.append(mse)

        loss = float(np.mean(mse_total))

        print(f"Loss médio: {loss}")

        return loss, len(X), {}

# ==========================================
# EXECUÇÃO
# ==========================================

print("=" * 60)
print("CLIENTE FLOWER")
print("=" * 60)

fl.client.start_numpy_client(
    server_address="127.0.0.1:8081",
    client=FederatedClient()
)