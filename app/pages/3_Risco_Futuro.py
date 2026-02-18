import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objs as go

# =========================
# Configuração da página
# =========================
st.set_page_config(page_title="Risco Futuro", layout="wide")

st.title("🔮 Previsão de Risco Futuro (Ano Seguinte)")
st.caption("Modelo Longitudinal — Antecipação estratégica de risco de defasagem.")

# =========================
# Ajuste de caminhos
# =========================
BASE_DIR = os.path.dirname(__file__)                      # .../app/pages
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # raiz do projeto

# =========================
# Carregar modelo longitudinal
# =========================
MODEL_PATH = os.path.join(ROOT_DIR, "models", "modelo_risco_longitudinal.pkl")

if not os.path.exists(MODEL_PATH):
    st.error(f"Modelo não encontrado em: {MODEL_PATH}")
    st.stop()

modelo_dict = joblib.load(MODEL_PATH)
model = modelo_dict["model"]
features_modelo = modelo_dict["features"]

st.success("Modelo longitudinal carregado com sucesso.")


# =========================
# Explicação
# =========================
st.markdown("""
Este modelo utiliza os indicadores do ano atual (t) para prever a probabilidade
do aluno entrar em risco de defasagem no próximo ano (t+1).

Isso permite uma atuação preventiva.
""")

# =========================
# Inputs (ano atual)
# =========================
st.subheader("📊 Indicadores do Ano Atual (t)", divider="blue")

col1, col2, col3, col4 = st.columns(4)

with col1:
    IAA = st.number_input("IAA (Autoavaliação)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col2:
    IEG = st.number_input("IEG (Engajamento)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col3:
    IPS = st.number_input("IPS (Psicossocial)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col4:
    IDA = st.number_input("IDA (Desempenho Acadêmico)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

col5, col6, col7, col8 = st.columns(4)

with col5:
    IPV = st.number_input("IPV (Ponto de Virada)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col6:
    MATEM = st.number_input("Matemática", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col7:
    PORTUG = st.number_input("Português", 0.0, 10.0, 5.0, 0.1, format="%.2f")

with col8:
    INGLES = st.number_input("Inglês", 0.0, 10.0, 5.0, 0.1, format="%.2f")

col9, col10 = st.columns(2)

with col9:
    IDADE = st.number_input("Idade", 5, 25, 12)

with col10:
    TEMPO_PM = st.number_input("Tempo na Passos Mágicos (anos)", 0, 10, 1)

# IPP opcional
if any("IPP" in f for f in features_modelo):
    IPP = st.number_input("IPP (Psicopedagógico)", 0.0, 10.0, 5.0, 0.1, format="%.2f")

dados_input = {}

for f in features_modelo:
    base_name = f.replace("_t", "")

    if base_name == "IAA":
        dados_input[f] = IAA
    elif base_name == "IEG":
        dados_input[f] = IEG
    elif base_name == "IPS":
        dados_input[f] = IPS
    elif base_name == "IDA":
        dados_input[f] = IDA
    elif base_name == "IPV":
        dados_input[f] = IPV
    elif base_name == "MATEM":
        dados_input[f] = MATEM
    elif base_name == "PORTUG":
        dados_input[f] = PORTUG
    elif base_name == "INGLES":
        dados_input[f] = INGLES
    elif base_name == "IDADE":
        dados_input[f] = IDADE
    elif base_name == "TEMPO_PM":
        dados_input[f] = TEMPO_PM
    elif base_name == "IPP" and "IPP" in locals():
        dados_input[f] = IPP
    else:
        dados_input[f] = 0  # fallback

df_input = pd.DataFrame([dados_input])

# =========================
# Botão previsão
# =========================
if st.button("🚀 Prever Risco Futuro"):
    with st.spinner("Calculando risco futuro..."):

        prob = model.predict_proba(df_input)[0][1]
        classe = model.predict(df_input)[0]

        st.subheader("📈 Resultado da Previsão", divider="green")

        colA, colB = st.columns([1,1])

        with colA:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                number={'suffix': "%"},
                title={'text': "Probabilidade de Risco no Próximo Ano"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkred"},
                    'steps': [
                        {'range': [0, 40], 'color': "green"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                }
            ))

            fig.update_layout(height=350)
            st.plotly_chart(fig, width='stretch')

        with colB:
            if prob < 0.4:
                st.success("🟢 Baixo risco futuro.")
                st.markdown("O aluno tende a manter estabilidade.")
            elif prob < 0.7:
                st.warning("🟡 Risco futuro moderado.")
                st.markdown("Recomenda-se acompanhamento contínuo.")
            else:
                st.error("🔴 Alto risco futuro.")
                st.markdown("Sugere-se intervenção preventiva imediata.")

        st.markdown("---")

        st.markdown("### 🔎 Variáveis que mais influenciaram a previsão")

        importancias = pd.Series(model.feature_importances_, index=features_modelo).sort_values(ascending=False)

        fig_imp = go.Figure(go.Bar(
            x=importancias.values,
            y=importancias.index,
            orientation="h"
        ))

        fig_imp.update_layout(
            height=400,
            yaxis={'categoryorder':'total ascending'},
            title="Importância das Features — Modelo Longitudinal"
        )

        st.plotly_chart(fig_imp, width='stretch')
