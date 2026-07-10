import plotly.graph_objects as go


def _layout(fig, titulo, yaxis=""):

    fig.update_layout(
        title=titulo,
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified",
        legend=dict(orientation="h")
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        title=yaxis,
        showgrid=True
    )

    return fig


# ==========================================
# MEMÓRIA
# ==========================================

def grafico_memoria(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["memory_mb"],
            mode="lines",
            name="RAM",
            line=dict(width=2)
        )
    )

    return _layout(fig, "🧠 Uso de Memória", "MB")


# ==========================================
# CPU
# ==========================================

def grafico_cpu(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["cpu"],
            mode="lines",
            name="CPU",
            line=dict(width=2)
        )
    )

    return _layout(fig, "⚙ Uso de CPU")


# ==========================================
# DOWNLOAD
# ==========================================

def grafico_download(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["download_mb"],
            mode="lines",
            name="Download",
            line=dict(width=2)
        )
    )

    return _layout(fig, "📥 Download", "MB")


# ==========================================
# UPLOAD
# ==========================================

def grafico_upload(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["upload_mb"],
            mode="lines",
            name="Upload",
            line=dict(width=2)
        )
    )

    return _layout(fig, "📤 Upload", "MB")