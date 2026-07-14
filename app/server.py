import json
import logging
import time
from datetime import datetime
from pathlib import Path

import flwr as fl

from config import (
    SERVER_ADDRESS,
)

# =====================================================
# CONFIGURAÇÕES
# =====================================================

NUM_ROUNDS = 10

DATA_DIR = Path("data")

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

STATUS_FILE = DATA_DIR / "flower_status.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# =====================================================
# ESTRATÉGIA FEDERADA
# =====================================================

strategy = fl.server.strategy.FedAvg(

    fraction_fit=1.0,

    fraction_evaluate=1.0,

    min_fit_clients=1,

    min_evaluate_clients=1,

    min_available_clients=1

)

# =====================================================
# STATUS
# =====================================================

status = {

    "running": True,

    "strategy": "FedAvg",

    "rounds": NUM_ROUNDS,

    "started_at":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

    "finished_at": None,

    "training_time": 0

}

with open(

    STATUS_FILE,

    "w",

    encoding="utf-8"

) as arquivo:

    json.dump(

        status,

        arquivo,

        indent=4

    )

# =====================================================
# INFORMAÇÕES
# =====================================================

print("=" * 70)
print("FLOWER SERVER")
print("=" * 70)
print(f"Servidor : {SERVER_ADDRESS}")
print(f"Rounds   : {NUM_ROUNDS}")
print("=" * 70)

inicio = time.time()

# =====================================================
# EXECUÇÃO
# =====================================================

try:

    fl.server.start_server(

        server_address=SERVER_ADDRESS,

        config=fl.server.ServerConfig(

            num_rounds=NUM_ROUNDS

        ),

        strategy=strategy

    )

except KeyboardInterrupt:

    print()

    print("Servidor interrompido pelo usuário.")

finally:

    tempo = round(

        time.time() - inicio,

        2

    )

    status["running"] = False

    status["training_time"] = tempo

    status["finished_at"] = datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )

    with open(

        STATUS_FILE,

        "w",

        encoding="utf-8"

    ) as arquivo:

        json.dump(

            status,

            arquivo,

            indent=4

        )

    print()

    print("=" * 70)
    print("TREINAMENTO FINALIZADO")
    print("=" * 70)
    print(f"Tempo total : {tempo} segundos")
    print(f"Status salvo em : {STATUS_FILE}")
    print("=" * 70)