from pathlib import Path
import json

import pandas as pd

# =====================================================
# ARQUIVOS
# =====================================================

CENTRALIZED_FILE = (
    Path("models")
    / "centralized"
    / "results.json"
)

FEDERATED_FILE = (
    Path("models")
    / "federated"
    / "results.json"
)

OUTPUT_FILE = (
    Path("models")
    / "comparison.csv"
)

# =====================================================
# CARREGA RESULTADOS
# =====================================================

if not CENTRALIZED_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado:\n{CENTRALIZED_FILE}"
    )

if not FEDERATED_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado:\n{FEDERATED_FILE}"
    )

with open(
    CENTRALIZED_FILE,
    "r",
    encoding="utf-8"
) as f:

    centralized = json.load(f)

with open(
    FEDERATED_FILE,
    "r",
    encoding="utf-8"
) as f:

    federated = json.load(f)

# =====================================================
# COMPARAÇÃO
# =====================================================

linhas = []

print("=" * 80)
print("COMPARAÇÃO DOS MODELOS")
print("=" * 80)

for metrica in centralized.keys():

    c = centralized[metrica]
    f = federated[metrica]

    # Melhor MAE
    melhor_mae = (
        "Centralizado"
        if c["mae"] < f["mae"]
        else "Federado"
    )

    # Melhor RMSE
    melhor_rmse = (
        "Centralizado"
        if c["rmse"] < f["rmse"]
        else "Federado"
    )

    # Melhor R²
    melhor_r2 = (
        "Centralizado"
        if c["r2"] > f["r2"]
        else "Federado"
    )

    linhas.append({

        "Métrica": metrica,

        "MAE Centralizado":
            c["mae"],

        "MAE Federado":
            f["mae"],

        "Melhor MAE":
            melhor_mae,

        "RMSE Centralizado":
            c["rmse"],

        "RMSE Federado":
            f["rmse"],

        "Melhor RMSE":
            melhor_rmse,

        "R² Centralizado":
            c["r2"],

        "R² Federado":
            f["r2"],

        "Melhor R²":
            melhor_r2

    })

    print()

    print("-" * 80)

    print(metrica.upper())

    print("-" * 80)

    print(
        f"MAE  : "
        f"{c['mae']:.6f}"
        f"  |  "
        f"{f['mae']:.6f}"
        f"  -> {melhor_mae}"
    )

    print(
        f"RMSE : "
        f"{c['rmse']:.6f}"
        f"  |  "
        f"{f['rmse']:.6f}"
        f"  -> {melhor_rmse}"
    )

    print(
        f"R²   : "
        f"{c['r2']:.6f}"
        f"  |  "
        f"{f['r2']:.6f}"
        f"  -> {melhor_r2}"
    )

# =====================================================
# SALVA CSV
# =====================================================

resultado = pd.DataFrame(linhas)

resultado.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("=" * 80)
print("Comparação concluída.")
print(f"Arquivo salvo em: {OUTPUT_FILE}")
print("=" * 80)