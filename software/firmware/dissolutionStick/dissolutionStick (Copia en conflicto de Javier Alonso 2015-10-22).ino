#include <Wire.h>
#include <LCD.h>
#include <LiquidCrystal_I2C.h>  // F Malpartida's NewLiquidCrystal library
#include <SPI.h> //SPI required for Ethernet
#include <Ethernet.h> // Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library

#include "PinDefinitions.h"
#include "Variables.h"
#include "Communication.h"

boolean DEBUG = false;

Communication comm(true); 
PinDefinitions pinDefs; 

LiquidCrystal_I2C  lcd(I2C_ADDR,En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin);

void setup() 
{ 
  Ethernet.begin(mac, ip);
  comm._Udp.begin(localport);
  
  Serial.begin(57600);
  if (DEBUG == true) {
    Serial.println("Starting setup");
  }

  pinDefs.configurePins();


  
  lcd.begin(16,2);
  lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
  lcd.setBacklight(1);
  lcd.backlight();
  
  if (DEBUG == true) {
    Serial.println("Setup complete");
  }
}

void dissolve() {
  //lcd.print("DISSOLVE");
  digitalWrite(valve4, HIGH);
  delay(500);
  digitalWrite(valve1, HIGH);
  //lcd.print("DONE");
  for (int thisCount = 0; thisCount <= 10; thisCount++) {
     digitalWrite(ledRed, HIGH);
     digitalWrite(ledGreen, LOW);
    delay(100); 
    digitalWrite(ledRed, LOW);
    digitalWrite(ledGreen, HIGH);
    delay(100);
  }
 digitalWrite(valve4, LOW);
 digitalWrite(valve1, LOW);
 digitalWrite(valve2, LOW);
 delay(800);
 digitalWrite(ttlOUTA, HIGH);
 delay(1000);
 digitalWrite(ttlOUTA, LOW);
}



void loop() {
  //comm.parseRequest();
  comm.processEthernetRequest(&temperature, &pressure, &tSet, &pSet, &regulation, &heaterOn);
  
  temperatureADC = analogRead(1);
  temperatureVoltage = float(temperatureADC)/1024*5;
  temperatureResistance = temperatureVoltage/(5-temperatureVoltage)*470;
  currentTemperature = (temperatureResistance - 100)/0.385;
  temperature = 0.95*temperature + 0.05*currentTemperature;//-15 is a correction to the datasheet.

  //Serial.println("TSET:" + String(tSet));

  if (regulation == "temperature") {
    if (currentTemperature < tSet) {
      heaterOn = true; 
    } else {
      heaterOn = false;
    }
  } else if (regulation == "pressure") {
    if (currentPressure < pSet) {
      heaterOn = true; 
    } else {
      heaterOn = false;
    }
  } else {
   // if (DEBUG == true) {
      Serial.println("REGULATION not valid");
      delay(1000);
   // }
  }
  if (heaterOn == true) {
    Serial.println("Heater on!");
     digitalWrite(transformer1, HIGH);
     digitalWrite(transformer2, HIGH);
     digitalWrite(ledRed, HIGH);
  } else {
    digitalWrite(transformer1, LOW);
    digitalWrite(transformer2, LOW);
    digitalWrite(ledRed, LOW); 
  }
  

  pressureADC = analogRead(2);
  pressureVoltage = float(pressureADC)/1024*5;
  currentPressure = (pressureVoltage/100 - 0.004)*15/0.016 + 1;
  pressure = 0.95*pressure + 0.05*currentPressure;

  if (DEBUG == true) {
    delay(300);
    Serial.println("TEMPERATURE");
    Serial.println("=======================");
    Serial.println("1: " + String(temperatureADC));
    Serial.println("temperatureVoltage: " + String(temperatureVoltage));
    Serial.println("R: " + String(temperatureResistance));
    Serial.println("current temperature: " + String(currentTemperature));
    Serial.println("temperature: " + String(temperature)); 
    Serial.println("voltage pressure: " + String(pressureVoltage));
    Serial.println("Pressure: " + String(pressure));  
    Serial.println("2: " + String(pressureADC));
    Serial.println("3: " + String(analogRead(3)));
  }

  lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("T: " + String(temperature) + " C");
  lcd.setCursor(0,0);
  lcd.print("P: " + String(pressure) + " bar" + triggerReceived);


  if (digitalRead(ttlIN) == HIGH) {
   triggerReceived = " TRIG"; 
  } else {
   triggerReceived = ""; 
  }

  if (analogRead(0) < 300) {
   dissolve(); 
  }
    
  if (Serial.available() > 0) {
    // read the incoming byte:
    valveToSwitch = Serial.parseInt();

    Serial.print("Valve to Switch: " + String(valveToSwitch));
    
    if (valveToSwitch < 7) {
      digitalWrite(valveToSwitch +1, !digitalRead(valveToSwitch + 1));
     } else if (valveToSwitch == 11) {
      dissolve(); 
     } else if (valveToSwitch == 12) {
      for (int i = 0; i < 1000; i++) {
        digitalWrite(ttlOUTA, !digitalRead(ttlOUTA));
        delay(1000);
        Serial.println("Out: " + String(digitalRead(ttlOUTA)));
      }
     }
  }
  
  
   
}
