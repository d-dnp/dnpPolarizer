int temperatureADC = 0;
int pressureADC = 0; 

int valves = 0;

float temperature = 0;
float pressure = 0;
float tSet = 20;
float pSet = -5;
String regulation = "pressure";

//timing - delays in ms
int stickValveOn = 0;
int stickValveOff = 3000;
int pushValveOn = 800;
int pushValveOff = 3000;
int triggerOn = 3000;
int triggerOff = 4000;

int valveToSwitch;


float temperatureVoltage = 0;
float temperatureResistance = 0.0;
float currentTemperature = 0.0;

float pressureVoltage = 0.0;
float currentPressure = 0.0;


String triggerReceived = "";
String answer = "";

boolean heaterOn = false;
boolean trig = false; 

byte mac[] ={ 0xDE, 0xAD, 0xDA, 0x0E, 0xAD, 0x7A  }; //Assign mac address
IPAddress ip(10, 1, 15, 250); //Assign the IP Adress
const int localport = 5000;
