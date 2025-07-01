# Importamos las bibliotecas necesarias
import pandas as pd  # Para manipulación y análisis de datos
from sklearn.tree import DecisionTreeClassifier  # Para el clasificador de árbol de decisión
import joblib  # Para guardar y cargar el modelo entrenado

# Cargar el dataset de Nezahualcoyotl desde un archivo CSV
df = pd.read_csv("datos_iztapalapa.csv")

# Mapeo de la columna 'Riesgo' de texto a valores numéricos
# Este mapeo convertirá las categorías de riesgo en valores numéricos, 
# necesarios para el modelo de aprendizaje automático.
riesgo_map = {
    "Zona Inundada": 0,               # "Zona Inundada" mapeado a 0
    "Riesgo Alto": 1,                  # "Riesgo Alto" mapeado a 1
    "Riesgo Medio": 2,                 # "Riesgo Medio" mapeado a 2
    "Riesgo Bajo (Advertencia)": 3,    # "Riesgo Bajo (Advertencia)" mapeado a 3
    "Riesgo Muy Bajo": 4,              # "Riesgo Muy Bajo" mapeado a 4
    "Fuera de peligro": 5             # "Fuera de peligro" mapeado a 5
}

# Aplicamos el mapeo de la columna 'Riesgo' al formato numérico 
# y creamos una nueva columna llamada 'RiesgoNum' en el DataFrame
df["RiesgoNum"] = df["Riesgo"].map(riesgo_map)

# Comprobamos si hay valores NaN en la columna 'RiesgoNum' 
# después de aplicar el mapeo. Si existe algún valor NaN, se eliminarán.
if df["RiesgoNum"].isna().sum() > 0:
    print(f"Hay {df['RiesgoNum'].isna().sum()} valores NaN en la columna 'RiesgoNum'. Eliminando...")
    df = df.dropna(subset=["RiesgoNum"])  # Eliminamos las filas con NaN en 'RiesgoNum'

# Verificamos las primeras filas del DataFrame para asegurarnos de que el mapeo fue realizado correctamente
print(df.head())

# Separamos las características (X) y las etiquetas (y)
# X son las características (distancia en cm), y se utiliza como entrada para el modelo
# y es la columna 'RiesgoNum' (la etiqueta), que es lo que el modelo predice
X = df[["distancia_cm"]]  # Extraemos la columna 'distancia_cm' como característica
y = df["RiesgoNum"]  # Extraemos la columna 'RiesgoNum' como etiqueta

# Creamos un modelo de árbol de decisión y lo entrenamos con los datos
modelo = DecisionTreeClassifier(random_state=42)  # Usamos un valor fijo para reproducibilidad
modelo.fit(X, y)  # Entrenamos el modelo con las características (X) y las etiquetas (y)

# Guardamos el modelo entrenado en un archivo utilizando joblib
# Esto permitirá cargar el modelo en el futuro sin tener que volver a entrenarlo
joblib.dump(modelo, "modelo_iztapalapa.pkl")

# Mensaje final indicando que el modelo se entrenó y guardó correctamente
print("✅ Modelo de Iztapalapa entrenado correctamente y guardado como 'modelo_iztapalapa.pkl'")
