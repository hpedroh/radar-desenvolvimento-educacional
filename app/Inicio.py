import streamlit as st

# =========================
# Configuração Global
# =========================
st.set_page_config(
    page_title="Radar Educacional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.markdown("## 📊 Radar Educacional")
    st.caption("Monitoramento e Previsão de Defasagem Escolar")

    st.divider()

    st.markdown("### 🎯 Sobre o Projeto")
    st.markdown("""
    Sistema desenvolvido para:

    - 📈 Monitoramento estratégico  
    - 🚨 Identificação de risco atual  
    - 🔮 Antecipação de risco futuro  
    - 👤 Análise individual do aluno  
    """)

    st.divider()

    st.markdown("### 📁 Projeto")
    st.link_button(
        "🔗 Ver Repositório no GitHub",
        "https://github.com/hpedroh/radar-desenvolvimento-educacional.git",
        use_container_width=True
    )

# =========================
# Header Principal
# =========================
st.title("📊 Radar Educacional")
st.markdown(
    "### Inteligência Analítica aplicada à gestão pedagógica"
)

st.markdown(
    """
O **Radar Educacional** transforma indicadores educacionais em insights acionáveis,
permitindo monitoramento contínuo e antecipação de risco de defasagem.
"""
)

st.divider()

# =========================
# Propósito Estratégico
# =========================
st.markdown("## 🎯 Propósito do Sistema")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Monitoramento", "Indicadores consolidados")
col2.metric("⚠️ Risco Atual", "Modelo transversal")
col3.metric("🔮 Risco Futuro", "Modelo longitudinal")
col4.metric("🎯 Intervenção", "Apoio à decisão")

st.markdown(
    """
O sistema foi projetado para apoiar decisões pedagógicas baseadas em evidência,
identificando padrões de risco e antecipando trajetórias de defasagem.
"""
)

st.divider()

# =========================
# Componentes Analíticos
# =========================
st.markdown("## 🧠 Componentes do Sistema")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Dashboard Geral")
    st.markdown("""
    - Evolução histórica de risco  
    - Distribuição de indicadores  
    - Análises categóricas estratégicas  
    - Perfil demográfico  
    """)

    st.markdown("### 🚨 Risco Atual")
    st.markdown("""
    Modelo preditivo que estima a probabilidade
    de defasagem no ano corrente.
    """)

with col2:
    st.markdown("### 🔮 Risco Futuro")
    st.markdown("""
    Modelo longitudinal que antecipa risco
    no ciclo seguinte.
    """)

    st.markdown("### 👤 Consulta Individual")
    st.markdown("""
    Análise detalhada por aluno, integrando:
    - Histórico
    - Indicadores atuais
    - Probabilidade de risco
    """)

st.divider()

# =========================
# Guia de Uso
# =========================
st.markdown("## 🚀 Como Utilizar")

st.info(
    """
📌 **Fluxo recomendado de análise:**

1️⃣ Inicie pelo **Dashboard Geral** para visão estratégica  
2️⃣ Explore o **Risco Atual** para análise operacional  
3️⃣ Utilize o **Risco Futuro** para planejamento preventivo  
4️⃣ Consulte alunos individualmente para decisões pedagógicas específicas  
"""
)

st.divider()

# =========================
# Rodapé
# =========================
st.caption(
    "Sistema desenvolvido para apoio à gestão educacional orientada por dados."
)
