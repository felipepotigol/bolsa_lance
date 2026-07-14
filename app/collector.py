import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from config import (
    METRICS_FILE,
    PROMETHEUS_URL,
    UPDATE_TIME,
)

# =====================================================
# PREPARAÇÃO
# =====================================================

Path(METRICS_FILE).parent.mkdir(
    parents=True,
    exist_ok=True
)

if not Path(METRICS_FILE).exists():

    df = pd.DataFrame(columns=[
        "timestamp",
        "memory",
        "cpu",
        "network_receive",
        "network_transmit"
    ])

    df.to_csv(
        METRICS_FILE,
        index=False
    )

# =====================================================
# CONSULTA AO PROMETHEUS
# =====================================================

def consultar(query: str) -> float:
    try:

        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query},
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        resultado = data["data"]["result"]

        if len(resultado) == 0:
            return 0.0

        return float(resultado[0]["value"][1])

    except Exception as erro:

        print(f"Erro Prometheus: {erro}")

        return 0.0


# =====================================================
# CONSULTAS
# =====================================================

MEMORY_QUERY = "avg(container_memory_usage_bytes)"

CPU_QUERY = "avg(rate(container_cpu_usage_seconds_total[1m]))"

NETWORK_RECEIVE_QUERY = (
    "sum(container_network_receive_bytes_total)"
)

NETWORK_TRANSMIT_QUERY = (
    "sum(container_network_transmit_bytes_total)"
)

# =====================================================
# LOOP PRINCIPAL
# =====================================================

print("=" * 70)
print("        FEDERATED MONITORING - COLLECTOR")
print("=" * 70)
print(f"Arquivo........: {METRICS_FILE}")
print(f"Prometheus.....: {PROMETHEUS_URL}")
print(f"Intervalo......: {UPDATE_TIME} segundos")
print("Pressione CTRL+C para encerrar.")
print("=" * 70)

coleta = 0

try:

    while True:

        memoria = consultar(MEMORY_QUERY)

        cpu = consultar(CPU_QUERY)

        download = consultar(
            NETWORK_RECEIVE_QUERY
        )

        upload = consultar(
            NETWORK_TRANSMIT_QUERY
        )

        horario = datetime.now()

        linha = pd.DataFrame([{

            "timestamp":
                horario.strftime("%Y-%m-%d %H:%M:%S"),

            "memory":
                memoria,

            "cpu":
                cpu,

            "network_receive":
                download,

            "network_transmit":
                upload

        }])

        linha.to_csv(
            METRICS_FILE,
            mode="a",
            header=False,
            index=False
        )

        print(
            f"[{coleta:05}] "
            f"{horario.strftime('%H:%M:%S')} | "
            f"RAM: {memoria/1024/1024:8.2f} MB | "
            f"CPU: {cpu:10.6f} | "
            f"DOWN: {download/1024/1024:10.2f} MB | "
            f"UP: {upload/1024/1024:10.2f} MB"
        )

        coleta += 1

        # Resumo a cada 10 coletas
        if coleta % 10 == 0:

            print("\n" + "=" * 70)

            print("RESUMO DA COLETA")

            print(f"Coletas realizadas : {coleta}")

            print(f"Última atualização : {horario.strftime('%d/%m/%Y %H:%M:%S')}")

            print(f"Arquivo            : {METRICS_FILE}")

            print("=" * 70 + "\n")

        time.sleep(UPDATE_TIME)

except KeyboardInterrupt:

    print()

    print("=" * 70)

    print("Coleta encerrada pelo usuário.")

    print(f"Total de coletas realizadas: {coleta}")

    print("=" * 70)