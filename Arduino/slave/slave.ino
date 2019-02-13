#include <Wire.h>

/*
The purposes of the slave uc is to take the load
off the master uc and deal with position control 
of the wheel. This requires up to four interrupts 
occuring at the slot detectors while ensuring that 
each wheel has moved the same distance to ensure 
the car is straight at the end of a move command.
 */

#define SLAVE_ADDRESS (0x8)
#define MOVEMENT_SPEED (125)

#define WHEEL_LEFT_PLUS   (9)
#define WHEEL_LEFT_MINUS  (10)
#define WHEEL_LEFT_INTERRUPT (2)

#define WHEEL_RIGHT_PLUS   (5)
#define WHEEL_RIGHT_MINUS  (6)
#define WHEEL_RIGHT_INTERRUPT (3)

volatile int leftTicks = 0;
volatile int rightTicks = 0;

void setup() {
  pinMode(WHEEL_LEFT_PLUS, OUTPUT);
  pinMode(WHEEL_LEFT_MINUS, OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(WHEEL_LEFT_INTERRUPT), LeftSlotDetector, CHANGE);
  attachInterrupt(digitalPinToInterrupt(WHEEL_RIGHT_INTERRUPT), RightSlotDetector, CHANGE);
  
  analogWrite(WHEEL_LEFT_PLUS, 0);
  analogWrite(WHEEL_LEFT_MINUS, 0);

  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(ReceiveEvent);
}

void loop() {
  
}

void LeftSlotDetector()
{
  leftTicks++;
}

void RightSlotDetector()
{
  rightTicks++;
}

void ReceiveEvent(int byteReceiveCount)
{
  String message = "";
  int count = 0;
  
  while(1 < Wire.available())
  {
    char c = Wire.read();

    message += c;
    count++;
  }

  for(int i = 0; i < count; i++)
  {
    Wire.write(message[i]);
  }
}


