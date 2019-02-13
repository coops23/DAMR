#include <Servo.h>
#include <Wire.h>
#include <HMC5883L.h>

#define PWMB (6)
#define PWMA (3)
#define AIN1 (7)
#define AIN2 (8)
#define BIN1 (4)
#define BIN2 (5)

#define SERVO_BOT (11)

#define ENCODER_LEFT (2) //place holder, acts as Interrupt 0 for arduino uno
#define ENCODER_RIGHT (10) //place holder, acts as Interrupt 1 for arduino uno

#define DISTANCE_SENSOR_ECHO (12)
#define DISTANCE_SENSOR_TRIGGER (13)

//A5 and A4 are being used by the 3-axis digital compass.

#define FORWARD (0)
#define BACKWARD (1)
#define LEFT (2)
#define RIGHT (3)
#define STOP (4)

#define COMPASS_SCALE (1.8)
#define COMPASS_SAMPLE_COUNT (5)
#define COMPASS_ACCURACY_MARGIN (2)

void init();
void parseCommand(String message);
void executeCommand(unsigned int opcode, unsigned int value, unsigned int* response);
void motor(int choice, int value);
unsigned int distance();
void heading(float* currentHeading, float* changeHeading);

Servo servoBot;
Servo servoTop;

HMC5883L compass;

String inputString = "";  
boolean stringComplete = false;

volatile static byte oldPins = 0;
volatile unsigned int left = 0;
volatile unsigned int right = 0;

int error = 0;

void setup()
{
    int error;
    
    Serial.begin(9600);
    inputString.reserve(200);
    
    Wire.begin(); // Start the I2C interface.
    error = compass.setScale(COMPASS_SCALE); // Set the scale of the compass.
    if(error != 0) // If there is an error, print it out.
      //Serial.println(compass.getErrorText(error));
    error = compass.setMeasurementMode(MEASUREMENT_CONTINUOUS); // Set the measurement mode to Continuous
    if(error != 0) // If there is an error, print it out.
      //Serial.println(compass.getErrorText(error));
    pinMode(DISTANCE_SENSOR_TRIGGER, OUTPUT);
    pinMode(DISTANCE_SENSOR_ECHO, INPUT);
    
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    servoBot.attach(SERVO_BOT);
    
    //Endable Interrupts for PCIE2 Arduino Pins (D0-7)
    PCICR |= (1<<PCIE2);
    
    //Setup pins 2,3
    //PCMSK2 |= (1<<PCINT18); broke encoder :(
    PCMSK2 |= (1<<PCINT19); 
  
    //Trigger Interrupt on rising edge
    MCUCR = (1<<ISC01) | (1<<ISC01);
    
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, HIGH);
    analogWrite(PWMA, 150);
    analogWrite(PWMB, 150);
    servoBot.write(96);
    
    delay(1000);
}

void loop()
{
    float dir, last;
    
    if (stringComplete) {
        parseCommand(inputString); 
        // clear the string:
        inputString = "";
        stringComplete = false;
    }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}

void parseCommand(String message)
{
    char msg[256];
    unsigned int command = 0;
    unsigned int opcode = 0; 
    unsigned int value = 0; 
    unsigned int response = 0;
   
    message.toCharArray(msg, sizeof(msg));
    command = atoi(msg);
    opcode = command & 0x000F;
    value = (command & 0xFFF0) >> 4;
  
    executeCommand(opcode, value, &response);
    Serial.println(response);
}

void executeCommand(unsigned int opcode, unsigned int value, unsigned int* response)
{
    float angleChange = 0, angle = 0;
    
    switch(opcode)
    {
        case 0:
            servoBot.write(value);
            *response = 1;
            break;
        case 1:
            *response = 0;
            break;
        case 2:
            *response += (servoBot.read() << 4);
            *response += 1;
            break;
        case 3:
            *response += 0;
            break;
        case 4:
            motor(FORWARD, value);
            *response = 1;
            break;
        case 5:
            motor(BACKWARD, value);
            *response = 1;
            break;
        case 6:
            motor(LEFT, value);
            *response = 1;
            break;
        case 7:
            motor(RIGHT, value);
            *response = 1;
            break;
        case 8:
            motor(STOP, 0);
            *response = 1;
            break;
        case 9:
            heading(&angle, &angleChange);
            *response = (((unsigned)angle) << 4);
            *response += 1;
            break;
        case 10:
            *response = (distance() << 4);
            *response += 1;
            break;
        default:
            *response = 0;
            break; 
    }
}

