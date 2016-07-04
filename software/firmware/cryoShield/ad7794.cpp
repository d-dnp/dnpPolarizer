/*
  ad7794.cpp -- Library for talking to the ad7794 via SPI.

  Compatibility tested with Arduino due and CS pin 9.
*/

/* THIS EXAMPLE IS WORKING AS OF FRI, MARCH 21 2014, BEFORE I LEFT FOR AMERICA.
THE IMPORTANT BIT IS NEVER TO SWITCH ON BIAS


The instrumentation amplifier needs headroom, so it will only work well if the lower voltage is high enough above ground.
To solve this problem by switching on bias (which should bias V- to Vdd/2) never worked for me.
Maybe the chip cannot source enough current, but I think I have checked that as well.

TASKS:
- restructure the ad7794 library according to the various registers.

*/
#include "SPI.h"
#include "Arduino.h"
#include "ad7794.h"

ad7794::ad7794(int pin)
{
  //probably this does not work here and has to go into the setup
  //pinMode(pin, OUTPUT);
  _pin = pin;
  //SPI.begin(10);
}


void ad7794::reset() {
 digitalWrite(_pin, LOW);
 SPI.transfer(B11111111);
 SPI.transfer(B11111111);
 SPI.transfer(B11111111);
 SPI.transfer(B11111111);
 digitalWrite(_pin, HIGH); 
 delay(1);
}

byte ad7794::getStatus()
{
 digitalWrite(_pin, LOW);
 //delay(1000);
  SPI.transfer(B01000000);
  byte status = SPI.transfer(0x00);
  digitalWrite(_pin, HIGH);

  return status; 
}



byte ad7794::readRegister(byte address) {
  digitalWrite(_pin, LOW);
  address = address << 3;
  address = address + 64; // read
  SPI.transfer(address);
  byte value = SPI.transfer(0x00);
  digitalWrite(_pin, HIGH);
  return value;
}


void ad7794::writeRegister(byte address, byte value) {
  digitalWrite(_pin, LOW);
  address = address << 3;  
  SPI.transfer(address);
  SPI.transfer(value);//is this correct?
  digitalWrite(_pin, HIGH);
}

void ad7794::writeTwoRegisters(byte address, byte value1, byte value2) {
  address = address << 3;
  digitalWrite(_pin, LOW);
  SPI.transfer(address);
  SPI.transfer(value1);
  SPI.transfer(value2);//is this correct?
  digitalWrite(_pin, HIGH);
}

void ad7794::setConfigurationRegister(int gain, int channel, int biasGenerator) {
  //configurationRegistor high
  //standard configuration: no bias, unipolar coding with boost and zero gain
  byte configHigh = B00011000;
  configHigh |= byte(int(log(gain)/log(2)));
  configHigh |= byte(biasGenerator) << 6;
  
  //configurationRegistor low
  //standard configuration: Internal Reference, Buffered
  byte configLow = B10010000;
  configLow |= byte(channel-1); 
    
  ad7794::writeTwoRegisters(CONFIGURATION, configHigh, configLow);
}


long ad7794::readMultipleRegisters(byte address, int bytes) {
 //read a given number of bytes starting at register. 

 address = address << 3;
 address = address + 64;//this is a read

 long answer = 0;
 long rep;
 digitalWrite(_pin, LOW);
 SPI.transfer(address);
 for (int i = 0; i<bytes; i++) {
  //Serial.println("i: " + String(i));
  rep  = SPI.transfer(0x00);
  answer += rep << (8*(bytes - i - 1));
 
  //Serial.println("rep: " +  String(rep, HEX));
 }
 digitalWrite(_pin, HIGH);
 return answer;
}

