1.- Instalar Arduino IDE
2.- Conectar arduino al sensor ultrasónico 
3.- Conectar arduino a la computadora
4.- Ejecutar el archivo SensorArduino.ino en Arduino IDE 
ajustar puerto si es necesario, en este caso por default es COM3
5.- Abrir folder SENSOR en python (completo)
6.- Instalar librerías desde la consola (en caso de no tenerlas):

sudo apt-get install python3-tk
pip install pyserial
pip install joblib
pip install matplotlib
pip install twilio
pip install pandas
pip install scikit-learn

7.- En caso de no estar los archivos .pkl dentro del folder, ejecutar entrenar_neza.py o entrenar_iztapalapa.py para generar los archivos
8.- En sensor_gui.py ajustar parámetros con cuenta personal (si se quiere visualizar el mensaje sms): 

# -------------------- CONFIGURACIÓN DE TWILIO --------------------
# Configuración de Twilio para el envío de SMS
account_sid = 'AC91fab1803c4d8884b8a61a993566e6ee'   # Tu Account SID de Twilio
auth_token = '911145452c917cde1134d7c2bf05f052'     # Tu Auth Token de Twilio
twilio_phone = '+17629996185'    # Tu número de Twilio
to_phone = '+525517034968'      # Número al que enviar el SMS

URL para registro: https://www.twilio.com/es-mx

9.- Ejecutar codigo main (sensor_gui.py) y visualizar gráfica
10.- Poner el sensor viendo al fondo del bote y empezar a llenar poco a poco con agua
11.- Observar la gráfica creada desde python
