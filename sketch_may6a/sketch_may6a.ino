#include <Servo.h>

Servo servoGato;
Servo servoPerro;

void setup() {
  Serial.begin(9600);
  servoGato.attach(9);   // Pin para el servo de gato
  servoPerro.attach(10); // Pin para el servo de perro
}

void loop() {
  if (Serial.available() > 0) {
    char recibido = Serial.read();
    if (recibido == 'G') {
      moverServoGato();
    } else if (recibido == 'P') {
      moverServoPerro();
    }
  }
}

void moverServoGato() {
  servoGato.write(90);
  delay(1000);
  servoGato.write(0);
}

void moverServoPerro() {
  servoPerro.write(90);
  delay(1000);
  servoPerro.write(0);
}
