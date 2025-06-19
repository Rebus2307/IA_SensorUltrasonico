import serial
# from twilio.rest import Client  # Comentado temporalmente
import time
import joblib

# Configura el puerto serie
arduino_port = '/dev/ttyACM0'
baud_rate = 9600

# Twilio (comentado temporalmente)
# account_sid = 'ACf1ab67a30ec8983187444ca806e26258'
# auth_token = 'ea202aff7bd290cf141eb04e8bcdab33'
# twilio_phone = '+16282450793'
# to_phone = '+525561348712'

# Conexión al puerto serie
arduino = serial.Serial(arduino_port, baud_rate)

# Cliente Twilio (comentado temporalmente)
# client = Client(account_sid, auth_token)

# Variable de control para envío único
sentMessage = False

# Función para enviar SMS (simulada)
def send_sms(message):
    # message = client.messages.create(
    #     body=message,
    #     from_=twilio_phone,
    #     to=to_phone
    # )
    # print(f"Mensaje enviado: {message.sid}")
    
    # Simulación de envío por consola
    print(f"⚠️ [SIMULACIÓN] Se enviaría el siguiente SMS: {message}")

# Mapa inverso de clases
riesgo_map_inv = {
    0: "🟢 Riesgo: Bajo",
    1: "🟡 Riesgo: Medio",
    2: "🔴 Riesgo: Alto - ¡Nivel crítico!"
}

# Seleccionar modelo por zona
print("Selecciona la zona que deseas monitorear:")
print("1. Nezahualcóyotl")
print("2. Iztapalapa")
opcion = input("Escribe 1 o 2 y presiona Enter: ")

if opcion == "1":
    modelo = joblib.load("modelo_neza.pkl")
    print("✅ Modelo cargado: Nezahualcóyotl")
elif opcion == "2":
    modelo = joblib.load("modelo_iztapalapa.pkl")
    print("✅ Modelo cargado: Iztapalapa")
else:
    print("❌ Opción inválida. Terminando el programa.")
    exit()

# Clasificación usando el modelo entrenado
def clasificar_riesgo(distancia_cm):
    prediccion = modelo.predict([[distancia_cm]])[0]
    return riesgo_map_inv[prediccion]

# Esperar datos del Arduino
print("Esperando datos del Arduino...\n")

while True:
    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').strip()
        print(f"Datos recibidos: {data}")
        
        try:
            distancia = float(data)
            riesgo = clasificar_riesgo(distancia)
            print(riesgo)

            if "Alto" in riesgo and not sentMessage:
                send_sms("⚠️ ALERTA: Nivel de agua crítico detectado.")
                sentMessage = True
            elif "Alto" not in riesgo:
                sentMessage = False

        except ValueError:
            print("❌ Dato inválido recibido.")
    
    time.sleep(1)
