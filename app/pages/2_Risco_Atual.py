import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import plotly.graph_objs as go

# =========================
# Configuração da página
# =========================
st.set_page_config(page_title="Risco Atual", layout="wide")

st.title("🚨 Previsão de Risco Atual de Defasagem")
st.caption("Ferramenta preditiva baseada em Machine Learning (modelo transversal).")

# =========================
# Ajuste de caminhos
# =========================
BASE_DIR = os.path.dirname(__file__)                 # .../app/pages
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))  # raiz do projeto

# =========================
# Carregar modelo
# =========================
MODEL_PATH = os.path.join(ROOT_DIR, "models", "modelo_risco_transversal.pkl")

if not os.path.exists(MODEL_PATH):
    st.error(f"Modelo não encontrado em: {MODEL_PATH}")
    st.stop()

modelo_dict = joblib.load(MODEL_PATH)
model = modelo_dict["model"]
features_modelo = modelo_dict["features"]

st.success("Modelo carregado com sucesso.")


# =========================
# Explicação
# =========================
st.markdown("""
Este modelo estima a **probabilidade do aluno estar em risco de defasagem no ano atual**.

O risco é definido como:

- **DEFAS < 0 → aluno defasado**
- **DEFAS ≥ 0 → aluno adequado ou adiantado**

Abaixo, insira os indicadores do aluno para obter a previsão.
""")

# =========================
# Inputs
# =========================
st.subheader("📊 Indicadores do Aluno", divider="blue")

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

# =========================
# Montar dataframe de entrada
# =========================
dados_input = {
    "IAA": IAA,
    "IEG": IEG,
    "IPS": IPS,
    "IDA": IDA,
    "IPV": IPV,
    "MATEM": MATEM,
    "PORTUG": PORTUG,
    "INGLES": INGLES,
    "IDADE": IDADE,
    "TEMPO_PM": TEMPO_PM
}

if "IPP" in features_modelo:
    IPP = st.number_input("IPP (Psicopedagógico)", 0.0, 10.0, 5.0, 0.1, format="%.2f")
    dados_input["IPP"] = IPP

df_input = pd.DataFrame([dados_input])

df_input = df_input[features_modelo]

# =========================
# Botão de previsão
# =========================
if st.button("⚡️ Calcular Risco"):
    with st.spinner("Calculando..."):

        prob = model.predict_proba(df_input)[0][1]
        classe = model.predict(df_input)[0]

        st.subheader("📈 Resultado da Previsão", divider="green")

        colA, colB = st.columns([1,1])

        # Gauge
        with colA:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                number={'suffix': "%"},
                title={'text': "Probabilidade de Risco"},
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

        # Interpretação
        with colB:
            if prob < 0.4:
                st.success("🟢 Baixo risco de defasagem.")
                st.markdown("O aluno apresenta indicadores consistentes.")
            elif prob < 0.7:
                st.warning("🟡 Risco moderado de defasagem.")
                st.markdown("Recomenda-se monitoramento pedagógico.")
            else:
                st.error("🔴 Alto risco de defasagem.")
                st.markdown("Sugere-se intervenção pedagógica imediata.")

        st.markdown("---")

        st.markdown("### 🔎 Importância das Variáveis no Modelo")

        importancias = pd.Series(model.feature_importances_, index=features_modelo).sort_values(ascending=False)

        fig_imp = go.Figure(go.Bar(
            x=importancias.values,
            y=importancias.index,
            orientation="h"
        ))

        fig_imp.update_layout(
            height=400,
            yaxis={'categoryorder':'total ascending'},
            title="Importância das Features no Modelo"
        )

        st.plotly_chart(fig_imp, width='stretch')