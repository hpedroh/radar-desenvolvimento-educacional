import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

BASE_DIR = os.path.dirname(__file__)  # .../app/pages
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))  # raiz do projeto
SRC_PATH = os.path.join(ROOT_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from utils.charts import (
    format_number,
    plot_histograma,
    plot_bar,
    plot_scatter,
    plot_line,
    plot_gauge_percent,
    COLORS
)

# =========================
# Carregar base consolidada
# =========================
DATA_PATH = os.path.join(ROOT_DIR, "data", "base_consolidada.csv")

df = pd.read_csv(DATA_PATH)

# garantir numéricos
for c in ["IAN","IDA","IEG","IAA","IPS","IPP","IPV","DEFAS","INDE_ATUAL","IDADE","TEMPO_PM"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# =========================
# Cabeçalho
# =========================
st.title("📊 Dashboard Geral — Monitoramento Educacional")
st.caption("Visão executiva + análise exploratória (EDA) dos indicadores da Passos Mágicos.")

# =========================
# Filtros (todos no topo)
# =========================
st.subheader("🔎 Filtros", divider="blue")

# Inicialização de estado
if "ano" not in st.session_state:
    st.session_state.ano = sorted(df["ANO"].dropna().unique())[-1]

if "fase" not in st.session_state:
    st.session_state.fase = "Todas"

if "faixa" not in st.session_state:
    st.session_state.faixa = "Todas"

if "status" not in st.session_state:
    st.session_state.status = "Todos"

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.selectbox(
        "Ano",
        sorted(df["ANO"].dropna().unique()),
        key="ano"
    )

with col2:
    fases = sorted(df["FASE"].dropna().astype(str).unique())
    st.selectbox(
        "Fase",
        ["Todas"] + fases,
        key="fase"
    )

with col3:
    if "FAIXA_DEFASAGEM" in df.columns:
        st.selectbox(
            "Faixa de Defasagem",
            ["Todas"] + sorted(df["FAIXA_DEFASAGEM"].dropna().unique()),
            key="faixa"
        )

with col4:
    if st.session_state.ano == 2024 and "ATIVO_INATIVO" in df.columns:
        st.selectbox(
            "Status",
            ["Todos"] + sorted(df["ATIVO_INATIVO"].dropna().astype(str).unique()),
            key="status"
        )

def limpar_filtros():
    st.session_state["ano"] = sorted(df["ANO"].dropna().unique())[-1]
    st.session_state["fase"] = "Todas"
    st.session_state["faixa"] = "Todas"
    st.session_state["status"] = "Todos"

with col5:
    st.button("🔄 Limpar filtros", on_click=limpar_filtros)


# =========================
# Aplicar filtros
# =========================
df_f = df[df["ANO"] == st.session_state.ano].copy()

if st.session_state.fase != "Todas":
    df_f = df_f[df_f["FASE"].astype(str) == st.session_state.fase]

if st.session_state.faixa != "Todas" and "FAIXA_DEFASAGEM" in df_f.columns:
    df_f = df_f[df_f["FAIXA_DEFASAGEM"] == st.session_state.faixa]

if st.session_state.status != "Todos" and "ATIVO_INATIVO" in df_f.columns:
    df_f = df_f[df_f["ATIVO_INATIVO"].astype(str) == st.session_state.status]

# =========================
# KPIs + Gauge
# =========================
st.subheader("📌 Visão Executiva", divider="blue")

total = len(df_f)
em_risco = (df_f["DEFAS"] < 0).sum() if "DEFAS" in df_f.columns else 0
perc_risco = (em_risco / total) if total > 0 else np.nan

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total de alunos", format_number(total))
k2.metric("Em risco (DEFAS < 0)", format_number(em_risco))
k3.metric("% em risco", format_number(perc_risco * 100, "%0.1f") + "%")
k4.metric("INDE médio", format_number(df_f["INDE_ATUAL"].mean(), "%0.2f") if "INDE_ATUAL" in df_f.columns else "-")

g1, g2 = st.columns([1, 1])
with g1:
    st.plotly_chart(plot_gauge_percent(perc_risco, "Percentual em risco"), width='stretch')
    st.caption("**Interpretação:** verde = melhor cenário, amarelo = atenção, vermelho = criticidade.")
with g2:
    risco_ano = (df.groupby("ANO")["DEFAS"].apply(lambda x: (pd.to_numeric(x, errors="coerce") < 0).mean()).sort_index())
    risco_ano.index = risco_ano.index.astype(str)
    fig = plot_line(risco_ano, "Evolução do % em risco (DEFAS < 0)", yaxis="Percentual em risco")
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, width='stretch')
    st.caption(
        "**Interpretação estratégica:** este indicador mede o impacto longitudinal do programa. "
        "Reduções sucessivas no percentual de alunos em defasagem sugerem efetividade pedagógica; "
        "aumento ou estagnação indicam necessidade de intervenção."
    )


# =========================
# Distribuições principais (estilo EDA)
# =========================
st.subheader("📈 Distribuição dos Indicadores", divider="blue")
st.caption("Gráficos para entender o perfil dos alunos no recorte selecionado (ano/fase/escola).")

a, b, c = st.columns(3)
with a:
    st.plotly_chart(plot_histograma(df_f, "DEFAS", "Distribuição de DEFAS (negativo = defasado)", nbins=12, color=COLORS["red"]), width='stretch')
    st.caption("Quanto mais à esquerda (negativo), maior a defasagem.")
with b:
    st.plotly_chart(plot_histograma(df_f, "IDA", "Distribuição de IDA (desempenho acadêmico)", nbins=20, color=COLORS["green"]), width='stretch')
    st.caption("IDA é um dos indicadores mais ligados ao risco no seu modelo.")
with c:
    st.plotly_chart(plot_histograma(df_f, "IEG", "Distribuição de IEG (engajamento)", nbins=20, color=COLORS["yellow"]), width='stretch')
    st.caption("Engajamento tende a se relacionar com desempenho e ponto de virada.")

d, e, f = st.columns(3)
with d:
    st.plotly_chart(plot_histograma(df_f, "IAN", "Distribuição de IAN (adequação do nível)", nbins=20, color=COLORS["blue"]), width='stretch')
    st.caption("Perfil de defasagem / IAN.")
with e:
    st.plotly_chart(plot_histograma(df_f, "IPS", "Distribuição de IPS (psicossocial)", nbins=20, color=COLORS["light_green"]), width='stretch')
    st.caption("Ajuda a observar padrões que antecedem queda de desempenho/engajamento.")
with f:
    if "IPP" in df_f.columns:
        st.plotly_chart(plot_histograma(df_f, "IPP", "Distribuição de IPP (psicopedagógico)", nbins=20, color=COLORS["blue"]), width='stretch')
        st.caption("IPP confirma/contradiz defasagem.")
    else:
        st.info("IPP não está disponível nesse recorte.")

# =========================
# Relações (scatter) com legenda e explicação
# =========================
st.subheader("🔎 Relações entre Indicadores", divider="blue")

df_f["FLAG_RISCO"] = np.where(df_f["DEFAS"] < 0, "Em risco", "Sem risco")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        plot_scatter(
            df_f, "IEG", "IDA",
            "IEG vs IDA (engajamento x desempenho) — com legenda de risco",
            color_col="FLAG_RISCO",
            color_map={"Em risco": COLORS["red"], "Sem risco": COLORS["green"]},
            height=380
        ),
        width='stretch'
    )
    st.caption("Maior engajamento (IEG) tende a acompanhar melhor desempenho (IDA).")

