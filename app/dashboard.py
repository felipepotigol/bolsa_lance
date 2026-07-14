import streamlit as st

from config import DASHBOARD_REFRESH

from utils.metrics import (
    load_metrics,
    latest_metrics,
    latest_predictions,
    statistics
)

from utils.charts import (
    grafico_memoria,
    grafico_cpu,
    grafico_download,
    grafico_upload
)

from utils.status import (
    get_status,
    get_flower_status
)

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Federated Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Federated Monitoring Dashboard")

st.caption(
    "Projeto PIBIC • Monitoramento Inteligente com Aprendizagem Federativa"
)

st.divider()

# =====================================================
# CARREGAMENTO DOS DADOS
# =====================================================

df = load_metrics()

if df.empty:

    st.warning(
        "Nenhuma métrica encontrada."
    )

    st.stop()

ultima = latest_metrics()

pred = latest_predictions()

stats = statistics()

status = get_status()

flower = get_flower_status()

# =====================================================
# STATUS GERAL
# =====================================================

st.subheader("🖥️ Status do Sistema")

status_cards = [

    ("Prometheus",
     status["Prometheus"],
     "📡"),

    ("Coletor",
     status["Metrics"],
     "📥"),

    ("Modelos",
     status["Models"],
     "🧠"),

    ("Preditor",
     status["Predictions"],
     "📈")

]

colunas = st.columns(4)

for coluna, card in zip(colunas, status_cards):

    nome, ativo, icone = card

    with coluna:

        if ativo:

            st.success(
                f"{icone} {nome}"
            )

        else:

            st.error(
                f"{icone} {nome}"
            )

# =====================================================
# FLOWER
# =====================================================

st.divider()

st.subheader("🌐 Aprendizagem Federativa")

f1, f2, f3, f4 = st.columns(4)

with f1:

    if flower["running"]:

        st.success("🟢 Servidor Online")

    else:

        st.error("🔴 Servidor Offline")

with f2:

    st.metric(
        "Estratégia",
        flower["strategy"]
    )

with f3:

    st.metric(
        "Rodada",
        flower["round"]
    )

with f4:

    st.metric(
        "Clientes",
        flower["clients"]
    )

# =====================================================
# MÉTRICAS
# =====================================================

st.divider()

st.subheader("📊 Métricas Atuais")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(

        "🧠 Memória",

        f"{ultima['memory_mb']:.2f} MB"

    )

with m2:

    st.metric(

        "⚙ CPU",

        f"{ultima['cpu']:.6f}"

    )

with m3:

    st.metric(

        "📥 Download",

        f"{ultima['download_mb']:.2f} MB"

    )

with m4:

    st.metric(

        "📤 Upload",

        f"{ultima['upload_mb']:.2f} MB"

    )

# =====================================================
# PREVISÕES
# =====================================================

if pred is not None:

    st.divider()

    st.subheader("🤖 Previsões da Inteligência Artificial")

    p1, p2, p3, p4 = st.columns(4)

    with p1:

        st.metric(

            "Memória Prevista",

            f"{pred['memory']/1024/1024:.2f} MB"

        )

    with p2:

        st.metric(

            "CPU Prevista",

            f"{pred['cpu']:.6f}"

        )

    with p3:

        st.metric(

            "Download Previsto",

            f"{pred['network_receive']/1024/1024:.2f} MB"

        )

    with p4:

        st.metric(

            "Upload Previsto",

            f"{pred['network_transmit']/1024/1024:.2f} MB"

        )

st.divider()

st.subheader("📈 Monitoramento em Tempo Real")

# =====================================================
# GRÁFICOS
# =====================================================

g1, g2 = st.columns(2)

with g1:

    st.plotly_chart(

        grafico_memoria(df),

        use_container_width=True,

        key="memoria"

    )

with g2:

    st.plotly_chart(

        grafico_cpu(df),

        use_container_width=True,

        key="cpu"

    )

g3, g4 = st.columns(2)

with g3:

    st.plotly_chart(

        grafico_download(df),

        use_container_width=True,

        key="download"

    )

with g4:

    st.plotly_chart(

        grafico_upload(df),

        use_container_width=True,

        key="upload"

    )

# =====================================================
# ESTATÍSTICAS
# =====================================================

st.divider()

st.subheader("📊 Estatísticas")

e1, e2 = st.columns(2)

with e1:

    st.markdown("### 🧠 Memória")

    st.metric(
        "Média",
        f"{stats['memory_mean']:.2f} MB"
    )

    st.metric(
        "Máximo",
        f"{stats['memory_max']:.2f} MB"
    )

    st.metric(
        "Mínimo",
        f"{stats['memory_min']:.2f} MB"
    )

with e2:

    st.markdown("### ⚙ CPU")

    st.metric(
        "Média",
        f"{stats['cpu_mean']:.6f}"
    )

    st.metric(
        "Máximo",
        f"{stats['cpu_max']:.6f}"
    )

    st.metric(
        "Mínimo",
        f"{stats['cpu_min']:.6f}"
    )

# =====================================================
# INFORMAÇÕES FLOWER
# =====================================================

st.divider()

st.subheader("🌐 Informações do Treinamento Federado")

i1, i2 = st.columns(2)

with i1:

    st.write(f"**Estratégia:** {flower['strategy']}")

    st.write(f"**Rodada Atual:** {flower['round']}")

    st.write(f"**Clientes:** {flower['clients']}")

with i2:

    st.write(f"**Servidor Ativo:** {flower['running']}")

    st.write(f"**Iniciado em:** {flower['started_at']}")

    st.write(f"**Última Atualização:** {flower['last_update']}")

# =====================================================
# TABELA
# =====================================================

st.divider()

st.subheader("📝 Últimas Coletas")

st.dataframe(

    df.tail(30),

    use_container_width=True,

    hide_index=True

)

# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.caption(
    "Federated Monitoring Dashboard • PIBIC/UFRN • Docker • Prometheus • Grafana • Flower • Streamlit"
)