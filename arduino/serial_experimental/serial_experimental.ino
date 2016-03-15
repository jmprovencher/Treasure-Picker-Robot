#include <PID_v1.h>
#include <LiquidCrystal.h>
#include <PololuMaestro.h>


// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0;
// value that allows a simple switch case
boolean mode = false;
// string used to print on the serial
String action = "";

int pinsDrive[6] = {3, 6, 7, 8, 9, 10};
int pinsRead[4] = {18, 19, 20, 21};
int pinPrehenseur = 4;
int pinElectroAimant = 5;
int spdWheels[2] = {255, 0};
unsigned long spdBuffer = 0;
int duration = 0;

double Setpoint[4] = {3000, 3000, 3000, 3000};
double Input[4] = {3000, 3000, 3000, 3000};
double Output[4];
MicroMaestro maestro(Serial1);
MicroMaestro prehenseurMaestro(Serial2);

PID firstPID(&Input[0], &Output[0], &Setpoint[0], 0.00005, 0.25, 0, REVERSE);
PID secondPID(&Input[1], &Output[1], &Setpoint[1], 0.000066, 0.30, 0, REVERSE);
PID thirdPID(&Input[2], &Output[2], &Setpoint[2], 0.00005, 0.2, 0, REVERSE);
PID fourthPID(&Input[3], &Output[3], &Setpoint[3], 0.00005, 0.2, 0, REVERSE);

PID pidList[4] = {firstPID, secondPID, thirdPID, fourthPID};

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  for(int i = 0; i < 6; i++){
    pinMode(pinsDrive[i], OUTPUT);
  }
  
  for(int i = 0; i < 4; i++){
    pinMode(pinsRead[i], INPUT);
    pidList[i].SetMode(AUTOMATIC);
    pidList[i].SetSampleTime(15);
  }
  attachInterrupt(digitalPinToInterrupt(18), decrementDuration, FALLING);
  attachInterrupt(digitalPinToInterrupt(20), decrementDuration, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(pinsDrive[4], spdWheels[0]);
  analogWrite(pinsDrive[5], spdWheels[1]);
  if(duration != 0){
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
  else{
    stopWheels();
  }
}

void decrementDuration(){
  duration--;
}

void stopWheels(){
  Setpoint[2] = 3000; Setpoint[3] = 3000; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
  for(int i = 4; i<6; i++){
      analogWrite(pinsDrive[i], 0);
  }
}

void serialEvent(){
    // read the incoming byte:
    incomingByte = Serial.read();
    Serial.write(incomingByte);
    
    if(!mode){
      duration = 0;
      if(incomingByte == 56){
        action = "Moving forward ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
        mode = true;
      }
      else if(incomingByte == 50){
        action = "Moving backwards ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000; spdWheels[0] = 0, spdWheels[1] = 255;
        mode = true;
      }
      else if(incomingByte == 52){
        action = "Moving left ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 255, spdWheels[1] = 0;
        mode = true;
      }
      else if(incomingByte == 54){
        action = "Moving right ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000; spdWheels[0] = 0, spdWheels[1] = 255;
        mode = true;
      }
      else if(incomingByte == 55){
        action = "Turning left ";
        Setpoint[2] = 800; Setpoint[3] = 3000; Setpoint[0] = 3000; Setpoint[1] = 800; spdWheels[0] = 255, spdWheels[1] = 0;
        mode = true;
      }
      else if(incomingByte == 57){
        action = "Turning right ";
        Setpoint[2] = 800; Setpoint[3] = 3000; Setpoint[0] = 3000; Setpoint[1] = 800; spdWheels[0] = 0, spdWheels[1] = 255;
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
      else if(incomingByte == 98){
        action = "Camera Left ";
        maestro.setTarget(0, 2400);
        maestro.setTarget(1, 6200);
      }
      else if(incomingByte == 97){
        action = "Camera Right ";
        maestro.setTarget(0, 9600);
        maestro.setTarget(1, 6200);
      }
      else if(incomingByte == 99){
        action = "Camera Front ";
        maestro.setTarget(0, 6000);
        maestro.setTarget(1,6200);
      }
      else if(incomingByte == 100){
        action = "Camera Treasure ";
        maestro.setTarget(0,6000);
        maestro.setTarget(1, 4044);
      }
      else{
        action = "Invalid action ";
        stopWheels();        
      }
    }
    else if(mode){
      duration = incomingByte;
      mode = false;
    }
}
