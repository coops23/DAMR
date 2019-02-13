#include <Wire.h>

#define SLAVE_ADDRESS (0x8)

int x = 0;

void setup() {
  Wire.begin();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void SlaveCommand()
{
  Wire.beginTransmission(SLAVE_ADDRESS); // transmit to device #8
  Wire.write("x is ");        // sends five bytes
  Wire.write(x);              // sends one byte
  Wire.endTransmission();    // stop transmitting

  x++;
  delay(500);
}

