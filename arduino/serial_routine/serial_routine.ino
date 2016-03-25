#include <PID_v1.h>
#include <LiquidCrystal.h>
#include <PololuMaestro.h>


// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0;
// value that allows a simple switch case
boolean mode = false;
// value that indicates rotation
boolean rotation = false;
// string used to print on the serial
String action = "";

const int pinsDrive[4] = {3, 6, 7, 8};
const int pinsDirection[8] = {32, 34, 36, 38, 40, 42, 46, 48};
const int pinsRead[4] = {19, 21, 17, 20};
const int pinElectroAimant = 5;
int spdWheels[8] = {0, 0, 0, 0, 0, 0, 0, 0};

unsigned long spdBuffer = 0;
int duration = 0;

const int straightAhead[8] = {255, 0, 0, 255, 0, 0, 0, 0};
const int backwardsMov[8] = {0, 255, 255, 0, 0, 0, 0, 0};
const int straightLeft[8] = {255, 0, 0, 255, 255, 0, 0, 255};
const int straightRight[8] = {255, 0, 0, 255, 0, 255, 255, 0};
const int turnLeft[8] = {255, 0, 255, 0, 255, 0, 255, 0};
const int turnRight[8] = {0, 255, 0, 255, 0, 255, 0, 255};
const int interruptWheels[8] = {0, 0, 0, 0, 0, 0, 0, 0};

double Setpoint[4] = {3000, 3000, 3000, 3000};
double Input[4] = {3000, 3000, 3000, 3000};
double Output[4];

MicroMaestro maestro(Serial2);
MicroMaestro prehenseurMaestro(Serial3);

PID firstPID(&Input[0], &Output[0], &Setpoint[0], 0.00006, 0.2, 0, REVERSE);
PID secondPID(&Input[1], &Output[1], &Setpoint[1], 0.00006, 0.225, 0, REVERSE);
PID thirdPID(&Input[2], &Output[2], &Setpoint[2], 0.0001, 0.25, 0, REVERSE);
PID fourthPID(&Input[3], &Output[3], &Setpoint[3], 0.000055, 0.16, 0, REVERSE);

PID pidList[4] = {firstPID, secondPID, thirdPID, fourthPID};

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600);
  for(int i = 0; i < 4; i++){
    pinMode(pinsDrive[i], OUTPUT);
  }
  for(int i = 0; i < 8; i++){
    pinMode(pinsDirection[i], OUTPUT);
  }
  for(int i = 0; i < 4; i++){
    pinMode(pinsRead[i], INPUT);
    pidList[i].SetMode(AUTOMATIC);
    pidList[i].SetOutputLimits(0, 120);
    pidList[i].SetSampleTime(15);
  }
  attachInterrupt(digitalPinToInterrupt(20), decrementDuration, FALLING);
  attachInterrupt(digitalPinToInterrupt(21), decrementDuration, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < 8; i++){
    if(spdWheels[i] == 0){
      digitalWrite(pinsDirection[i], LOW);
    }
    else{
      digitalWrite(pinsDirection[i], HIGH);
    }
  }
  if(duration > 1){
    for(int j = 0; j<4; j++){
      spdBuffer = pulseIn(pinsRead[j], HIGH, 3000);
      if(spdBuffer == 0){
        spdBuffer = 3000;
      }
      Input[j] = (spdBuffer);
      pidList[j].Compute();
      //Serial.print(Input[j]);
      //Serial.print(" - ");
      //Serial.print(Setpoint[j]);
      //Serial.print(" - ");
      //Serial.print(Output[j]);
      //Serial.print(";");
    }
    //Serial.println(".");
    //Serial.print(action);
      for(int j = 0; j<4; j++){
      if(Setpoint[j] != 3000){
        analogWrite(pinsDrive[j], Output[j]);
      }
      else{
        analogWrite(pinsDrive[j], 0);
      }
    }
    //Serial.println(incomingByte - i, DEC);
    delay(20);
  }
  else if(duration == 1){
    duration = 0;
    stopWheels();
    //Serial.print(1);
  }
}

void decrementDuration(){
  if(duration > 1){
    duration--;
  }
}

void stopWheels(){
  Setpoint[2] = 3000; Setpoint[3] = 3000; Setpoint[0] = 3000; Setpoint[1] = 3000;
  for(int i = 0; i<8; i++){
      spdWheels[i] = interruptWheels[i];
      analogWrite(pinsDirection[i], 0);
  }
}

void serialEvent(){
    // read the incoming byte:
    incomingByte = Serial.read();
    
    if(!mode){
      duration = 0;
      if(incomingByte == 56){
        action = "Moving forward ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightAhead[i];
        }
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 50){
        action = "Moving backwards ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = backwardsMov[i];
        }
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 52){
        action = "Moving left ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightLeft[i];
        }
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 54){
        action = "Moving right ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightRight[i];
        }
        rotation = false;
        mode = true;
        
      }
      else if(incomingByte == 55){
        action = "Turning left ";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 1200; Setpoint[1] = 1200;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnLeft[i];
        }
        rotation = true;
        mode = true;
      }
      else if(incomingByte == 57){
        action = "Turning right ";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 1200; Setpoint[1] = 1200;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnRight[i];
        }
        rotation = true;
        mode = true;
      } 
      else if(incomingByte == 93){
        action = "Activate Magnet";
        analogWrite(pinElectroAimant, 255);
      }
      else if(incomingByte == 94){
        action = "Deactivate Magnet";
        analogWrite(pinElectroAimant, 0);
      }
      else if(incomingByte == 95){
        action = "Prehenseur down";
        prehenseurMaestro.setTarget(0, 6000);
        prehenseurMaestro.setTarget(1, 6200);
      }
      else if(incomingByte == 96){
        action = "Prehenseur up ";
        prehenseurMaestro.setTarget(0, 6000);
        prehenseurMaestro.setTarget(1, 4044);
      }
      else if(incomingByte == 97){
        action = "Camera Left ";
        maestro.setTarget(1, 2400);
        maestro.setTarget(2, 6200);
      }
      else if(incomingByte == 98){
        action = "Camera Right ";
        maestro.setTarget(1, 9600);
        maestro.setTarget(2, 6200);
      }
      else if(incomingByte == 99){
        action = "Camera Front ";
        maestro.setTarget(1, 6000);
        maestro.setTarget(2,6200);
      }
      else if(incomingByte == 100){
        action = "Camera Treasure ";
        maestro.setTarget(1,6000);
        maestro.setTarget(2, 4044);
      }
      else{
        action = "Invalid action ";
        stopWheels();        
      }
    }
    else if(mode){
      for(int i = 0; i < 4; i++){
        Output[i] = 0;
      }
      if(rotation == false){
        duration = incomingByte*52;
      }
      else{
        duration = incomingByte*107;
      }
      mode = false;
    }
}
