/*
  ad7794.h - Library for talking to the ad7794 via SPI.

  Compatibility tested with Arduino due and CS pin 9.
*/
#ifndef ad7794_h
#define ad7794_h
#include "SPI.h"
#include "Arduino.h"

#define COMMUNICATION 0
#define STATUS 0
#define MODE 1
#define CONFIGURATION 2
#define DATA 3
#define IDREG 4
#define IOREG 5
#define OFFREG 6
#define FULL_SCALE_REG 7


class ad7794
{
  public:
    ad7794(int pin);
    void reset();
    byte getStatus();
    byte readRegister(byte address);
    void writeRegister(byte address, byte value);
    void writeTwoRegisters(byte address, byte value1, byte value2);
    void setConfigurationRegister(int gain, int channel, int biasGenerator);
    long readMultipleRegisters(byte address, int bytes);
  private:
    int _pin;
};

#endif
