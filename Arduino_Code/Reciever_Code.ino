/*
Date: 7/9/2012
Author: David Beath
Project: Player Tracking Project

Purpose: The code for the base stations. Waits for packets from 
any sending XBees. Upon recieving a packet, it will read the recieved 
signal strength (RSSI) of the packet, and the serial address of the 
XBee the packet was sent from. 
It then acts as a server that will send this data to any connected 
clients, along with the unique ID of the base station.

*/

#include <Ethernet.h>
#include <XBee.h>
#include <SPI.h>

//--------------------------------------------------------------------

// The below three values must be unique to each base station.

// The unique MAC address of the base station.
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA };

// The IP address of the base station.
IPAddress ip(192, 168, 1, 5);

//The unique ID of the base station.
int stationID = 0;

//--------------------------------------------------------------------

// Initialises the server and the port it sends on.
EthernetServer server(84);

// Initialises the XBee.
XBee xbee = XBee();

// Initialises the response packets.
Rx16Response rx16 = Rx16Response();

void setup() 
{
  //Initialises the Ethernet connection and server.
  Ethernet.begin(mac,ip);
  server.begin();

  Serial.begin(9600);
  xbee.begin(9600);
}

void loop()
{
  packetRead();
}

// Reads any incoming packets.
void packetRead()
{
  // Waits for an incoming packet.
  xbee.readPacket(20);
  if (xbee.getResponse().isAvailable())
  {
    // Checks if the packet is the right type.
    if (xbee.getResponse().getApiId() == RX_16_RESPONSE)
    {
      // Reads the packet.
      xbee.getResponse().getRx16Response(rx16);
      
      // Prints the data to the connected client.
      dataPrint();
    }  
    else 
    {
      Serial.println("Wrong Api");
    } 
  }
  else if (xbee.getResponse().isError())
  {
    Serial.println("No Packet");
    Serial.println(xbee.getResponse().getErrorCode());
  } 
}

// Gets the data from the packet and sends it to the client. 
void dataPrint()
{
  // Initialises the client connection.  
  EthernetClient client = server.available();
  if (client) 
  {
    while (client.connected())
    {
      if (client.available())
      {
        // Prints the RSSI value to the client.
        client.print(rx16.getRssi());
        
        client.print(",");
        
        // Prints the data from the packet to the client.    
        for(int i = 0; i < rx16.getDataLength(); i++)
        {
          //Serial.print(rx16.getData(i),HEX);
          client.print(rx16.getData(i),HEX);
        }
            
        client.print(",");
        
        // Prints the unique ID of the base station to the client.
        client.print(stationID);
        
        // Tells the client that the message has ended.    
        client.println("\r\n");
      }
      break;
    }
    delay(1);
    //client.stop();  
  }
}
