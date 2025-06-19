import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Cargar el dataset correcto
df = pd.read_csv("datos_nezahualcoyotl.csv")

# Mapear la columna de riesgo
riesgo_map = {"Bajo": 0, "Medio": 1, "Alto": 2}
df["RiesgoNum"] = df["Riesgo"].map(riesgo_map)

# Entrenar el modelo
X = df[["Distancia_cm"]]
y = df["RiesgoNum"]
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X, y)

# Guardar modelo en archivo válido
joblib.dump(modelo, "modelo_neza.pkl")

print("✅ Modelo de Nezahualcóyotl entrenado correctamente.")
