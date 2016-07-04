#include "Arduino.h"
#include "communication.h"

#include <SPI.h> //SPI required for Ethernet
#include <Ethernet.h> // Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library

Communication::Communication(boolean debug)
{
  //Ethernet Stuff 
  byte mac[] ={ 0xDE, 0xAD, 0xDA, 0x0E, 0xAD, 0x8A  }; //Assign mac address
  IPAddress ip(10, 1, 15, 232); //Assign the IP Adress
  int localPort = 5000; // Assign a port to talk over
  char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
  String datReq; //String for our data
  int packetSize; //Size of the packet
  EthernetUDP _Udp; // Create a UDP Object

  String answer = "";
  boolean DEBUG = debug;


}

float Communication::readFloatEthernet() {
   String response = Communication::readStringEthernet();
   if (response == "FAIL") {
    return 0.11111;
   } else {
    return response.toFloat();
   }
}


int Communication::readIntEthernet() {
   String response = Communication::readStringEthernet();
   Serial.print("Response: ");
   Serial.println(response);
   if (response == "FAIL") {
    return 0.11111;
   } else {
    return response.toInt();
   }
}

String Communication::readStringEthernet() {   
   packetSize =_Udp.parsePacket(); //Reads the packet size

   if(packetSize>0) { //if packetSize is >0, that means someone has sent a request
    _Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Read the data request
    String response(packetBuffer); //Convert char array packetBuffer into a string called dat\Req
    Communication::sendString("CONFIRM");
    return response;

   } else if (DEBUG == true) {
    Serial.println("Packet Size = 0");
    return "FAIL";
   }
}

void Communication::sendString(String text) {
    _Udp.beginPacket(_Udp.remoteIP(), _Udp.remotePort()); //Initialize packet send
    _Udp.print(text); //Send the temperature data
    _Udp.endPacket(); //End the packet
}

void Communication::processEthernetRequest(int *freq, volatile int *dac0, volatile int *dac1) {
  /* This routine, in contrast to everyhting else, is absolutely only working together with dissolutionStick.ino */
  packetSize = _Udp.parsePacket(); //Reads the packet size

  if(packetSize>0) { //if packetSize is >0, that means someone has sent a request
    
    _Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Read the data request
    String dataReq(packetBuffer); //Convert char array packetBuffer into a string called dat\Req

    memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array

    Serial.println("DatReq: " + dataReq);
    // this is pythonic 
    if (String(dataReq.charAt(0))  == "G") { //Do the following if Temperature is requested
      Serial.println("Get Request");
      if (dataReq.substring(1) == "FREQ") {
        answer = String(*freq);
      } else if (dataReq.substring(1) == "DAC0") {
         answer = String(*dac0); 
      } else if (dataReq.substring(1) == "DAC1") {
        answer = String(*dac1);
        //Serial.println("Getting TSET");
      } 
      //delay(5);
    Communication::sendString(answer);      

    } else if (String(dataReq.charAt(0)) == "S") {
      Serial.println("Setting value");
      if (dataReq.substring(1) == "FREQ") {
        *freq = Communication::readIntEthernet();
        Serial.println("Setting FREQ: " + String(*freq));
      } else if (dataReq.substring(1) == "DAC0") {
        *dac0 = Communication::readIntEthernet();
        Serial.println("DAC0: " + String(*dac0));
      } else if (dataReq.substring(1) == "DAC1") {
        *dac1 = Communication::readIntEthernet();
        Serial.println("DAC1: " + String(*dac1));
      }      
    }       
  }
  memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array
}


