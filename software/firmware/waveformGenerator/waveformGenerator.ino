#include <SPI.h> //SPI required for Ethernet
#include <Ethernet.h> // Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library
/*
  Simple Waveform generator with Arduino Due

  * connect two push buttons to the digital pins 2 and 3 
    with a 10 kilohm pulldown resistor to choose the waveform
    to send to the DAC0 and DAC1 channels
  * connect a 10 kilohm potentiometer to A0 to control the 
    signal frequency

 */


 
#include "Communication.h"
#include "Waveforms.h"
#include "fullWaveform.h"

byte mac[] ={ 0xDE, 0xAD, 0xDA, 0x0E, 0xAD, 0x8A  }; //Assign mac address
IPAddress ip(10, 1, 15, 232); //Assign the IP Adress
const int localport = 5000;

Communication comm(true); 

#define oneHzSample 1000000/maxSamplesNum  // sample for the 1Hz signal expressed in microseconds 

const int button0 = 2, button1 = 3;
volatile int dac0 = 0, dac1 = 0;
int frequency = 10000;

volatile boolean timerOn;


volatile int i = 0;
int sample;

volatile boolean l;


//TC1 ch 0
void TC3_Handler()
{       // we want to cover 20% of 4096
        // or 0 to 819. If we divide this by 8 we get 102
        TC_GetStatus(TC1, 0);
        dacc_write_conversion_data(DACC_INTERFACE, i << 3);
        //analogWrite(DAC1, waveformTriangle[i]);
        //analogWrite(DAC1, waveformsTable[wave0][i]);

        //sweep 1: 0 to 62
        if (i == 612) {
            i = 550;
        }
        i++;
        //102*10 kHz = 102000
        //TIMER_CLOCK2 = MCK /8 = 10500000
       
        //i &= ~(1<<8); 
        //digitalWrite(13, l = !l);
}

void startTimer(Tc *tc, uint32_t channel, IRQn_Type irq, uint32_t frequency) {
        pmc_set_writeprotect(false);
        pmc_enable_periph_clk((uint32_t)irq);
        TC_Configure(tc, channel, TC_CMR_WAVE | TC_CMR_WAVSEL_UP_RC | TC_CMR_TCCLKS_TIMER_CLOCK3);
        uint32_t rc = VARIANT_MCK/32/frequency; //128 because we selected TIMER_CLOCK4 above
        TC_SetRA(tc, channel, rc/2); //50% high, 50% low
        TC_SetRC(tc, channel, rc);
        TC_Start(tc, channel);
        tc->TC_CHANNEL[channel].TC_IER=TC_IER_CPCS;
        tc->TC_CHANNEL[channel].TC_IDR=~TC_IER_CPCS;
        NVIC_EnableIRQ(irq);
        timerOn = true;
}


void stopTimer(Tc *tc, uint32_t channel, IRQn_Type irq) {
  NVIC_DisableIRQ(irq);
  TC_Stop(tc, channel);
  timerOn = false;
}


void setup() {
  Serial.begin(9600);

  timerOn = false;
  
  Ethernet.begin(mac, ip);
  comm._Udp.begin(localport);
  
  analogWriteResolution(12);  // set the analog output resolution to 12 bit (4096 levels)
  //Serial.begin(9600);
  //Serial.print(VARIANT_MCK);

  analogWrite(DAC0, 3727); 
  //analogWrite(DAC0, 0); 
  analogWrite(DAC1, 0);

  //frequency is samples * frequency, for example 102 * 10kHz = 1020000, max value is 1280000
  //TC1 channel 0, the IRQ for that channel and the desired frequency
  //600000 is the maximum frequency to allow for anything to processed in the loop.
  startTimer(TC1, 0, TC3_IRQn, 600000); 
  //delay(2000);
  //stopTimer(TC1, 0, TC3_IRQn);
  Serial.print("IP: ");
  Serial.print(Ethernet.localIP());
  
  Serial.println("Setup complete");
}


void loop() {
    //Serial.println("Hello");
  comm.processEthernetRequest(&frequency, &dac0, &dac1);
  //Serial.println("Eth processed");

  if (!timerOn) {
    //Serial.println("DAC0: " + String(dac0) + " ");
    //Serial.println("DAC1: " + String(dac1) + " ");
    analogWrite(DAC0, dac0);
    analogWrite(DAC1, dac1);
  }
  //delay(500);
}
