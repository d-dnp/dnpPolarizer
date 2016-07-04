#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library
//- See more at: http://www.toptechboy.com/#sthash.A8STFLcE.dpuf
#include <SPI.h>
#include "ad7794.h"


//Ethernet Stuff 
byte mac[] ={ 0x90, 0xA2, 0xDA, 0x0E, 0xAD, 0x0A  }; //Assign mac address
IPAddress ip(10, 1, 15, 243); //Assign the IP Adress
unsigned int localPort = 5000; // Assign a port to talk over
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
String datReq; //String for our data
int packetSize; //Size of the packet
EthernetUDP Udp; // Create a UDP Object

/* THIS EXAMPLE IS WORKING AS OF FRI, MARCH 21 2014, BEFORE I LEFT FOR AMERICA.
THE IMPORTANT BIT IS NEVER TO SWITCH ON BIAS


The instrumentation amplifier needs headroom, so it will only work well if the lower voltage is high enough above ground.
To solve this problem by switching on bias (which should bias V- to Vdd/2) never worked for me.
Maybe the chip cannot source enough current, but I think I have checked that as well.

TASKS:
- restructure the ad7794 library according to the various registers.


//This example has the lcb bit removed, but introduces interrupts
*/

ad7794 ad(12);
long int dataBuffer[1024];

//ad7794 ad(9);

int lightOn = 1;
int millisStart = 0;
int duration = 0;
float range;
char command;
int voltageInt = 0;
float voltageVolt = 0.0;
int resistor;
int biasGenerator;//this governs the AD7794 bias generator. 0: off
int gain = 32;
int gainAB = 32;
int gainCERNOX = 128;
int dataLength = 100;
float dwellTime = 10;
int channel;
String rString = "";
int current = 10;//current in uA

boolean BIAS;
boolean DEBUG = true;

long val = 0;

// DIGITAL PINS - V2
#define S11 2
#define S12 3
#define S13 5
#define S14 6
#define S21 7
#define S22 8
#define S23 9
#define S24 11
#define AD7794CS 12 //note that this causes trouble on the UNO
//cf. https://www.circuitsathome.com/mcu/running-multiple-slave-devices-on-arduino-spi-bus

// I2C LCD DISPLAY STUFF
//#include <LCD.h>
//#include <LiquidCrystal_I2C.h>  // F Malpartida's NewLiquidCrystal library

#define I2C_ADDR    0x27  // Define I2C Address for controller
#define BACKLIGHT_PIN  3
#define En_pin  2
#define Rw_pin  1
#define Rs_pin  0
#define D4_pin  4
#define D5_pin  5
#define D6_pin  6
#define D7_pin  7

#define  LED_OFF  0
#define  LED_ON  1
LiquidCrystal_I2C  lcd(I2C_ADDR,En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin);


void setup() {
  //define output ad7794
  pinMode(12, OUTPUT);


  lcd.begin (16,2);  // initialize the lcd
  //Switch on the backlight
  lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
  lcd.setBacklight(LED_OFF);
  lcd.backlight();
  
  lcd.print("Starting up");
  
  //pinMode(10, INPUT_PULLUP);
  Serial.begin(57600);
  SPI.begin();
  
  Ethernet.begin( mac, ip); //Inialize the Ethernet
  Udp.begin(localPort); //Initialize Udp

  ad.reset();
  Serial.print("Status: ");
  Serial.println(ad.getStatus(), BIN);

  ///////////////////////////////////////////////////////////////////////////
  ///////////// CONFIGURATION REGISTER //////////////////////////////////////
  ///////////////////////////////////////////////////////////////////////////
  channel = 8;//set channel to 8 to monitor AVDD//4:   2.5 mV rather than 4mV
  biasGenerator = 0;//channel;
  
  //configurationRegister high
  //standard configuration: no bias, unipolar coding with boost and zero gain
  byte configHigh = B00011000;
  configHigh |= byte(int(log(gain)/log(2)));
  configHigh |= byte(biasGenerator) << 6;
  
  //configurationRegister low
  //standard configuration: Internal Reference, Buffered
  byte configLow = B10010000;
  configLow |= byte(channel-1); 
  
  if (DEBUG == true) {
    Serial.print("Configuration Register High: ");
    Serial.println(configHigh, BIN);

    Serial.print("Configuration Register Low: ");
    Serial.println(configLow, BIN);
  }
  
  ad.setConfigurationRegister(1, 8, 0);
  //ad.writeTwoRegisters(CONFIGURATION, configHigh, configLow);



  //curent source
  //0b11: 1mA
  //0b10: 210 uA
  //0b01: 10uA
  //0b00: off
  current = 10;
  ad.writeRegister(IOREG, 0b01);//
  delay(1);

  //mode: continuous conversion, 123 Hz
  ad.writeTwoRegisters(MODE, B00000000, B00000011);
  //ad.writeTwoRegisters(MODE, B00000000, B00001111);




  long conRegister = ad.readMultipleRegisters(CONFIGURATION, 2);
  byte ioRegister = ad.readRegister(IOREG);
  long modRegister = ad.readMultipleRegisters(MODE, 2);

  
  if (DEBUG == true) {
    Serial.print("Con: ");
    Serial.println(conRegister, BIN);

    Serial.print("IO: ");
    Serial.println(ioRegister, BIN);

    Serial.print("Mode: ");
    Serial.println(modRegister, BIN);
  }

  //attachInterrupt(10, readADC, FALLING);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  //pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(11, OUTPUT);
  


  // if AD7794 channel is 4, wire current through R1 (check the connection of AD1+ on the board.
  returnPath(channel, true);
  delay(1);
  drivePath(channel, false);
  delay(1);
}

