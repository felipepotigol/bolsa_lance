import flwr as fl
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Carregar dados
df = pd.read_csv("metrics.csv")

X = np.array(range(len(df))).reshape(-1, 1)
y = df["memory"].values

# Criar modelo
model = LinearRegression()
model.fit(X, y)

print("\nPESOS INICIAIS DO MODELO")
print("Coeficiente:", model.coef_)
print("Intercepto:", model.intercept_)


class FederatedClient(fl.client.NumPyClient):

    def get_parameters(self, config):
        return [
            model.coef_,
            np.array([model.intercept_])
        ]

    def fit(self, parameters, config):

        print("\nPESOS RECEBIDOS DO SERVIDOR")
        print("Coeficiente:", parameters[0])
        print("Intercepto:", parameters[1])

        model.coef_ = parameters[0]
        model.intercept_ = parameters[1][0]

        model.fit(X, y)

        print("\nPESOS APÓS TREINAMENTO LOCAL")
        print("Coeficiente:", model.coef_)
        print("Intercepto:", model.intercept_)

        return (
            [
                model.coef_,
                np.array([model.intercept_])
            ],
            len(X),
            {}
        )

    def evaluate(self, parameters, config):

        prediction = model.predict(X)

        loss = np.mean((prediction - y) ** 2)

        return loss, len(X), {}


fl.client.start_numpy_client(
    server_address="127.0.0.1:8081",
    client=FederatedClient()
)