const int trigPin = 7;
const int echoPin = 6;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  Serial.begin(9600);
  delay(3000); // Esperar al inicio
}

void loop() {
  long duracion;
  float distancia;

  // Disparo del pulso ultrasónico
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Medir tiempo del eco
  duracion = pulseIn(echoPin, HIGH);

  // Calcular distancia en cm
  distancia = duracion * 0.034 / 2.0;

  // Enviar solo la distancia
  Serial.println(distancia);

  delay(5000); // Esperar antes de la siguiente medición
}
