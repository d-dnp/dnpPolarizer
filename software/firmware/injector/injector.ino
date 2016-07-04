const int relay1Pin = 2; //relay 1 control digital Pin.
const int relay2Pin = 4; //relay 2 control digital Pin.
const int sensorPin = 0; //Potentiometer anolog pin.
const int TTLin = 5;     //ttl signal in from dissolution.
const int rev = 1;       //reversal signal 
const int TTLout = 3;    //ttl signal out to spectrometer 

int revSignal = 0;
int sensorValue = 0;     //stores the value coming from the potentiometer.
int goalPosition = 420;  //final position when extended.
int currentPosition = 0; //where the actuator is at any moment.

int ttl = LOW;
int stopVar=0;
boolean extending = false;
boolean retracting = false;

void setup(){
  //Start serial connection.
  Serial.begin(9600);
  
  //Iniatalize the relay pins as output.
  //INitialize the TTL signal as input
  pinMode(relay1Pin,OUTPUT);
  pinMode(relay2Pin,OUTPUT);
  pinMode(TTLin,INPUT);
  pinMode(rev,INPUT);
  pinMode(TTLout, OUTPUT);
  
  //Initialize the relay pins
  digitalWrite(relay1Pin,HIGH);
  digitalWrite(relay2Pin, HIGH);
  digitalWrite(TTLout,LOW);
}

void loop(){
  
  //Read value from sensor.
  currentPosition = analogRead(sensorPin);
  revSignal=analogRead(rev);
  //Red value from TTLin
  ttl = digitalRead(TTLin);
  
  //Printing results in serial monitor.
//  delay(100);  

  Serial.print("Current = ");
  Serial.print(currentPosition);
  Serial.print("\t Goal = ");
  Serial.print(goalPosition);
  Serial.print("\n");
  Serial.print(extending);
  Serial.print("\n");
  Serial.print("reversal = ");
  Serial.print(revSignal);
  Serial.print("\n");
  
  //if reversal signal is high->it has priority over all
  if(revSignal==0)
  {  
    goalPosition=198;
    if (goalPosition<=currentPosition){
      retracting = true;
      extending = false;
      digitalWrite(relay1Pin,LOW);
      digitalWrite(relay2Pin,HIGH);
      Serial.print("Retracting");
      Serial.println("\n");      
    }
  }
  else
  {
    goalPosition = 352;  
    if (ttl==HIGH && stopVar==0){
      if (goalPosition>=currentPosition){
        retracting = false;
        extending = true;
        digitalWrite(relay1Pin,HIGH);
        digitalWrite(relay2Pin,LOW);
        Serial.print("Extending");
        Serial.println("\n");  
      }    
    }
  }
  if (retracting == true && currentPosition <= goalPosition){
    //we have reached our goal, shut the relay off
    digitalWrite(relay1Pin,HIGH);
    digitalWrite(relay2Pin, HIGH);
    retracting = false; 
    Serial.println("IDLE retracting");  
    Serial.println("\n");  
    stopVar=0;
  }
  if (extending == true && currentPosition >= goalPosition-2) {
    //we have reached our goal, shut the relay off
    digitalWrite(relay1Pin,HIGH);
    digitalWrite(relay2Pin, HIGH);
    extending = false; 
    Serial.println("IDLE extending");  
    Serial.println("\n");
    digitalWrite(TTLout,HIGH);
    delay(100);
    digitalWrite(TTLout,LOW);    
    stopVar=1;   
    }
}     

