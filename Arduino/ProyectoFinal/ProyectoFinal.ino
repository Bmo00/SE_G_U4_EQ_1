#define R 9
#define G 10
#define B 11
int Pin_echo = 3;
int Pin_trig = 2;

void setup() {
  Serial.begin (9600);
  Serial.setTimeout(100);
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(Pin_trig, OUTPUT);
  pinMode(Pin_echo, INPUT);
  digitalWrite(Pin_trig, LOW);
}

int pulso, cm, valor, inicio, fin;
String m, apagar;

void loop() {
  inicio = 0;
  digitalWrite(Pin_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Pin_trig, LOW);

  pulso = pulseIn(Pin_echo, HIGH); //Medición del ancho de pulso recibido en el pin Echo
  cm = pulso / 50;             // Convertimos ese pulso en una distancia y a cm
  Serial.println(cm);


  if (Serial.available() > 0) {
    String metros = Serial.readString();

    fin = metros.indexOf(",", inicio);
    m = metros.substring(inicio, fin);
    inicio = fin + 1;
    fin = metros.indexOf(',', inicio);
    apagar = metros.substring(inicio, fin);

    if (m.toInt() < 6) {
      digitalWrite(R, 1);
      digitalWrite(G, 0);
      digitalWrite(B, 0);
      delay(50);
      digitalWrite(R, 0);
      digitalWrite(G, 0);
      digitalWrite(B, 0);
      delay(50);
      digitalWrite(R, 1);
      digitalWrite(G, 0);
      digitalWrite(B, 0);
    }
    if (apagar.toInt() == 1) {
      digitalWrite(R, 0);
      digitalWrite(G, 0);
      digitalWrite(B, 0);
    }
  }
  delay(100);
}
