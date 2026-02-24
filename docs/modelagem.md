# Modelagem Preditiva

Utilizamos o algoritmo **XGBoost Classifier** para dois cenários distintos.

## 1. Modelo Transversal (Risco Atual)
Focado em identificar alunos que já estão em situação crítica no ano corrente.

**Performance:**
![Curva ROC Transversal](images/eda_roc_curve_transversal.png)

### Principais Drivers
Os indicadores que mais influenciam o risco atual são:
![Importância Transversal](images/model_transversal_importance.png)

## 2. Modelo Longitudinal (Risco Futuro)
Modelo diferencial que utiliza dados do ano anterior para prever a situação do ano seguinte.
![Importância Longitudinal](images/model_longitudinal_importance.png)