/*
Date: 13/7/2012
Author: David Beath
Project: Player Tracking Project

Purpose: The code for the player tags. On powerup reads the Serial Low
address of the attached XBee and saves it to the payload. The XBee then
Broadcasts this payload to all listening devices every 10 milliseconds.

*/

#include <XBee.h>

// Initialises the XBee.
XBee xbee = XBee();

// Sets the size of the payload.
uint8_t payload[4];

// Sets the command to get the Serial Low Address.
uint8_t slCmd[] = {'S','L'};

// Sets the command to exit AT mode. 
uint8_t cnCmd[] = {'C','N'};

// Initialises the AT Request and Response.
AtCommandRequest atRequest = AtCommandRequest();
AtCommandResponse atResponse = AtCommandResponse();

void setup()
{
  Serial.begin(9600); 
  xbee.begin(9600);
  
  // Reads the Serial Address of the XBee.
  addressRead();   
}

// Sends a broadcast packet every 10 milliseconds.
void loop()
{       
    packetSend();
    
    delay(10);
}

// Sends the packet over the XBee port.
void packetSend()
{ 
  // Sets the destination, payload, and size of the packet.
  Tx16Request tx = Tx16Request(0xFFFF, payload, sizeof(payload));
  
  xbee.send(tx);
}

// Reads the Serial Low Address of the XBee and adds it to the payload.
void addressRead()
{
  // Sets the AT Command to Serial Low Read.
  atRequest.setCommand(slCmd);
  
  // Sends the AT Command.
  xbee.send(atRequest);
  
  // Waits for a response and checks for the correct response code.
  if (xbee.readPacket(1000))
  {  
    if(xbee.getResponse().getApiId() == AT_COMMAND_RESPONSE)
    {
      xbee.getResponse().getAtCommandResponse(atResponse);
      
      if(atResponse.isOk())
      {
        // Reads the entire response and adds it to the payload.
        for (int i = 0; i < atResponse.getValueLength(); i++)
        {
          payload[i] = (atResponse.getValue()[i]);
          Serial.print(payload[i],HEX);
          Serial.print(" ");
        }
      }
      Serial.println(sizeof(payload));
    }
  }
  
  // Sets the AT Command to the Close Command.
  atRequest.setCommand(cnCmd);
  xbee.send(atRequest);
  
  // Wait two seconds.
  delay(2000);     
}
