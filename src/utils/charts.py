import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Paleta (mesma ideia do projeto base)
COLORS = {
    "blue": "#1f4e79",
    "green": "#2ca02c",
    "red": "#d62728",
    "yellow": "#ffbf00",
    "light_green": "#90ee90",
    "gray_line": "DarkSlateGrey",
}

def format_number(value, fmt="%0.0f"):
    """Formatação brasileira (milhar '.' e decimal ',')."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "-"
    s = fmt % value
    # se tiver decimal, troca separadores
    if "." in s:
        # primeiro troca milhar padrão (,) se existir
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    return s.replace(",", ".")

def _base_layout(fig, title, xaxis=None, yaxis=None, height=340, showlegend=True):
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=showlegend,
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    if xaxis:
        fig.update_xaxes(title=xaxis)
    if yaxis:
        fig.update_yaxes(title=yaxis)
    return fig

def plot_bar(df, col, title, xaxis="Categoria", top_n=15, orientation="h", color=None):
    """Bar chart de contagem (categorias)."""
    if col not in df.columns:
        return go.Figure()

    s = df[col].dropna()

    # se numérico com muita granularidade, agrupa em bins (melhor leitura)
    if pd.api.types.is_numeric_dtype(s) and s.nunique() > 25:
        s = pd.cut(s, bins=10)

    vc = s.value_counts().head(top_n)

    if orientation == "h":
        fig = go.Figure(go.Bar(
            x=vc.values,
            y=vc.index.astype(str),
            orientation="h",
            text=[format_number(v, "%0.0f") for v in vc.values],
            textposition="auto",
            marker=dict(color=color or COLORS["blue"]),
        ))
        fig = _base_layout(fig, title, xaxis="Quantidade", yaxis=xaxis, height=360, showlegend=False)
        fig.update_traces(marker=dict(line=dict(width=0.5, color=COLORS["gray_line"])))
        fig.update_yaxes(autorange="reversed")
    else:
        fig = go.Figure(go.Bar(
            x=vc.index.astype(str),
            y=vc.values,
            text=[format_number(v, "%0.0f") for v in vc.values],
            textposition="auto",
            marker=dict(color=color or COLORS["blue"]),
        ))
        fig = _base_layout(fig, title, xaxis=xaxis, yaxis="Quantidade", height=360, showlegend=False)
        fig.update_traces(marker=dict(line=dict(width=0.5, color=COLORS["gray_line"])))
    return fig

def plot_histograma(df, col, title, nbins=20, color=None, percent=False):
    """Histograma (opção de percentual)."""
    if col not in df.columns:
        return go.Figure()

    s = pd.to_numeric(df[col], errors="coerce").dropna()
    if s.empty:
        return go.Figure()

    fig = px.histogram(
        x=s,
        nbins=nbins,
        histnorm="percent" if percent else None,
        color_discrete_sequence=[color or COLORS["light_green"]],
    )
    yaxis = "Percentual (%)" if percent else "Quantidade"
    fig = _base_layout(fig, title, xaxis=col, yaxis=yaxis, height=340, showlegend=False)
    fig.update_traces(marker_line_width=0.5, marker_line_color=COLORS["gray_line"])
    return fig

def plot_scatter(df, x, y, title, color_col=None, color_map=None, height=360):
    if x not in df.columns or y not in df.columns:
        return go.Figure()

    d = df.copy()
    d[x] = pd.to_numeric(d[x], errors="coerce")
    d[y] = pd.to_numeric(d[y], errors="coerce")
    d = d.dropna(subset=[x, y])

    if color_col and color_col in d.columns:
        fig = px.scatter(
            d, x=x, y=y, color=color_col,
            color_discrete_map=color_map,
            opacity=0.75
        )
        fig = _base_layout(fig, title, xaxis=x, yaxis=y, height=height, showlegend=True)
    else:
        fig = px.scatter(d, x=x, y=y, opacity=0.75, color_discrete_sequence=[COLORS["blue"]])
        fig = _base_layout(fig, title, xaxis=x, yaxis=y, height=height, showlegend=False)

    return fig

def plot_line(series, title, xaxis="Ano", yaxis="Percentual", height=320, color=None):
    s = series.dropna()
    fig = go.Figure(go.Scatter(
        x=s.index.astype(str),
        y=s.values,
        mode="lines+markers",
        line=dict(color=color or COLORS["blue"], width=3)
    ))
    fig = _base_layout(fig, title, xaxis=xaxis, yaxis=yaxis, height=height, showlegend=False)
    return fig

def plot_gauge_percent(value_0_1, title):
    v = 0 if value_0_1 is None or np.isnan(value_0_1) else float(value_0_1)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=v * 100,
        number={"suffix": "%", "valueformat": ".1f"},
        title={"text": title},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS["red"]},
            "steps": [
                {"range": [0, 30], "color": COLORS["green"]},
                {"range": [30, 60], "color": COLORS["yellow"]},
                {"range": [60, 100], "color": COLORS["red"]},
            ],
        },
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig
