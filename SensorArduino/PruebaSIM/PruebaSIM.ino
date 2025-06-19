#include <SoftwareSerial.h>

SoftwareSerial sim800(10, 11); // RX, TX

const String numeroDestino = "+525517034968"; // Reemplaza con tu número real

void setup() {
  Serial.begin(9600);
  sim800.begin(9600);

  delay(1000);
  Serial.println("Iniciando SIM800L...");
  
  verificarConexionSIM800L();
  verificarRegistroRed();
  verificarSenal();

  Serial.println("Presiona cualquier tecla para enviar el SMS...");
}

void loop() {
  if (Serial.available()) {
    Serial.read(); // Leer la tecla presionada
    enviarSMS("Mensaje enviado desde Arduino al presionar una tecla.");
    Serial.println("Mensaje enviado.");
  }
}

void verificarConexionSIM800L() {
  sim800.println("AT");
  delay(1000);
  if (sim800.find("OK")) {
    Serial.println("✅ SIM800L responde a AT");
  } else {
    Serial.println("❌ SIM800L no responde. Verifica conexiones o alimentación.");
  }
}

void verificarRegistroRed() {
  sim800.println("AT+CREG?");
  delay(1000);
  while (sim800.available()) {
    String respuesta = sim800.readString();
    Serial.println("Registro en red: " + respuesta);
    if (respuesta.indexOf("+CREG: 0,1") != -1 || respuesta.indexOf("+CREG: 0,5") != -1) {
      Serial.println("✅ Registrado en red");
      return;
    }
  }
  Serial.println("❌ No registrado en red");
}

void verificarSenal() {
  sim800.println("AT+CSQ");
  delay(1000);
  while (sim800.available()) {
    String respuesta = sim800.readString();
    Serial.println("Nivel de señal: " + respuesta);
  }
}

void enviarSMS(String mensaje) {
  sim800.println("AT+CMGF=1"); // Modo texto
  delay(500);
  sim800.print("AT+CMGS=\"");
  sim800.print(numeroDestino);
  sim800.println("\"");
  delay(1000);
  sim800.print(mensaje);
  delay(500);
  sim800.write(26); // Ctrl+Z
}
