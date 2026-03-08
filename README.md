# 📊 Radar Educacional --- Análise e Previsão de Risco de Defasagem

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Machine
Learning](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Concluído-success)

------------------------------------------------------------------------

## 🎯 Sobre o Projeto

O **Radar Educacional** foi desenvolvido no contexto do **Datathon --
Pós-Tech Data Analytics (FIAP)** com dados da ONG **Passos Mágicos**.

O objetivo do projeto é transformar indicadores pedagógicos e
psicossociais em inteligência analítica para:

-   Identificar alunos em risco de defasagem
-   Antecipar risco no ciclo seguinte
-   Apoiar intervenções pedagógicas baseadas em dados
-   Avaliar a efetividade do programa educacional

------------------------------------------------------------------------

## 📖 Documentação Detalhada
Acesse a documentação técnica completa do projeto, incluindo detalhes da modelagem e análises profundas:

👉 **[Clique aqui para acessar a Documentação Oficial](https://hpedroh.github.io/radar-desenvolvimento-educacional)**

------------------------------------------------------------------------

## 🔗 Acessos Rápidos
- 🚀 **Aplicação Streamlit: [Clique aqui para acessar a aplicação](https://radar-desenvolvimento-educacional.streamlit.app/)**

------------------------------------------------------------------------

## 🏫 Contexto

A base de dados contempla os anos 2022, 2023 e 2024 e utiliza os
seguintes indicadores:

-   IAN -- Índice de Adequação de Nível\
-   IDA -- Índice de Desempenho Acadêmico\
-   IEG -- Índice de Engajamento\
-   IAA -- Índice de Autoavaliação\
-   IPS -- Índice Psicossocial\
-   IPP -- Índice Psicopedagógico\
-   IPV -- Índice de Ponto de Virada\
-   INDE -- Índice Global do Aluno\
-   DEFAS -- Indicador de Defasagem

------------------------------------------------------------------------

# 📊 Parte 1 --- Storytelling Analítico

Foram respondidas 10 perguntas estratégicas sobre evolução da defasagem,
desempenho, engajamento e impacto psicossocial.

Principais insights:

-   Engajamento (IEG) está fortemente associado ao desempenho (IDA)
-   IPS antecede quedas acadêmicas
-   A combinação IDA + IEG + IPS é forte preditora do INDE
-   Redução consistente de DEFAS sugere impacto positivo do programa

------------------------------------------------------------------------

# 🤖 Parte 2 --- Modelagem Preditiva

## 🚨 Modelo Transversal (Risco Atual)

Prediz se o aluno está em risco no ano corrente.

-   Accuracy ≈ 71%
-   ROC AUC ≈ 0.77

## 🔮 Modelo Longitudinal (Risco Futuro)

Prediz risco no ano seguinte usando dados do ano atual.

-   Accuracy ≈ 74%
-   ROC AUC ≈ 0.83

------------------------------------------------------------------------

# 🚀 Aplicação Streamlit

A aplicação possui:

-   📊 Dashboard Geral
-   🚨 Risco Atual
-   🔮 Risco Futuro
-   👤 Consulta Individual

Deploy realizado via Streamlit Community Cloud.

------------------------------------------------------------------------

# 📁 Estrutura do Projeto

    radar-desenvolvimento-educacional/
    ├── app/                # Aplicação Streamlit
    ├── data/               # Bases de dados (Raw e Consolidada)
    ├── docs/               # Documentação MkDocs (Markdown e Imagens)
    ├── models/             # Modelos XGBoost (.pkl)
    ├── notebooks/          # Notebooks de análise e treinamento
    ├── src/                # Scripts auxiliares (load_data, charts)
    ├── mkdocs.yml          # Configuração da documentação
    ├── requirements.txt    # Dependências do projeto
    └── README.md

------------------------------------------------------------------------

# 📌 Conclusão

O projeto integra análise exploratória, modelagem preditiva e aplicação
interativa, gerando impacto estratégico para gestão educacional baseada
em dados.

------------------------------------------------------------------------

# 📜 Licença

Projeto acadêmico desenvolvido para o Datathon -- Pós-Tech FIAP.