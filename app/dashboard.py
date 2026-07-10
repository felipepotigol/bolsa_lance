import streamlit as st

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

from utils.status import get_status

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

# =====================================================
# DADOS
# =====================================================

df = load_metrics()

if df.empty:
    st.warning("Nenhuma métrica encontrada.")
    st.stop()

ultima = latest_metrics()

pred = latest_predictions()

stats = statistics()

status = get_status()

# =====================================================
# STATUS
# =====================================================

st.subheader("Status do Sistema")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if status["Prometheus"]:
        st.success("🟢 Prometheus")
    else:
        st.error("🔴 Prometheus")

with c2:
    if status["Metrics"]:
        st.success("🟢 Metrics")
    else:
        st.error("🔴 Metrics")

with c3:
    if status["Models"]:
        st.success("🟢 Modelos")
    else:
        st.error("🔴 Modelos")

with c4:
    if status["Predictions"]:
        st.success("🟢 Predictor")
    else:
        st.error("🔴 Predictor")

st.divider()

# =====================================================
# MÉTRICAS
# =====================================================

st.subheader("Métricas Atuais")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "🧠 Memória",
    f"{ultima['memory_mb']:.2f} MB"
)

m2.metric(
    "⚙ CPU",
    f"{ultima['cpu']:.6f}"
)

m3.metric(
    "📥 Download",
    f"{ultima['download_mb']:.2f} MB"
)

m4.metric(
    "📤 Upload",
    f"{ultima['upload_mb']:.2f} MB"
)

# =====================================================
# PREVISÕES
# =====================================================

if pred is not None:

    st.divider()

    st.subheader("Previsões da IA")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "Memória Prevista",
        f"{pred['memory']/1024/1024:.2f} MB"
    )

    p2.metric(
        "CPU Prevista",
        f"{pred['cpu']:.6f}"
    )

    p3.metric(
        "Download Previsto",
        f"{pred['network_receive']/1024/1024:.2f} MB"
    )

    p4.metric(
        "Upload Previsto",
        f"{pred['network_transmit']/1024/1024:.2f} MB"
    )

# =====================================================
# GRÁFICOS
# =====================================================

st.divider()

st.subheader("Monitoramento")

g1, g2 = st.columns(2)

with g1:
    st.plotly_chart(
        grafico_memoria(df),
        use_container_width=True,
        key="ram"
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

st.subheader("Estatísticas")

e1, e2 = st.columns(2)

with e1:

    st.write("### Memória")

    st.write(f"**Média:** {stats['memory_mean']:.2f} MB")

    st.write(f"**Máxima:** {stats['memory_max']:.2f} MB")

    st.write(f"**Mínima:** {stats['memory_min']:.2f} MB")

with e2:

    st.write("### CPU")

    st.write(f"**Média:** {stats['cpu_mean']:.6f}")

    st.write(f"**Máxima:** {stats['cpu_max']:.6f}")

    st.write(f"**Mínima:** {stats['cpu_min']:.6f}")

# =====================================================
# TABELA
# =====================================================

st.divider()

with st.expander("Últimas coletas"):

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )