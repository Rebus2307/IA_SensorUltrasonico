import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Cargar el dataset de Iztapalapa
df = pd.read_csv("datos_iztapalapa.csv")

# Mapear la columna de riesgo (texto a número)
riesgo_map = {"Bajo": 0, "Medio": 1, "Alto": 2}
df["RiesgoNum"] = df["Riesgo"].map(riesgo_map)

# Separar entrada (X) y etiqueta (y)
X = df[["Distancia_cm"]]
y = df["RiesgoNum"]

# Entrenar árbol de decisión
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X, y)

# Guardar modelo entrenado en archivo
joblib.dump(modelo, "modelo_iztapalapa.pkl")

print("✅ Modelo de Iztapalapa entrenado correctamente y guardado como 'modelo_iztapalapa.pkl'")
