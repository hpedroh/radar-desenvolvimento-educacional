import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "data", "base_consolidada.csv")
    df = pd.read_csv(data_path)
    return df
