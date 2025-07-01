# Importar librerías necesarias
import tkinter as tk  # Para la interfaz gráfica
from tkinter import messagebox  # Para mostrar mensajes emergentes
import serial  # Para la comunicación serial con Arduino
import time  # Para controlar el tiempo de espera
import joblib  # Para guardar y cargar el modelo entrenado
import threading  # Para crear hilos y manejar la lectura de datos de manera simultánea
import matplotlib.pyplot as plt  # Para la creación de gráficos
from matplotlib.animation import FuncAnimation  # Para animar los gráficos
from twilio.rest import Client  # Para enviar SMS usando Twilio

# -------------------- CONFIGURACIÓN --------------------
arduino_port = 'COM3'  # Puerto del Arduino
baud_rate = 9600  # Velocidad de transmisión

# Definición de las listas globales
distancias = []  # Lista para almacenar las distancias
riesgos = []  # Lista para almacenar los riesgos
sentMessage = False  # Variable de control para enviar SMS solo una vez
contador_inundacion = 0  # Contador para contar las veces consecutivas que la zona está inundada

# -------------------- CONFIGURACIÓN DE TWILIO --------------------
# Configuración de Twilio para el envío de SMS
account_sid = 'AC91fab1803c4d8884b8a61a993566e6ee'   # Tu Account SID de Twilio
auth_token = '911145452c917cde1134d7c2bf05f052'     # Tu Auth Token de Twilio
twilio_phone = '+17629996185'    # Tu número de Twilio
to_phone = '+525517034968'      # Número al que enviar el SMS

client = Client(account_sid, auth_token)  # Crear cliente Twilio

# -------------------- ENVÍO DE SMS --------------------
def send_sms(message):
    """Envía un SMS usando Twilio."""
    try:
        # Enviar mensaje SMS
        message = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=to_phone
        )
        print(f"📤 SMS enviado: {message.sid}")
    except Exception as e:
        print(f"Error enviando SMS: {e}")

# -------------------- CLASIFICACIÓN CON IA --------------------
def clasificar_riesgo(distancia_cm):
    """Clasifica el riesgo basado en la distancia."""
    if distancia_cm <= 18:
        return 'Zona Inundada'  # Riesgo crítico
    elif 18.1 <= distancia_cm < 18.3:
        return 'Riesgo Alto'  # Riesgo alto
    elif 18.3 <= distancia_cm < 18.6:
        return 'Riesgo Medio'  # Riesgo medio
    elif 18.6 <= distancia_cm < 19:
        return 'Riesgo Bajo (Advertencia)'  # Advertencia
    elif 19 <= distancia_cm < 19.5:
        return 'Riesgo Muy Bajo'  # Muy bajo
    else:
        return 'Fuera de peligro'  # Sin riesgo

# -------------------- LECTURA SERIAL + CLASIFICACIÓN --------------------
def leer_datos():
    """Lee los datos del Arduino y clasifica el riesgo."""
    global sentMessage, distancias, riesgos, contador_inundacion
    while True:
        if arduino.in_waiting > 0:  # Si hay datos en espera
            data = arduino.readline().decode('utf-8').strip()  # Leer y decodificar los datos
            print(f"Datos recibidos: {data}")
            try:
                distancia = float(data)  # Convertir los datos a flotante
                riesgo = clasificar_riesgo(distancia)  # Clasificar el riesgo
                print(f"Riesgo clasificado: {riesgo}")

                # Añadir los valores a las listas globales
                distancias.append(distancia)
                riesgos.append(riesgo)

                # Verificar cuántas veces consecutivas se ha detectado "Zona Inundada"
                if "Zona Inundada" in riesgo:
                    contador_inundacion += 1
                else:
                    contador_inundacion = 0  # Resetear el contador si no es "Zona Inundada"

                # Enviar SMS solo si se detecta "Zona Inundada" tres veces consecutivas
                if contador_inundacion >= 3 and not sentMessage:
                    send_sms("⚠️ ALERTA: Inundación detectada. Proceder a protocolos de seguridad ciudadana.")
                    sentMessage = True  # Marcar que ya se envió el mensaje y no se enviará de nuevo
            except ValueError:
                print("❌ Dato inválido recibido.")  # Manejo de error si los datos no son válidos
        time.sleep(1)  # Espera de 1 segundo para la siguiente lectura

