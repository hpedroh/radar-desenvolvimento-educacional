# :open_book: Guia do Utilizador

Este guia orienta a equipa da **Passos Mágicos** sobre como navegar e extrair valor das quatro ferramentas principais integradas na aplicação.

---

## :bar_chart: 1. Dashboard Geral
Área voltada para a gestão estratégica, permitindo uma visão macro da evolução da ONG.

* **Filtros Inteligentes:** Utilize a barra lateral para filtrar por **Ano** ou **Fase** (Quartzo, Ágata, etc.).
* **KPIs de Impacto:** Acompanhe em tempo real o total de alunos, o INDE médio e a evolução do índice de defasagem.
* **Análise de Fluxo:** Observe como os alunos estão a migrar entre as faixas de risco ao longo dos anos.

![Demonstração Dashboard](images/eda_faixa_defasagem_ano.png){: align=center width="700" }

---

## :material-alert-decagram: 2. Monitor de Risco Atual
Ferramenta para intervenção imediata baseada no **Modelo Transversal**.

1.  **Identificação:** O sistema lista todos os alunos classificados como "Em Risco" no ano corrente.
2.  **Triagem:** Utilize a tabela para ordenar alunos pelo índice de risco (probabilidade matemática).
3.  **Foco:** Priorize alunos com **IPS (Psicossocial)** baixo, pois estes são os que têm maior probabilidade de evasão ou queda de rendimento.

!!! info "Nota Técnica"
    Este modelo utiliza os dados do ano letivo em curso para detetar anomalias de comportamento acadêmico e engajamento.

---

## :material-crystal-ball: 3. Predição de Risco Futuro
A funcionalidade mais avançada do sistema, utilizando o **Modelo Longitudinal**.

* **Objetivo:** Antecipar quem poderá entrar em defasagem no próximo ano.
* **Ação Preventiva:** Permite à coordenação pedagógica planear o reforço escolar ou apoio psicológico antes mesmo de o aluno apresentar notas baixas.

!!! tip "Como interpretar?"
    Se um aluno aparece com risco alto para o próximo ano, verifique o seu **IEG (Engajamento)**. Muitas vezes, uma queda no engajamento precede a queda no desempenho.

---

## :material-account-search: 4. Consulta Individual do Aluno
Área de "deep dive" para tutores e psicólogos.

1.  **Pesquisa:** Selecione o nome do aluno no menu suspenso.
2.  **Histórico:** Veja a evolução de todos os índices (**IDA, IEG, IPS, IPP**) de forma visual.
3.  **Veredito da IA:** O sistema apresenta a probabilidade de risco específica para aquele aluno, acompanhada dos principais fatores que estão a influenciar essa nota.

---

## :material-frequently-asked-questions: Perguntas Frequentes

!!! question "O que significa um risco de 85%?"
    Significa que, com base no comportamento histórico de outros alunos com indicadores semelhantes, a probabilidade de este aluno apresentar defasagem escolar é muito alta.

!!! warning "Dados Faltantes"
    Se alguns gráficos não carregarem para um aluno específico, verifique se todos os campos foram preenchidos na base de dados (PEDE). O modelo requer pelo menos os índices básicos para realizar a predição.

---

## :material-check-decagram: Boas Práticas de Uso

* **Revisões Mensais:** Recomendamos que a equipa pedagógica aceda ao monitor de risco pelo menos uma vez por mês.
* **Exportação:** Utilize o botão de exportação lateral do Streamlit para descarregar tabelas de alunos em risco para reuniões de conselho de classe.
* **Cruzamento de Dados:** Nunca tome uma decisão baseada apenas num índice; cruze sempre o **IDA (Notas)** com o **IPS (Emocional)**.

---

:arrow_right: **Dúvidas Técnicas?** [Consulte os Detalhes da Modelagem](modelagem.md)