import plotly.graph_objects as go

# =====================================================
# LAYOUT PADRÃO
# =====================================================

def _layout(fig, titulo, yaxis=""):

    fig.update_layout(

        title={
            "text": titulo,
            "x": 0.02,
            "font": {
                "size": 20
            }
        },

        template="plotly_dark",

        height=380,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        hovermode="x unified",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        legend=dict(
            orientation="h",
            y=1.05,
            x=0
        )

    )

    fig.update_xaxes(

        showgrid=False,

        showline=True,

        linewidth=1

    )

    fig.update_yaxes(

        title=yaxis,

        showgrid=True,

        gridcolor="rgba(255,255,255,0.12)",

        zeroline=False

    )

    return fig


# =====================================================
# MEMÓRIA
# =====================================================

def grafico_memoria(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["timestamp"],

            y=df["memory_mb"],

            mode="lines",

            name="RAM",

            line=dict(
                width=3,
                shape="spline"
            ),

            fill="tozeroy"

        )

    )

    return _layout(
        fig,
        "🧠 Uso de Memória",
        "MB"
    )


# =====================================================
# CPU
# =====================================================

def grafico_cpu(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["timestamp"],

            y=df["cpu"],

            mode="lines",

            name="CPU",

            line=dict(
                width=3,
                shape="spline"
            ),

            fill="tozeroy"

        )

    )

    return _layout(
        fig,
        "⚙ Uso de CPU"
    )


# =====================================================
# DOWNLOAD
# =====================================================

def grafico_download(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["timestamp"],

            y=df["download_mb"],

            mode="lines",

            name="Download",

            line=dict(
                width=3,
                shape="spline"
            ),

            fill="tozeroy"

        )

    )

    return _layout(
        fig,
        "📥 Tráfego de Download",
        "MB"
    )


# =====================================================
# UPLOAD
# =====================================================

def grafico_upload(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["timestamp"],

            y=df["upload_mb"],

            mode="lines",

            name="Upload",

            line=dict(
                width=3,
                shape="spline"
            ),

            fill="tozeroy"

        )

    )

    return _layout(
        fig,
        "📤 Tráfego de Upload",
        "MB"
    )