import joblib
import os

def load_models():
    base_path = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(base_path, "models")

    modelo_transversal = joblib.load(os.path.join(model_path, "modelo_risco_transversal.pkl"))
    modelo_longitudinal = joblib.load(os.path.join(model_path, "modelo_risco_longitudinal.pkl"))

    return modelo_transversal, modelo_longitudinal
