#include <Servo.h>

Servo myServo;  // Create a servo object

void setup() {
  Serial.begin(9600);     // Start serial communication
  myServo.attach(9);      // Attach servo to pin D9 (change if needed)
}

void loop() {
  if (Serial.available()) {
    int angle = Serial.parseInt();  // Read the incoming integer

    if (angle >= 0 && angle <= 180) {
      myServo.write(angle);  // Move the servo to the received angle
      Serial.print("Moved to angle: ");
      Serial.println(angle);
    } else {
      Serial.println("Invalid angle received.");
    }

    // Clear out any leftover bytes in
