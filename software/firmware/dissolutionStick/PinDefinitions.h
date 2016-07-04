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

// other pins: 20 ground, 21 + 3.3V
const int valve1 = 2;//He gas open
const int valve2 = 3;//He gas close (optional)
const int valve3 = 4;
const int valve4 = 5;//valve on dissolution stick 
const int valve5 = 6;
const int valve6 = 7;//KF50 Sample Space
const int valve7 = 8;
const int valve8 = 9;//He inlet sample space Fast

const int trigger = 13;

const int ledButton = 10; //pushButton
const int ledRed = 11; //red
const int ledGreen = 12; //green

const int pushButton = 0;

const int ttlIN = 13;
const int ttlOUTB = A4;
const int ttlOUTA = A5;

const int transformer1 = 50;
const int transformer2 = 51;

class PinDefinitions {
  public:
    PinDefinitions();
    void configurePins();
};

