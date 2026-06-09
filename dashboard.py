import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import psutil
import time

st.set_page_config(layout="wide")

st.title("📊 Dashboard Híbrido - Federated Learning + Sistema")

# -------------------------
# Funções ML simuladas
# -------------------------
def gerar_ml(n=50):
    return pd.DataFrame({
        "round": np.arange(n),
        "loss": np.random.rand(n) * 2,
        "accuracy": np.random.rand(n)
    })

# -------------------------
# Funções do sistema real
# -------------------------
def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent

    net = psutil.net_io_counters()
    return cpu, ram, net.bytes_sent / 1e6, net.bytes_recv / 1e6

placeholder = st.empty()

while True:
    df = gerar_ml()

    cpu, ram, net_up, net_down = get_system_metrics()

    # ---------------- ML: Loss
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df["round"], y=df["loss"],
        mode="lines+markers", name="Loss"
    ))
    fig1.update_layout(title="📉 Loss (Treinamento)", xaxis_title="Round", yaxis_title="Loss")

    # ---------------- ML: Accuracy
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df["round"], y=df["accuracy"],
        mode="lines+markers", name="Accuracy"
    ))
    fig2.update_layout(title="📈 Accuracy (Modelo)", xaxis_title="Round", yaxis_title="Accuracy")

    # ---------------- CPU
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=["CPU"], y=[cpu], name="CPU"))
    fig3.update_layout(title="🖥️ Uso de CPU (%)", yaxis_range=[0, 100])

    # ---------------- RAM
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=["RAM"], y=[ram], name="RAM"))
    fig4.update_layout(title="🧠 Uso de RAM (%)", yaxis_range=[0, 100])

    # ---------------- Rede
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=["Upload", "Download"],
        y=[net_up, net_down],
        name="Rede (MB)"
    ))
    fig5.update_layout(title="🌐 Uso de Rede (MB acumulado)")

    with placeholder.container():

        col1, col2 = st.columns(2)
        col3, col4, col5 = st.columns(3)

        with col1:
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.plotly_chart(fig4, use_container_width=True)

        with col5:
            st.plotly_chart(fig5, use_container_width=True)

    time.sleep(2)