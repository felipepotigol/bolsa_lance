import flwr as fl
import logging
import json
import os
import time
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO
# ==========================================

HOST = "0.0.0.0"
PORT = "8081"

NUM_ROUNDS = 10

STATUS_FILE = "data/flower_status.json"

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# ==========================================
# ESTRATÉGIA FEDERADA
# ==========================================

strategy = fl.server.strategy.FedAvg(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=1,
    min_evaluate_clients=1,
    min_available_clients=1
)

# ==========================================
# STATUS
# ==========================================

status = {
    "running": True,
    "strategy": "FedAvg",
    "round": 0,
    "clients": 0,
    "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "last_update": "",
    "training_time": 0
}

with open(STATUS_FILE, "w", encoding="utf-8") as f:
    json.dump(status, f, indent=4)

print("=" * 60)
print("FLOWER SERVER")
print("=" * 60)
print(f"Endereço : {HOST}:{PORT}")
print(f"Rounds   : {NUM_ROUNDS}")
print("=" * 60)

inicio = time.time()

# ==========================================
# EXECUÇÃO
# ==========================================

try:

    fl.server.start_server(
        server_address=f"{HOST}:{PORT}",
        config=fl.server.ServerConfig(
            num_rounds=NUM_ROUNDS
        ),
        strategy=strategy
    )

except KeyboardInterrupt:

    print("\nServidor encerrado.")

finally:

    status["running"] = False
    status["training_time"] = round(
        time.time() - inicio,
        2
    )
    status["last_update"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)

    print("=" * 60)
    print("Treinamento finalizado.")
    print("=" * 60)