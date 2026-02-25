# :bar_chart: Análise Exploratória de Dados (EDA)

Nesta seção, exploramos as nuances do dataset da **Passos Mágicos (2022-2024)** para entender o que realmente impulsiona o desenvolvimento dos alunos e quais sinais antecedem o risco de defasagem.

---

## 📈 Evolução e Perfil de Defasagem

O ponto de partida da nossa análise é o índice **DEFAS** (Diferença entre Fase Atual e Fase Ideal). O gráfico abaixo ilustra como a ONG tem conseguido atuar na redução da defasagem severa ao longo do tempo.

![Perfil de Defasagem](images/eda_faixa_defasagem_ano.png){: align=center width="700" }

!!! info "Insights sobre a Defasagem"
    * **Tendência:** Observa-se uma migração de alunos das faixas "Severa" para "Moderada" e "Adequada", indicando a eficácia pedagógica.
    * **Foco de Alerta:** Alunos que permanecem estagnados na defasagem severa por mais de 2 ciclos são priorizados pelo modelo preditivo.

---

## 🤝 O "Cabo de Guerra": Engajamento vs. Desempenho

Uma das descobertas mais importantes é a correlação entre o **IEG (Engajamento)** e o **IDA (Desempenho Acadêmico)**. Não existe sucesso acadêmico isolado do envolvimento do aluno com a ONG.

=== ":material-chart-scatter-plot: Visão Geral"
    ![IEG vs IDA](images/eda_ieg_vs_ida.png){: align=center width="600" }

=== ":material-lightbulb: Conclusão Analítica"
    !!! success "O Ponto de Virada"
        Alunos com **IEG > 7.5** raramente entram em risco de defasagem, mesmo que iniciem com um IDA baixo. O engajamento atua como um **fator de proteção** para o desenvolvimento escolar.

---

## :material-molecule: Multidimensionalidade e Correlações

O sucesso de um aluno na Passos Mágicos é multidimensional. O **INDE (Índice Global)** não é apenas uma média aritmética, mas o reflexo de um ecossistema equilibrado.

![Mapa de Correlação](images/eda_correlacao.png){: align=center width="700" }

### Matriz de Influência

| Indicador | Impacto no Risco | Observação |
| :--- | :---: | :--- |
| **IPS (Psicossocial)** | :material-arrow-up: Alto | Frequentemente o IPS cai *antes* das notas baixarem. |
| **IAA (Autoavaliação)** | :material-arrow-right: Médio | Alunos com IAA muito superior ao IDA podem estar superestimando sua base. |
| **IPP (Psicopedagógico)** | :material-alert: Crítico | Fundamental para detectar barreiras de aprendizado não verbais. |

---

## :material-comment-search: Drivers do Ponto de Virada (IPV)

!!! tip "O que define o sucesso?"
    A análise mostra que o aumento no **IPV (Índice de Ponto de Virada)** está fortemente ligado à frequência nas atividades extracurriculares e ao apoio psicossocial constante.

---

## :material-database-sync: Resumo da Engenharia de Dados
Para viabilizar estas análises, realizamos:

1.  **Unificação:** Consolidação de 3 anos de bases distintas em um único dataset longitudinal.
2.  **Saneamento:** Padronização de nomes (Snake Case) e tratamento de duplicidades de RA.
3.  **Criação de Features:** Desenvolvimento de métricas como `TEMPO_PM` (Tempo de permanência no programa) para medir a curva de evolução.

---

:arrow_right: **Próximo Passo:** [Entenda como estes dados alimentam nossos Modelos Preditivos](modelagem.md)