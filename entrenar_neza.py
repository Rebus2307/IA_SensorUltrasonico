# Importamos las bibliotecas necesarias
import pandas as pd  # Para cargar y manipular el dataset
from sklearn.tree import DecisionTreeClassifier  # Para crear y entrenar el modelo de árbol de decisión
import joblib  # Para guardar el modelo entrenado en un archivo

# Cargar el dataset de Nezahualcoyotl desde un archivo CSV
df = pd.read_csv("datos_nezahualcoyotl.csv")  # Cargar los datos en un DataFrame

# Mapeo de la columna 'Riesgo' de texto a valores numéricos
# Este mapeo es necesario para convertir las categorías de texto (como "Zona Inundada", "Riesgo Alto") 
# a valores numéricos que el modelo pueda procesar.
riesgo_map = {
    "Zona Inundada": 0,               # "Zona Inundada" mapeado a 0
    "Riesgo Alto": 1,                  # "Riesgo Alto" mapeado a 1
    "Riesgo Medio": 2,                 # "Riesgo Medio" mapeado a 2
    "Riesgo Bajo (Advertencia)": 3,    # "Riesgo Bajo (Advertencia)" mapeado a 3
    "Riesgo Muy Bajo": 4,              # "Riesgo Muy Bajo" mapeado a 4
    "Fuera de peligro": 5             # "Fuera de peligro" mapeado a 5
}

# Aplicar el mapeo en la columna 'Riesgo' y guardar el resultado en una nueva columna 'RiesgoNum'
df["RiesgoNum"] = df["Riesgo"].map(riesgo_map)

# Verificamos si hay valores NaN en la columna 'RiesgoNum' después de aplicar el mapeo
# Si encontramos algún valor NaN, significa que hubo algún valor en la columna 'Riesgo' 
# que no pudo ser mapeado correctamente y lo eliminamos.
if df["RiesgoNum"].isna().sum() > 0:
    print(f"Hay {df['RiesgoNum'].isna().sum()} valores NaN en la columna 'RiesgoNum'. Eliminando...")
    df = df.dropna(subset=["RiesgoNum"])  # Eliminar filas con NaN en la columna "RiesgoNum"

# Verificamos las primeras filas del DataFrame para asegurarnos de que el mapeo fue correcto
print(df.head())

# Separamos las características (X) y las etiquetas (y)
# X son las características (en este caso, la distancia en cm), y son las etiquetas (las categorías de riesgo numéricas)
X = df[["distancia_cm"]]  # Tomamos la columna 'distancia_cm' como entrada para el modelo
y = df["RiesgoNum"]  # Tomamos la columna 'RiesgoNum' como la salida, que es lo que queremos predecir

# Creamos el modelo de árbol de decisión
# Este modelo se usará para predecir la categoría de riesgo basado en la distancia
modelo = DecisionTreeClassifier(random_state=42)  # Usamos un valor fijo de 'random_state' para hacer el modelo reproducible
modelo.fit(X, y)  # Entrenamos el modelo con las características (X) y las etiquetas (y)

# Guardamos el modelo entrenado en un archivo con joblib
# Esto permite que el modelo se guarde y se pueda cargar más tarde sin tener que volver a entrenarlo
joblib.dump(modelo, "modelo_nezahualcoyotl.pkl")  # Guardamos el modelo con el nombre "modelo_nezahualcoyotl.pkl"

# Indicamos que el modelo se ha entrenado y guardado correctamente
print("✅ Modelo de Nezahualcoyotl entrenado correctamente y guardado como 'modelo_nezahualcoyotl.pkl'")