void motor(int choice, int value)
{
    float angleChange = 0, angle, desiredHeading = 0;
    left = right = 0;
    
    switch(choice)
    {
        case FORWARD:
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, HIGH);
            digitalWrite(BIN1, LOW);
            digitalWrite(BIN2, HIGH);
            while(left < value);
            break;
        case BACKWARD:
            digitalWrite(AIN1, HIGH);
            digitalWrite(AIN2, LOW);
            digitalWrite(BIN1, HIGH);
            digitalWrite(BIN2, LOW);
            while(left < value); 
            break;
        case LEFT:
            heading(&angle, &angleChange);
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, HIGH);
            digitalWrite(BIN1, HIGH);
            digitalWrite(BIN2, LOW); 
            desiredHeading = angle + value;
            desiredHeading = ((int)desiredHeading + 360) % 360;    
            while((angle > (desiredHeading + COMPASS_ACCURACY_MARGIN)) || (angle < (desiredHeading - COMPASS_ACCURACY_MARGIN))){     
                heading(&angle, &angleChange);
            }
            break;
        case RIGHT:
            heading(&angle, &angleChange);
            digitalWrite(AIN1, HIGH);
            digitalWrite(AIN2, LOW);
            digitalWrite(BIN1, LOW);
            digitalWrite(BIN2, HIGH);
            desiredHeading = angle - value;
            desiredHeading = ((int)desiredHeading + 360) % 360;    
            while((angle > (desiredHeading + COMPASS_ACCURACY_MARGIN)) || (angle < (desiredHeading - COMPASS_ACCURACY_MARGIN))){     
                heading(&angle, &angleChange);
            }
            break;
        case STOP:
           digitalWrite(AIN1, HIGH);
           digitalWrite(AIN2, HIGH);
           digitalWrite(BIN1, HIGH);
           digitalWrite(BIN2, HIGH);
        default:
            break;
    } 
     
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, HIGH);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, HIGH);
}

ISR( PCINT2_vect ) {
  //Read values from digital pins 2 to 7
  const byte actPins = PIND;
  //Match this values agaist the oldPins bitmask (XOR and AND for raising edge)
  const byte setPins = (oldPins ^ actPins) & actPins;

  if (setPins & 0b00000100)
      left++;
 
  oldPins = actPins;
}

unsigned int distance()
{
    long duration, distance;
    
    digitalWrite(DISTANCE_SENSOR_TRIGGER, LOW);  // Added this line
    delayMicroseconds(2); // Added this line
    digitalWrite(DISTANCE_SENSOR_TRIGGER, HIGH);
    //  delayMicroseconds(1000); - Removed this line
    delayMicroseconds(10); // Added this line
    digitalWrite(DISTANCE_SENSOR_TRIGGER, LOW);
    duration = pulseIn(DISTANCE_SENSOR_ECHO, HIGH);
    distance = (duration/2) / 29.1;
    distance *= 10;
    distance = constrain(distance, 0, 4000);
    return (unsigned int) distance;
}
   
void heading(float* currentHeading, float* changeHeading)
{
    int i = 0; 
    float heading = 0;
    
    MagnetometerScaled scaled = compass.readScaledAxis();
    
    heading = atan2(scaled.YAxis, scaled.ZAxis);
    heading += 0.29174923776; //declination angle
    
    if(heading < 0)
        heading += 2*PI;
    
    if(heading > 2*PI)
        heading -= 2*PI;
    
    heading *= (180/M_PI);    
    
    delay(10);
 
    *currentHeading = heading;     
}
    
