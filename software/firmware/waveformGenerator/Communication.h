/* communication.h - library for communicatiing with the Arduino over Ethernet.
 *  Created by Benno Meier, 21 July, 2015
 */
#include <SPI.h> //SPI required for Ethernet
#include <Ethernet.h> // Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library


#ifndef Communication_h

#define Communication_h
//#define EthernetUDP Udp;

class Communication {
  public:
    Communication(boolean debug);
    String readStringEthernet();
    float readFloatEthernet();
    int readIntEthernet();
    void sendString(String text);
    void processEthernetRequest(int *frequency, volatile int *dac0, volatile int *dac1);
    boolean DEBUG;
    char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
    String datReq; //String for our data
    int packetSize; //Size of the packet
    String answer;
    //int UDP_TX_PACKET_MAX_SIZE; 
    byte mac[];// = {0xDE, 0xAD, 0xDA, 0x0E, 0xAD, 0x7A}; //Assign mac address
    IPAddress ip; //{10, 1, 15, 232}; //Assign the IP Adress
    int localPort; // Assign a port to talk over
    EthernetUDP _Udp; // Create a UDP Object
};
#endif
