/* the only use of this class is to configure all the necessary pins as output pins */
#include "Arduino.h"
#include "PinDefinitions.h"

PinDefinitions::PinDefinitions() {
}

void PinDefinitions::configurePins() {
  //for some reason this stuff needs to be called separately  
 Serial.println("Now we define the pins");
   
  pinMode(ledRed, OUTPUT);
  pinMode(ledGreen, OUTPUT);
  pinMode(ledButton, OUTPUT);  
  //attachInterrupt(pushButton, dissolve, RISING);
  
  pinMode(valve1, OUTPUT);
  digitalWrite(valve1, HIGH);

  pinMode(valve2, OUTPUT);
  digitalWrite(valve2, LOW);
  
  pinMode(valve3, OUTPUT);
  digitalWrite(valve3, LOW);

  pinMode(valve4, OUTPUT);
  digitalWrite(valve4, LOW);
 
  pinMode(valve5, OUTPUT);
  digitalWrite(valve5, LOW);
  
  pinMode(valve6, OUTPUT);
  digitalWrite(valve6, LOW);
  
  pinMode(valve7, OUTPUT);
  digitalWrite(valve7, LOW);
  
  pinMode(valve8, OUTPUT);
  digitalWrite(valve8, LOW);


  pinMode(trigger, OUTPUT);
  digitalWrite(trigger, LOW);

  pinMode(transformer1, OUTPUT);
  pinMode(transformer2, OUTPUT);
  digitalWrite(transformer1, LOW);
  digitalWrite(transformer2, LOW);

  pinMode(ttlOUTA, OUTPUT);
  pinMode(ttlOUTB, OUTPUT);
  pinMode(ttlIN, INPUT);
  
  pinMode(20, OUTPUT);
  pinMode(21, OUTPUT);
  digitalWrite(20, LOW);
  digitalWrite(21, HIGH);
  
  digitalWrite(ledButton, HIGH);
  digitalWrite(ledRed, HIGH);
  digitalWrite(ledGreen, LOW);


}