with col2:
    st.plotly_chart(
        plot_scatter(
            df_f, "IAA", "IDA",
            "IAA vs IDA (autoavaliação x desempenho) — com legenda de risco",
            color_col="FLAG_RISCO",
            color_map={"Em risco": COLORS["red"], "Sem risco": COLORS["green"]},
            height=380
        ),
        width='stretch'
    )
    st.caption("Coerência entre percepção (IAA) e desempenho (IDA).")

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(
        plot_scatter(
            df_f, "IPS", "IDA",
            "IPS vs IDA (psicossocial x desempenho) — com legenda de risco",
            color_col="FLAG_RISCO",
            color_map={"Em risco": COLORS["red"], "Sem risco": COLORS["green"]},
            height=380
        ),
        width='stretch'
    )
    st.caption("Sinais psicossociais podem anteceder queda acadêmica.")
with col4:
    if "IPP" in df_f.columns:
        st.plotly_chart(
            plot_scatter(
                df_f, "IPP", "DEFAS",
                "IPP vs DEFAS (psicopedagógico x defasagem) — com legenda de risco",
                color_col="FLAG_RISCO",
                color_map={"Em risco": COLORS["red"], "Sem risco": COLORS["green"]},
                height=380
            ),
            width='stretch'
        )
        st.caption("Verifica se IPP acompanha (ou não) a defasagem.")
    else:
        st.info("IPP não está disponível nesse recorte.")

