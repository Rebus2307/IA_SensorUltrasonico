import tkinter as tk
from tkinter import messagebox
import serial
import time
import joblib
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# from twilio.rest import Client  # Twilio (comentado temporalmente)

# -------------------- CONFIGURACIÓN --------------------

arduino_port = '/dev/ttyACM0'
baud_rate = 9600

# Twilio (comentado temporalmente)
# account_sid = 'ACf1ab67a30ec8983187444ca806e26258'
# auth_token = 'ea202aff7bd290cf141eb04e8bcdab33'
# twilio_phone = '+16282450793'
# to_phone = '+525561348712'

# client = Client(account_sid, auth_token)  # Cliente Twilio

riesgo_map_inv = {
    0: "🟢 Riesgo: Bajo",
    1: "🟡 Riesgo: Medio",
    2: "🔴 Riesgo: Alto - ¡Nivel crítico!"
}

modelo = None
arduino = None
distancias = []
riesgos = []
sentMessage = False

# -------------------- ENVÍO DE SMS --------------------

def send_sms(message):
    # --- Twilio real ---
    # message = client.messages.create(
    #     body=message,
    #     from_=twilio_phone,
    #     to=to_phone
    # )
    # print(f"📤 SMS enviado: {message.sid}")
    
    # --- Simulación ---
    print(f"⚠️ [SIMULACIÓN] Se enviaría el siguiente SMS: {message}")

# -------------------- CLASIFICACIÓN CON IA --------------------

def clasificar_riesgo(distancia_cm):
    prediccion = modelo.predict([[distancia_cm]])[0]
    return riesgo_map_inv[prediccion]

# -------------------- LECTURA SERIAL + CLASIFICACIÓN --------------------

def leer_datos():
    global sentMessage
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            print(f"Datos recibidos: {data}")
            try:
                distancia = float(data)
                riesgo = clasificar_riesgo(distancia)
                print(riesgo)

                distancias.append(distancia)
                riesgos.append(riesgo)

                if "Alto" in riesgo and not sentMessage:
                    send_sms("⚠️ ALERTA: Nivel de agua crítico detectado.")
                    sentMessage = True
                elif "Alto" not in riesgo:
                    sentMessage = False
            except ValueError:
                print("❌ Dato inválido recibido.")
        time.sleep(1)

# -------------------- ACTUALIZACIÓN DE GRÁFICA --------------------

def actualizar_grafica(frame):
    if len(distancias) > 20:
        datos = distancias[-20:]
        colores = ['green' if "Bajo" in r else 'orange' if "Medio" in r else 'red' for r in riesgos[-20:]]
    else:
        datos = distancias
        colores = ['green' if "Bajo" in r else 'orange' if "Medio" in r else 'red' for r in riesgos]

    ax.clear()
    ax.bar(range(len(datos)), datos, color=colores)
    ax.set_ylim(0, 30)
    ax.set_title("Mediciones de Distancia (cm)")
    ax.set_ylabel("Distancia")
    ax.set_xlabel("Mediciones recientes")

# -------------------- INICIO DEL SISTEMA --------------------

def iniciar_sistema(zona):
    global modelo, arduino
    try:
        archivo_modelo = "modelo_neza.pkl" if zona == "Nezahualcóyotl" else "modelo_iztapalapa.pkl"
        modelo = joblib.load(archivo_modelo)
        arduino = serial.Serial(arduino_port, baud_rate)
        print(f"✅ Modelo cargado: {zona}")
        messagebox.showinfo("Modelo cargado", f"Modelo cargado correctamente: {zona}")

        threading.Thread(target=leer_datos, daemon=True).start()
        animar()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el sistema:\n{e}")

# -------------------- INTERFAZ GRÁFICA --------------------

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema de Monitoreo de Inundaciones")
    ventana.geometry("400x200")
    ventana.resizable(False, False)

    label = tk.Label(ventana, text="Selecciona la zona a monitorear:", font=("Arial", 14))
    label.pack(pady=20)

    btn_neza = tk.Button(ventana, text="Nezahualcóyotl", font=("Arial", 12),
                         command=lambda: iniciar_sistema("Nezahualcóyotl"))
    btn_neza.pack(pady=5)

    btn_izta = tk.Button(ventana, text="Iztapalapa", font=("Arial", 12),
                         command=lambda: iniciar_sistema("Iztapalapa"))
    btn_izta.pack(pady=5)

    ventana.mainloop()

# -------------------- GRÁFICA EN TIEMPO REAL --------------------

def animar():
    global fig, ax
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, actualizar_grafica, interval=1000)
    plt.tight_layout()
    plt.show()

# -------------------- EJECUCIÓN --------------------

if __name__ == "__main__":
    crear_interfaz()