# -------------------- ACTUALIZACIÓN DE GRÁFICA --------------------
def actualizar_grafica(frame):
    """Actualiza la gráfica con las mediciones recientes."""
    global distancias, riesgos
    if len(distancias) > 20:
        datos = distancias[-20:]  # Mostrar solo las últimas 20 mediciones
        colores = [
            '#FF0000' if "Zona Inundada" in r else 
            '#FF8C00' if "Riesgo Alto" in r else 
            '#FFFF00' if "Riesgo Medio" in r else 
            '#90EE90' if "Riesgo Bajo (Advertencia)" in r else 
            '#006400' if "Riesgo Muy Bajo" in r else 
            '#0000FF' for r in riesgos[-20:]
        ]
        etiquetas = riesgos[-20:]
    else:
        datos = distancias
        colores = [
            '#FF0000' if "Zona Inundada" in r else 
            '#FF8C00' if "Riesgo Alto" in r else 
            '#FFFF00' if "Riesgo Medio" in r else 
            '#90EE90' if "Riesgo Bajo (Advertencia)" in r else 
            '#006400' if "Riesgo Muy Bajo" in r else 
            '#0000FF' for r in riesgos
        ]
        etiquetas = riesgos

    ax.clear()  # Limpiar la gráfica antes de dibujar
    barras = ax.bar(range(len(datos)), datos, color=colores)  # Dibujar las barras con colores

    # Añadir etiquetas sobre las barras
    for i, barra in enumerate(barras):
        # Mostrar la distancia en la parte superior de la barra
        ax.text(
            barra.get_x() + barra.get_width() / 2,  # Centro de la barra en X
            barra.get_height() + 0.5,  # Colocar la etiqueta justo encima de la barra
            f'{datos[i]:.2f} cm',  # Etiqueta con la distancia
            ha='center',  # Alineación horizontal
            va='bottom',  # Alineación vertical
            color='black',  # Color del texto
            fontsize=8  # Tamaño de la fuente
        )
        
        # Mostrar la clasificación debajo de la barra
        ax.text(
            barra.get_x() + barra.get_width() / 2,  # Centro de la barra en X
            barra.get_height() - 2.5,  # Colocar la clasificación debajo de la barra
            etiquetas[i],  # Etiqueta con el riesgo
            ha='center',  # Alineación horizontal
            va='top',  # Alineación vertical
            color='black',  # Color del texto
            fontsize=8  # Tamaño de la fuente
        )

    ax.set_ylim(0, 30)  # Establecer los límites del eje Y
    ax.set_title("Mediciones de Distancia (cm)")  # Título de la gráfica
    ax.set_ylabel("Distancia")  # Etiqueta eje Y
    ax.set_xlabel("Mediciones recientes")  # Etiqueta eje X

# -------------------- INICIO DEL SISTEMA --------------------
def iniciar_sistema(zona):
    """Inicializa el sistema cargando el modelo y configurando el puerto serial."""
    global modelo, arduino
    try:
        archivo_modelo = "modelo_nezahualcoyotl.pkl" if zona == "Nezahualcóyotl" else "modelo_iztapalapa.pkl"
        modelo = joblib.load(archivo_modelo)  # Cargar el modelo de decisión previamente entrenado
        arduino = serial.Serial(arduino_port, baud_rate)  # Configurar el puerto serial
        print(f"✅ Modelo cargado: {zona}")
        messagebox.showinfo("Modelo cargado", f"Modelo cargado correctamente: {zona}")

        threading.Thread(target=leer_datos, daemon=True).start()  # Hilo para leer datos de manera continua
        animar()  # Iniciar la animación de la gráfica
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el sistema:\n{e}")

# -------------------- INTERFAZ GRÁFICA --------------------
def crear_interfaz():
    """Crear la interfaz gráfica de usuario con las opciones de zona."""
    ventana = tk.Tk()  # Crear la ventana principal
    ventana.title("Sistema de Monitoreo de Inundaciones")  # Título de la ventana
    ventana.geometry("400x200")  # Tamaño de la ventana
    ventana.resizable(False, False)  # Deshabilitar el cambio de tamaño

    label = tk.Label(ventana, text="Selecciona la zona a monitorear:", font=("Arial", 14))
    label.pack(pady=20)  # Etiqueta para seleccionar la zona

    # Botones para seleccionar la zona
    btn_neza = tk.Button(ventana, text="Nezahualcóyotl", font=("Arial", 12),
                         command=lambda: iniciar_sistema("Nezahualcóyotl"))
    btn_neza.pack(pady=5)

    btn_izta = tk.Button(ventana, text="Iztapalapa", font=("Arial", 12),
                         command=lambda: iniciar_sistema("Iztapalapa"))
    btn_izta.pack(pady=5)

    ventana.mainloop()  # Iniciar el ciclo de la interfaz gráfica

# -------------------- GRÁFICA EN TIEMPO REAL --------------------
def animar():
    """Función para animar la gráfica y actualizar en tiempo real."""
    global fig, ax
    fig, ax = plt.subplots()  # Crear la figura y el eje para la gráfica
    ani = FuncAnimation(fig, actualizar_grafica, interval=1000)  # Animación que actualiza cada 1000 ms
    plt.tight_layout()  # Ajustar la disposición de la gráfica
    plt.show()  # Mostrar la gráfica

# -------------------- EJECUCIÓN --------------------
if __name__ == "__main__":
    crear_interfaz()  # Iniciar la interfaz gráfica cuando se ejecute el script
