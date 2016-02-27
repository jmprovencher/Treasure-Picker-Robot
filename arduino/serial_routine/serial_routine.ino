#include <PID_v1.h>
#include <LiquidCrystal.h>



// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0;
// value that allows a simple switch case
boolean mode = false;
// string used to print on the serial
String action = "";

int pinsDrive[6] = {3, 6, 7, 8, 9, 10};
int pinsRead[4] = {14, 15, 16, 17};
int spdWheels[2] = {255, 0};
unsigned long spdBuffer = 0;
int duration = 0;

double Setpoint[4] = {3000, 3000, 3000, 3000};
double Input[4] = {3000, 3000, 3000, 3000};
double Output[4];

PID firstPID(&Input[0], &Output[0], &Setpoint[0], 1, 2, 0.2, REVERSE);
PID secondPID(&Input[1], &Output[1], &Setpoint[1], 1, 2, 0.2, REVERSE);
PID thirdPID(&Input[2], &Output[2], &Setpoint[2], 1, 2, 0.2, REVERSE);
PID fourthPID(&Input[3], &Output[3], &Setpoint[3], 1, 2, 0.2, REVERSE);

PID pidList[4] = {firstPID, secondPID, thirdPID, fourthPID};

void setup() {
  Serial.begin(115200);
  
  for(int i = 0; i < 6; i++){
    pinMode(pinsDrive[i], OUTPUT);
  }
  
  for(int i = 0; i < 4; i++){
    pinMode(pinsRead[i], INPUT);
    pidList[i].SetMode(AUTOMATIC);
    pidList[i].SetSampleTime(15);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(duration != 0){
    analogWrite(pinsDrive[4], spdWheels[0]);
    analogWrite(pinsDrive[5], spdWheels[1]);
    for(int i = 0; i < duration; i++){
      for(int j = 0; j<4; j++){
        spdBuffer = pulseIn(pinsRead[j], HIGH, 3000);
        if(spdBuffer == 0){
          spdBuffer = 3000;
        }
        Input[j] = (spdBuffer);
        pidList[j].Compute();
        Serial.print(Input[j]);
        Serial.print(" - ");
        Serial.print(Output[j]);
        Serial.print(";");
      }
      Serial.println(".");
      Serial.print(action);
      for(int j = 0; j<4; j++){
        analogWrite(pinsDrive[j], Output[j]); 
      }
      Serial.println(incomingByte - i, DEC);
      delay(20);
    }
    for(int i = 0; i<4; i++){
      Setpoint[i] = 3000;
    }
    for(int i = 4; i<6; i++){
        analogWrite(pinsDrive[i], 0);
    }
    duration = 0;
  }
}

void serialEvent(){
    // read the incoming byte:
    incomingByte = Serial.read();
    
    if(!mode){
      duration = 0;
      if(incomingByte == 56){
        action = "Moving forward ";
        Setpoint[0] = 600; Setpoint[1] = 600; Setpoint[2] = 3000; Setpoint[3] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
      }
      else if(incomingByte == 50){
        action = "Moving backwards ";
        Setpoint[0] = 600; Setpoint[1] = 600; Setpoint[2] = 3000; Setpoint[3] = 3000; spdWheels[0] = 0, spdWheels[1] = 255;
      }
      else if(incomingByte == 52){
        action = "Turning left ";
        Setpoint[2] = 600; Setpoint[3] = 600; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
      }
      else if(incomingByte == 54){
        action = "Turning right ";
        Setpoint[2] = 600; Setpoint[3] = 600; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 0, spdWheels[1] = 255;
      }
      else{
        action = "Invalid action ";        
        Setpoint[2] = 3000; Setpoint[3] = 3000; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
      }
      mode = true;
    }
    else if(mode){
      duration = incomingByte;
      mode = false;
    }
}
