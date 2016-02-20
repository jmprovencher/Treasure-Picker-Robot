#include <PID_v1.h>
#include <LiquidCrystal.h>
#include <TimerOne.h>

// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0;
// value that allows a simple switch case
boolean mode = false;
// string used to print on the serial
String action = "";

int wheelPos[4] = {0, 0, 0, 0};

int pins[6] = {3, 4, 7, 8, 9, 10};
int spdWheels[7] = {0, 0, 0, 0, 255, 0};

double Setpoint[4], Input[4], Output[4];

PID firstPID(&Input[0], &Output[0], &Setpoint[0], 2, 5, 1, DIRECT);
PID secondPID(&Input[1], &Output[1], &Setpoint[1], 2, 5, 1, DIRECT);
PID thirdPID(&Input[2], &Output[2], &Setpoint[2], 2, 5, 1, DIRECT);
PID fourthPID(&Input[3], &Output[3], &Setpoint[3], 2, 5, 1, DIRECT);

void setup() {
  Serial.begin(115200);
  
  Timer1.initialize(150000);
  Timer1.attachInterrupt(blinkLED); // blinkLED to run every 0.15 seconds
  
  for(int i = 0; i < 6; i++){
     pinMode(pins[i], OUTPUT);
  }
  for(int i = 0; i < 4; i++){
     Input[i] = analogRead(i);
     Setpoint[i] = spdWheels[i];
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();
                
                if(!mode){
                  if(incomingByte == 56){
                    action = "Moving forward ";
                    spdWheels[0] = 122; spdWheels[1] = 122; spdWheels[2] = 0; spdWheels[3] = 0; spdWheels[4] = 255, spdWheels[5] = 0;
                  }
                  else if(incomingByte == 50){
                    action = "Moving backwards ";
                    spdWheels[0] = 122; spdWheels[1] = 122; spdWheels[2] = 0; spdWheels[3] = 0; spdWheels[4] = 0, spdWheels[5] = 255;
                  }
                  else if(incomingByte == 52){
                    action = "Turning left ";
                    spdWheels[2] = 122; spdWheels[3] = 122; spdWheels[0] = 0; spdWheels[1] = 0; spdWheels[4] = 0, spdWheels[5] = 255;
                  }
                  else if(incomingByte == 54){
                    action = "Turning right ";
                    spdWheels[2] = 122; spdWheels[3] = 122; spdWheels[0] = 0; spdWheels[1] = 0; spdWheels[4] = 255, spdWheels[5] = 0;
                  }
                  else{
                    action = "Invalid action ";
                  }
                  delay(10);
                  mode = !mode;
                }
                else if(mode){
                  for(int i = 0; i < incomingByte; i++){
                    for(int i = 0; i<6; i++){
                      analogWrite(pins[i], spdWheels[i]);
                    }
                    if(Serial.available() > 0){
                      mode = !mode;
                      break;
                    }
                    Serial.print(action);
                    Serial.println(incomingByte - i, DEC);
                    delay(10);
                  }
                  mode = !mode;
                }
        }
}
