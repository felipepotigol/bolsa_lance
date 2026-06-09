import requests
import pandas as pd
import time
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def consultar(query):
    try:
        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query}
        )

        data = response.json()

        if len(data["data"]["result"]) > 0:
            return float(
                data["data"]["result"][0]["value"][1]
            )

        return 0

    except:
        return 0


dados = []

i = 0

while True:

    memoria = consultar(
        "container_memory_usage_bytes"
    )

    cpu = consultar(
        "rate(container_cpu_usage_seconds_total[1m])"
    )

    rede = consultar(
        "container_network_receive_bytes_total"
    )

    dados.append({
        "timestamp": datetime.now(),
        "memory": memoria,
        "cpu": cpu,
        "network": rede
    })

    print(
        f"Coleta {i} | "
        f"RAM={memoria:.0f} | "
        f"CPU={cpu:.6f} | "
        f"Rede={rede:.0f}"
    )

    pd.DataFrame(dados).to_csv(
        "metrics.csv",
        index=False
    )

    i += 1

    time.sleep(10)