void returnPath(int resistor, boolean BIAS) {
  if (BIAS == true) {
    digitalWrite(S21, HIGH);
  } else {
    digitalWrite(S21, LOW);
  }
  if (resistor == 1) {
    digitalWrite(S22, HIGH);
    digitalWrite(S23, HIGH);
    digitalWrite(S24, HIGH);
  } else if (resistor == 2) {
    digitalWrite(S22, HIGH);
    digitalWrite(S23, LOW);
    digitalWrite(S24, HIGH);
  } else if (resistor == 3) {
    digitalWrite(S22, LOW);
    digitalWrite(S24, LOW);
    digitalWrite(S23, HIGH);

  }
}

void drivePath(int resistor, boolean PLUSFIVE) {
  if (PLUSFIVE == true) {
    digitalWrite(S11, HIGH);
  } else {
    //note that in this case you may want to have the AD7794 current source programmed
    digitalWrite(S11, LOW);
  }
  if (resistor == 1) {
    digitalWrite(S12, HIGH);
    digitalWrite(S13, HIGH);
    digitalWrite(S14, HIGH);
  } else if (resistor == 2) {
    digitalWrite(S12, HIGH);
    digitalWrite(S13, LOW);
    digitalWrite(S14, HIGH);
  } else if (resistor == 3) {
    digitalWrite(S12, LOW);
    digitalWrite(S14, LOW);
    digitalWrite(S13, HIGH);
  }
}

void readADC() {
  //SET REGISTER 4 TO LOW IF ETHERNET SHIELD CONNECTED
  Serial.println("millis:" +  String(millis()));
  val = ad.readMultipleRegisters(DATA, 3);
  
  //Serial.println("Digitizer Level: " + String(float(val) / 0xffffff*100) + " %");
  //Serial.println("Voltage: " + String(float(val) / 0xffffff * 1.17/gain* 1000) + " mV");
  //Serial.println("Resistance: " + String(float(val) / 0xffffff * 1.17/gain/(current*1e-6)) + "Ohm");
}

void checkVCC() {
 ad.setConfigurationRegister(1, 8, 0);
 delay(100);
 val = ad.readMultipleRegisters(DATA, 3);
 Serial.println("Digitizer Level: " + String(float(val) / 0xffffff*100) + " %");
 Serial.println("Voltage: " + String(float(val) / 0xffffff * 1.17/8) + " V");

}

int probeCernox() {
  int start = millis();
  ad.setConfigurationRegister(gainCERNOX, 6, 0);
  delay(10);
  for (int c = 0; c < dataLength; c++) {
   //Serial.print(String(ad.readMultipleRegisters(DATA, 3)) + ","); 
   dataBuffer[c] = ad.readMultipleRegisters(DATA, 3);
   //dataBuffer[c] = ad.readMultipleRegisters(DATA, 3);
   //Serial.print(String(dataBuffer[c]) + ",");
   delay(dwellTime);
  }  
  Serial.println("Measuring Cernox takes " + String(millis() - start) + "ms");
  //dataToEthernet();
}

void dataToEthernet() {
  for (int c = 0; c < dataLength; c++) {
   //Serial.print(String(ad.readMultipleRegisters(DATA, 3)) + ","); 
   dataBuffer[c] = ad.readMultipleRegisters(DATA, 3);
   //dataBuffer[c] = ad.readMultipleRegisters(DATA, 3);
   delay(1);
  }  
}

void dataToSerial() {
 for (int c = 0; c < dataLength; c++) {
  Serial.print(dataBuffer[c], HEX);
  Serial.print(",");
 } 
 Serial.print("\n");
}

void probeVDD() {
  Serial.println("PROBING VDD \n=====================");
  ad.setConfigurationRegister(1, 8, 0); 
  delay(500);
  val = ad.readMultipleRegisters(DATA, 3);
  Serial.println("Val: " +  String(val, HEX));
  Serial.println("Digitizer Level: " + String(float(val) / 0xffffff*100) + " %");
  Serial.println("Voltage: " + String(float(val) / 0xffffff * 1.17*6) + " V");
}