# =========================
# Análises Categóricas Estratégicas
# =========================
st.subheader("🏫 Análises Categóricas Estratégicas", divider="blue")
st.caption("Distribuições-chave para apoio à tomada de decisão pedagógica.")

col1, col2 = st.columns(2)

# FASE
if "FASE" in df_f.columns:
    with col1:
        fig = plot_bar(
            df_f,
            "FASE",
            "Distribuição por Fase",
            xaxis="Fase",
            orientation="h",
            top_n=15,
            color=COLORS["blue"]
        )
        st.plotly_chart(fig, width='stretch')
        st.caption("Identifica concentração de alunos por etapa do ciclo.")

# TURMA
if "TURMA" in df_f.columns:
    with col2:
        fig = plot_bar(
            df_f,
            "TURMA",
            "Distribuição por Turma",
            xaxis="Turma",
            orientation="h",
            top_n=15,
            color=COLORS["light_green"]
        )
        st.plotly_chart(fig, width='stretch')
        st.caption("Permite identificar turmas com maior volume ou possível foco de intervenção.")

# Segunda linha
col3, col4 = st.columns(2)

# GÊNERO
if "GENERO" in df_f.columns:
    with col3:
        fig = plot_bar(
            df_f,
            "GENERO",
            "Distribuição por Gênero",
            xaxis="Gênero",
            orientation="h",
            color=COLORS["yellow"]
        )
        st.plotly_chart(fig, width='stretch')
        st.caption("Ajuda a observar possíveis diferenças demográficas.")

# ATIVO / INATIVO (2024)
if "ATIVO_INATIVO" in df_f.columns:
    with col4:
        fig = plot_bar(
            df_f,
            "ATIVO_INATIVO",
            "Situação do Aluno (Ativo/Inativo)",
            xaxis="Status",
            orientation="h",
            color=COLORS["red"]
        )
        st.plotly_chart(fig, width='stretch')
        st.caption("Importante para entender evasão ou desligamentos.")

# Terceira linha
if "ESCOLA" in df_f.columns:
    st.markdown("### 🏫 Distribuição por Escola")
    fig = plot_bar(
        df_f,
        "ESCOLA",
        "Distribuição de Alunos por Escola",
        xaxis="Escola",
        orientation="h",
        top_n=20,
        color=COLORS["blue"]
    )
    st.plotly_chart(fig, width='stretch')
    st.caption("Permite identificar concentração institucional e apoiar parcerias estratégicas.")


# =========================
# Perfil demográfico
# =========================
st.subheader("👥 Perfil Demográfico", divider="blue")

if "IDADE" in df_f.columns:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_bar(df_f, "IDADE", "Distribuição de Idade (contagem)", xaxis="Idade", orientation="h", top_n=20, color=COLORS["light_green"]), width='stretch')
        st.caption("Visão rápida de concentração de idades.")
    with c2:
        st.plotly_chart(plot_histograma(df_f, "IDADE", "Distribuição de Idade (%)", nbins=15, color=COLORS["light_green"], percent=True), width='stretch')
        st.caption("Histograma em percentual (padrão EDA do projeto base).")
else:
    st.info("IDADE não está disponível nesse recorte.")
