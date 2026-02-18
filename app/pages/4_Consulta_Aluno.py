import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objs as go

# =========================
# Configuração
# =========================
st.set_page_config(page_title="Consulta Aluno", layout="wide")

st.title("👤 Consulta Individual do Aluno")
st.caption("Análise histórica + risco atual + risco futuro")

# =========================
# Ajuste de caminhos
# =========================
BASE_DIR = os.path.dirname(__file__)                      # .../app/pages
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # raiz do projeto

DATA_PATH = os.path.join(ROOT_DIR, "data", "base_consolidada.csv")
MODEL_T_PATH = os.path.join(ROOT_DIR, "models", "modelo_risco_transversal.pkl")
MODEL_L_PATH = os.path.join(ROOT_DIR, "models", "modelo_risco_longitudinal.pkl")

# =========================
# Carregar base
# =========================
if not os.path.exists(DATA_PATH):
    st.error(f"Base não encontrada em: {DATA_PATH}")
    st.stop()

df = pd.read_csv(DATA_PATH)

# =========================
# Carregar modelos
# =========================
if not os.path.exists(MODEL_T_PATH):
    st.error(f"Modelo transversal não encontrado em: {MODEL_T_PATH}")
    st.stop()

if not os.path.exists(MODEL_L_PATH):
    st.error(f"Modelo longitudinal não encontrado em: {MODEL_L_PATH}")
    st.stop()

modelo_t = joblib.load(MODEL_T_PATH)
modelo_l = joblib.load(MODEL_L_PATH)

model_transversal = modelo_t["model"]
features_t = modelo_t["features"]

model_longitudinal = modelo_l["model"]
features_l = modelo_l["features"]

st.success("Base e modelos carregados com sucesso.")


df = pd.read_csv(DATA_PATH)

for c in ["IAN","IDA","IEG","IAA","IPS","IPP","IPV","DEFAS","INDE_ATUAL"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

modelo_t = joblib.load(MODEL_T_PATH)
modelo_l = joblib.load(MODEL_L_PATH)

model_transversal = modelo_t["model"]
features_t = modelo_t["features"]

model_longitudinal = modelo_l["model"]
features_l = modelo_l["features"]

# =========================
# Seleção do aluno
# =========================
st.subheader("🔎 Buscar aluno", divider="blue")

col1, col2 = st.columns(2)

with col1:
    ra_input = st.text_input("RA")

with col2:
    nomes = sorted(df["NOME"].dropna().unique())
    nome_input = st.selectbox("Nome", ["Selecionar"] + nomes)

if ra_input:
    df_aluno = df[df["RA"].astype(str) == str(ra_input)]
elif nome_input != "Selecionar":
    df_aluno = df[df["NOME"] == nome_input]
else:
    df_aluno = pd.DataFrame()

# =========================
# Se aluno encontrado
# =========================
if not df_aluno.empty:

    st.success("Aluno encontrado.")

    df_aluno = df_aluno.sort_values("ANO")

    # -----------------------
    # Histórico
    # -----------------------
    st.subheader("📈 Evolução Histórica", divider="green")

    fig = go.Figure()

    for col in ["IDA","IEG","IAN","IPS","IAA"]:
        if col in df_aluno.columns:
            fig.add_trace(go.Scatter(
                x=df_aluno["ANO"],
                y=df_aluno[col],
                mode="lines+markers",
                name=col
            ))

    fig.update_layout(
        title="Evolução dos Indicadores ao Longo dos Anos",
        xaxis_title="Ano",
        yaxis_title="Valor",
        height=450
    )

    st.plotly_chart(fig, width='stretch')

    # -----------------------
    # Risco Atual
    # -----------------------
    st.subheader("🚨 Risco Atual", divider="red")

    ultimo_registro = df_aluno.iloc[-1]

    input_t = pd.DataFrame([ultimo_registro[features_t]])

    prob_t = model_transversal.predict_proba(input_t)[0][1]

    colA, colB = st.columns([1,1])

    with colA:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_t * 100,
            number={'suffix': "%"},
            title={'text': "Probabilidade Atual"},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 40], 'color': "green"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
            }
        ))

        fig_g.update_layout(height=300)
        st.plotly_chart(fig_g, width='stretch')

    with colB:
        if prob_t < 0.4:
            st.success("Baixo risco atual.")
        elif prob_t < 0.7:
            st.warning("Risco moderado atual.")
        else:
            st.error("Alto risco atual.")

    # -----------------------
    # Risco Futuro
    # -----------------------
    st.subheader("🔮 Risco Futuro (Ano Seguinte)", divider="orange")

    input_l = {}

    for f in features_l:
        base = f.replace("_t", "")
        if base in ultimo_registro:
            input_l[f] = ultimo_registro[base]
        else:
            input_l[f] = 0

    df_input_l = pd.DataFrame([input_l])

    prob_l = model_longitudinal.predict_proba(df_input_l)[0][1]

    colC, colD = st.columns([1,1])

    with colC:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_l * 100,
            number={'suffix': "%"},
            title={'text': "Probabilidade Futuro"},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 40], 'color': "green"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
            }
        ))

        fig_g2.update_layout(height=300)
        st.plotly_chart(fig_g2, width='stretch')

    with colD:
        if prob_l < 0.4:
            st.success("Baixo risco futuro.")
        elif prob_l < 0.7:
            st.warning("Risco futuro moderado.")
        else:
            st.error("Alto risco futuro — atenção preventiva.")

    # -----------------------
    # Comparação com média
    # -----------------------
    st.subheader("📊 Comparação com Média da ONG", divider="blue")

    medias = df.groupby("ANO")[["IDA","IEG","IAN","IPS"]].mean().iloc[-1]

    comparativo = pd.DataFrame({
        "Aluno": ultimo_registro[["IDA","IEG","IAN","IPS"]],
        "Média ONG": medias
    })

    fig_comp = go.Figure()

    fig_comp.add_trace(go.Bar(
        x=comparativo.index,
        y=comparativo["Aluno"],
        name="Aluno"
    ))

    fig_comp.add_trace(go.Bar(
        x=comparativo.index,
        y=comparativo["Média ONG"],
        name="Média ONG"
    ))

    fig_comp.update_layout(
        barmode="group",
        title="Aluno vs Média ONG",
        height=400
    )

    st.plotly_chart(fig_comp, width='stretch')

else:
    st.info("Digite um RA ou selecione um nome para consultar.")