void reportRegistersToSerial() {
 Serial.println("Register\t Value\n=======================");
 delay(3);
 Serial.println("Mode\t\t" + String(ad.readMultipleRegisters(MODE, 2), BIN));
 delay(3);
 Serial.println("Configuration\t" +   String(ad.readMultipleRegisters(CONFIGURATION, 2), BIN)); 
 delay(3);
 Serial.println("IOREG\t" +   String(ad.readRegister(IOREG), BIN)); 
}

int probeAllenBradley(int channel) {
  //configure channel
  ad.setConfigurationRegister(32, channel, 0);

  ad.writeRegister(IOREG, 0b01);

  
  returnPath(channel, false);
  drivePath(channel, true);
  delay(1000);
  returnPath(channel, true);
  drivePath(channel, false);
  delay(1);

  delay(10);
  
  int startTime = millis();
  for (int c = 0; c < dataLength; c++) {
   //Serial.print(String(ad.readMultipleRegisters(DATA, 3)) + ",");
  boolean dataNotRead = true;
   int count = 0;
   while (dataNotRead) {
     count++;
     byte currentStatus = ad.getStatus();
    if (currentStatus < 100) {
     dataBuffer[c] = ad.readMultipleRegisters(DATA, 3);
     dataNotRead = false;
    } else {
     delay(1);
     if (count > 10) {
      Serial.println("10 attempts");
     }
   } 
   }
   delay(dwellTime);
  }  
  //switch off current source
  ad.writeRegister(IOREG, 0b00);
 // for (int c = 0; c < 256; c++) {
 //     Serial.print(String(dataBuffer[c])+ ","); 
 // }
  
  int stopTime = millis();
  Serial.println("Total time: " + String(stopTime-startTime));

  Serial.print("\nMeasured channel "+ String(channel)); 
  return dataBuffer[1023];
}



void loop() {
  delay(1);
  //ETHERNET  STUFF
  packetSize =Udp.parsePacket(); //Reads the packet size
  
  if(packetSize>0) { //if packetSize is >0, that means someone has sent a request
    
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Read the data request
    String datReq(packetBuffer); //Convert char array packetBuffer into a string called datReq
    
    if (datReq =="AB1") { //Do the following if Temperature is requested
    Serial.println("was geht ab?");
    probeAllenBradley(1); 
    dataToSerial();
    } else if (datReq == "AB2") {
    probeAllenBradley(2);
    } else if (datReq == "AB3") {
     probeAllenBradley(3); 
    } else if (datReq == "CERNOX") {
     Serial.println("Probing Cernox");
     probeCernox();
    }
    
    for (int c = 0; c < dataLength; c++) {
      //Serial.println("sending data over Ethernet!");
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //Initialize packet send
      Udp.print(String(dataBuffer[c]) + ","); //Send the temperature data
      Udp.endPacket(); //End the packet
    }
    
          
  }
  memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array


  
  
  if (Serial.available() > 0) // a command is waiting for us!
  {
    //Serial.println("Serial is available");
    command = Serial.read();
    //Serial.print("Command: ");
    //Serial.println(command);
    if (command == '1') {
        //lcd.home();
        //lcd.clear();
        //lcd.setCursor(0,0);
        val = probeAllenBradley(1);
        //rString = String(float(val) / 0xffffff * 1.17/gain/(current*1e-6));
        //lcd.print(command + " " + String(rString) + " Ohm");
        //delay(1000);
    } else if (command == '2') {
        val = probeAllenBradley(2);
    } else if (command == '3') {
         delay(500);
         //int value = Serial.parseInt();
         val = probeAllenBradley(3);
         //writeCapDacA(value, true);  
    } else if (command == '4') {
      Serial.println("Probing Cernox");       
      probeCernox(); 
      dataToSerial();
    } else if (command == '5') {
       delay(500);
      ad.reset(); 
    } else if (command == '6') {
      Serial.print("Status: ");
      Serial.println(ad.getStatus(), BIN);
    } else if (command == '7') {
      probeVDD(); 
    } else if (command == '8') {
     reportRegistersToSerial(); 
    }
    

    if (command != '1' && command != '2' && command != '3') {
      Serial.flush();
    }    
  }


  //if (digitalRead(10) == LOW) {
  delay(10);
  //  Serial.println("millis:" +  String(millis()));
  //val = ad.readMultipleRegisters(DATA, 3);
  //Serial.println("val: " + String(val, HEX));
  //readADC();
  //Serial.println("Resistance: " + String(float(val)/0xffffff*5000) + "Ohm");
  //  delay(500);
  //}

  delay(1000);
}
