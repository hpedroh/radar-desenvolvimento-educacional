# :brain: Inteligência e Modelagem Preditiva

Nesta seção, detalhamos a construção dos modelos de Inteligência Artificial baseados no algoritmo **XGBoost (Extreme Gradient Boosting)**, treinados para atuar na prevenção da defasagem escolar.

---

## :material-sitemap: Estratégia de Modelagem

Para uma cobertura completa do problema, não desenvolvemos apenas um modelo, mas uma **estratégia dual** que atende a diferentes necessidades da ONG:

<div class="grid cards" markdown>

-   :material-magnify-expand: **Modelo Transversal**

    **Foco:** Diagnóstico do "Hoje".
    Identifica alunos que apresentam sinais de defasagem no ano letivo atual para intervenção imediata.

-   :material-history: **Modelo Longitudinal**

    **Foco:** Predição do "Amanhã".
    Utiliza o comportamento histórico (ano $t$) para prever o risco de defasagem no próximo ano ($t+1$).

</div>

---

## :material-file-check: Performance e Resultados

Utilizamos o **XGBoost** pela sua alta performance em dados tabulares e capacidade de lidar com dados faltantes (comum em cadastros de ONGs).

=== ":material-vector-point: Modelo Transversal (Risco Atual)"

    !!! info "Objetivo: Identificação Imediata"
        O modelo foi calibrado para maximizar o **Recall**, garantindo que a ONG não deixe nenhum aluno em risco passar despercebido.

    ![Curva ROC Transversal](images/eda_roc_curve_transversal.png){: align=center width="500" }

    **Métricas de Validação (Base 2024):**
    
    | Métrica | Resultado | Status |
    | :--- | :---: | :--- |
    | **ROC AUC** | **0.77** | :material-check-circle: Bom |
    | **Precisão (Classe 1)** | 64% | :material-information: Moderado |
    | **Recall (Classe 1)** | **85%** | :material-star: Excelente |

=== ":material-fast-forward: Modelo Longitudinal (Risco Futuro)"

    !!! success "Diferencial Técnico"
        Este modelo alcançou uma performance superior ao transversal, demonstrando que o histórico acadêmico é um preditor poderosíssimo para o futuro.

    ![Curva ROC Longitudinal](images/model_longitudinal_roc.png){: align=center width="500" }

    **Métricas de Validação (Pares t -> t+1):**
    
    | Métrica | Resultado | Status |
    | :--- | :---: | :--- |
    | **ROC AUC** | **0.83** | :material-star: Excelente |
    | **Acurácia Geral** | 74% | :material-check-circle: Sólido |

---

## :material-order-numeric-ascending: O que define o Risco? (Drivers)

Entender o "porquê" da decisão do modelo é fundamental para a confiança pedagógica. Abaixo, os indicadores que mais pesam na decisão matemática da IA:

### Importância das Variáveis (Feature Importance)

<div class="grid" markdown>

![Importância Transversal](images/model_transversal_importance.png)
*Drivers do Modelo Transversal: Foco em índices acadêmicos e idade.*

![Importância Longitudinal](images/model_longitudinal_importance.png)
*Drivers do Modelo Longitudinal: Foco em tendências e tempo de casa.*

</div>

!!! tip "Interpretação para a ONG"
    Note que o **IPS (Índice Psicossocial)** e o **IEG (Engajamento)** aparecem consistentemente no topo. Isso confirma a tese de que o bem-estar emocional e a presença ativa são os maiores protetores contra a defasagem.

---

## :material-shield-check: Considerações de Deploy

Os modelos foram exportados utilizando a biblioteca `joblib` e estão integrados à aplicação **Streamlit**, permitindo:
1.  **Inferência em tempo real** para novos alunos.
2.  **Análise de "What-if"** (O que acontece com o risco se aumentarmos o engajamento deste aluno?).

---

:arrow_right: **Próximo Passo:** [Veja como operar estas predições no Guia do Usuário](guia.md)