#include <TimerOne.h>
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

const int pinClock = 3;
const int pinManchester = 50;
const int pinsDrive[4] = {6, 7, 8, 9};
const int pinsDirection[8] = {32, 34, 36, 38, 40, 42, 46, 48};
const int pinsRead[4] = {19, 21, 17, 20};
const int pinElectroAimant = 5;
const int pinPontDiodes = 22;
const int pinActiveAimant = 24;
int positionCamera = 6400;
int spdWheels[8] = {0, 0, 0, 0, 0, 0, 0, 0};

String manchesterCode = "";

bool stateClock = 0;
bool stateManchester = 0;
bool bitDecode = 0;
bool complete = false;
bool slow = false;
bool readyToBegin = false;
int compteur = 0;
int nombreDeSuite = 1;

int arrayCode[32] = {0};
int arrayBigReset[32] = {0};
int arrayDecode[7] = {0};
int arraySmallReset[7] = {0};
char arrayManchester[4] = {0};

int codeSecret = 0;
unsigned int count = 0;
unsigned int countLoop = 0;


// string used to signal a completed command
String commandComplete = String("done");

unsigned long spdBuffer = 0;
int duration = 0;

const int straightAhead[8] = {255, 0, 0, 255, 0, 255, 0, 255};
const int backwardsMov[8] = {0, 255, 255, 0, 0, 255, 0, 255};
const int straightLeft[8] = {255, 0, 0, 255, 255, 0, 0, 255};
const int straightRight[8] = {255, 0, 0, 255, 0, 255, 255, 0};
const int turnLeft[8] = {255, 0, 255, 0, 255, 0, 255, 0};
const int turnRight[8] = {0, 255, 0, 255, 0, 255, 0, 255};
const int interruptWheels[8] = {0, 0, 0, 0, 0, 0, 0, 0};

double Setpoint[4] = {3000, 3000, 3000, 3000};
double Input[4] = {3000, 3000, 3000, 3000};
double Output[4];

MicroMaestro maestro(Serial2);

PID firstPID(&Input[0], &Output[0], &Setpoint[0], 0.00006, 0.2, 0, REVERSE);
PID secondPID(&Input[1], &Output[1], &Setpoint[1], 0.00006, 0.225, 0, REVERSE);
PID thirdPID(&Input[2], &Output[2], &Setpoint[2], 0.0001, 0.25, 0, REVERSE);
PID fourthPID(&Input[3], &Output[3], &Setpoint[3], 0.000055, 0.16, 0, REVERSE);

PID pidList[4] = {firstPID, secondPID, thirdPID, fourthPID};

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600);
  TCCR3B = TCCR3B & 0b11111000 | 0x04;

  Timer1.initialize(2000000);

  pinMode(pinClock, INPUT);
  pinMode(pinManchester, INPUT);
  
  for(int i = 0; i < 4; i++){
    pinMode(pinsDrive[i], OUTPUT);
  }
  for(int i = 0; i < 8; i++){
    pinMode(pinsDirection[i], OUTPUT);
  }
  pinMode(pinElectroAimant, OUTPUT);
  pinMode(pinPontDiodes, OUTPUT);
  pinMode(pinActiveAimant, OUTPUT);
  
  for(int i = 0; i < 4; i++){
    pinMode(pinsRead[i], INPUT);
    pidList[i].SetMode(AUTOMATIC);
    pidList[i].SetOutputLimits(0, 120);
    pidList[i].SetSampleTime(15);
  }
  
  analogWrite(pinElectroAimant, 166);
  
  attachInterrupt(digitalPinToInterrupt(20), decrementDuration, FALLING);
  attachInterrupt(digitalPinToInterrupt(21), decrementDuration, FALLING);
  
  maestro.setSpeed(3, 12);
  maestro.setAcceleration(3, 120);
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
    //Serial.print(action);
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
    writeString(commandComplete);
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

float readCapacitorVoltage(){
  int capacitorVoltageValue = analogRead(A0);
  float capacitorVoltage = capacitorVoltageValue * (5.0 / 1023.0);
  return capacitorVoltage;
}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()

  for (int i = 0; i < stringData.length(); i++)
  {
      Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }

}// end writeString

void serialEvent(){
    // read the incoming byte:
    if(readyToBegin == false){
      Timer1.restart();
      readyToBegin == true;
      Timer1.attachInterrupt(readCapacitor); // readCapacitor runs every second
    }
    Timer1.detachInterrupt();
    incomingByte = Serial.read();
    
    if(!mode){
      duration = 0;
      if(incomingByte == 122){
        stopWheels();
        manchesterRead();
      }
      else if(incomingByte == 73){
        action = "Moving forward slowly ";
        Setpoint[0] = 1400; Setpoint[1] = 1400; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightAhead[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 56){
        action = "Moving forward ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightAhead[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 75){
        action = "Moving backwards slowly ";
        Setpoint[0] = 1400; Setpoint[1] = 1400; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = backwardsMov[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 50){
        action = "Moving backwards ";
        Setpoint[0] = 800; Setpoint[1] = 800; Setpoint[2] = 3000; Setpoint[3] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = backwardsMov[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 49){
        action = "Moving left slowly";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightLeft[i];
        }
        slow = true;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 52){
        action = "Moving left ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightLeft[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 51){
        action = "Moving right slowly";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightRight[i];
        }
        slow = true;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 54){
        action = "Moving right ";
        Setpoint[2] = 800; Setpoint[3] = 800; Setpoint[0] = 3000; Setpoint[1] = 3000;
        for(int i = 0; i<8; i++){
          spdWheels[i] = straightRight[i];
        }
        slow = false;
        rotation = false;
        mode = true;
      }
      else if(incomingByte == 74){
        action = "Turning left slowly";
        Setpoint[2] = 1500; Setpoint[3] = 1500; Setpoint[0] = 1500; Setpoint[1] = 1500;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnLeft[i];
        }
        slow = false;
        rotation = true;
        mode = true;
      }
      else if(incomingByte == 55){
        action = "Turning left ";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 1200; Setpoint[1] = 1200;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnLeft[i];
        }
        slow = false;
        rotation = true;
        mode = true;
      }
      else if(incomingByte == 76){
        action = "Turning right slowly";
        Setpoint[2] = 1500; Setpoint[3] = 1500; Setpoint[0] = 1500; Setpoint[1] = 1500;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnRight[i];
        }
        slow = false;
        rotation = true;
        mode = true;
      }
      else if(incomingByte == 57){
        action = "Turning right ";
        Setpoint[2] = 1200; Setpoint[3] = 1200; Setpoint[0] = 1200; Setpoint[1] = 1200;
        for(int i = 0; i<8; i++){
          spdWheels[i] = turnRight[i];
        }
        slow = false;
        rotation = true;
        mode = true;
      }
      else if(incomingByte == 101){
        action = "Charging Capacitor";
        digitalWrite(pinPontDiodes, HIGH);
        writeString(commandComplete);
      }
      else if(incomingByte == 102){
        action = "Stop charging";
        digitalWrite(pinPontDiodes, LOW);
        writeString(commandComplete);
      }
      else if(incomingByte == 103){
        action = "Activate Magnet";
        analogWrite(pinElectroAimant, 180);
        digitalWrite(pinActiveAimant, HIGH);
        writeString(commandComplete);
      }
      else if(incomingByte == 104){
        action = "Deactivate Magnet";
        digitalWrite(pinActiveAimant, LOW);
        for(int i = 0; i++; i < 10){
          int myValue = 123.46*pow(2.718, -0.284*i);
          analogWrite(pinElectroAimant, myValue);
          delay(100);
        }
        writeString(commandComplete);
      }
      else if(incomingByte == 80){
        action = "Prehenseur down";
        maestro.setTarget(3, 9100);
        writeString(commandComplete);
      }
      else if(incomingByte == 81){
        action = "Prehenseur up ";
        maestro.setTarget(3, 2127);
        writeString(commandComplete);
      }
      else if(incomingByte == 82){
        action = "tite touche ";
        maestro.setTarget(3, 2127);
        delay(150);
        maestro.setTarget(3, 9100);
        delay(150);
        maestro.setTarget(3, 2127);
        delay(150);
        maestro.setTarget(3, 9100);
        delay(150);
        maestro.setTarget(3, 2127);
        writeString(commandComplete);
      }
      else if(incomingByte == 120){
        action = "Camera Depot ";
        maestro.setTarget(1,6000);
        maestro.setTarget(2, 4044);
        writeString(commandComplete);
      }
      else if(incomingByte == 97){
        action = "Camera Left ";
        maestro.setTarget(1, 2400);
        maestro.setTarget(2, 6200);
        writeString(commandComplete);
      }
      else if(incomingByte == 98){
        action = "Camera Right ";
        maestro.setTarget(1, 9600);
        maestro.setTarget(2, 6200);
        writeString(commandComplete);
      }
      else if(incomingByte == 99){
        action = "Camera Front ";
        maestro.setTarget(1, 6000);
        maestro.setTarget(2,6400);
        positionCamera = 6400;
        writeString(commandComplete);
      }
      else if(incomingByte == 100){
        action = "Camera Treasure ";
        maestro.setTarget(1, 6000);
        maestro.setTarget(2,5000);
        positionCamera = 5000;
        writeString(commandComplete);
      }
      else if(incomingByte == 121){
        action = "Touch and go ";
        positionCamera = positionCamera - 100;
        maestro.setTarget(2,positionCamera);
        writeString(commandComplete);
      }
      else{
        action = "Invalid action ";
        stopWheels();        
      }
    }
    else if(mode){
      for(int i = 0; i < 4; i++){
        pidList[i].SetOutputLimits(0, 1);
        pidList[i].SetOutputLimits(-1, 0);
        pidList[i].SetOutputLimits(0, 120);
      }
      for(int i = 0; i < 4; i++){
        Output[i] = 0;
      }
      if(rotation == false){
        if(slow == false){
          duration = incomingByte*60;
        }
        else{
          duration = incomingByte*6;
        }
      }
      else{
        duration = incomingByte*24;
      } 
      mode = false;
    }
  Timer1.restart();
  Timer1.attachInterrupt(readCapacitor);
}

void readCapacitor()
{
  writeString(String(readCapacitorVoltage()));
}

void Reading()
{
  readCapacitor();
  delay(10);
  if(digitalRead(pinClock) == HIGH){
    count++;
  }
}

void manchesterRead()
{
  action = "Reading Manchester";
  attachInterrupt(digitalPinToInterrupt(pinClock), Reading, RISING);
  while (complete == false){
    if (count != countLoop)
    {
      countLoop = count;
      stateClock = digitalRead(pinClock);
      stateManchester = digitalRead(pinManchester);
      bitDecode = stateClock ^ stateManchester;
      arrayCode[compteur] = bitDecode;
      compteur++;
    } 
    if (compteur == 32 && complete == false)
    {
      for (int i = 0; i < 32; i++)
      {
        if (arrayCode[i] == 1)
        {
          for (int j = i; j < i+8; j++)
          {
            if (arrayCode[j+1] == 1)
            {
              nombreDeSuite++;
              if (nombreDeSuite > 7 && arrayCode[j+2] == 0)
              {
                for (int k = 0; k < 7; k++)
                {
                  arrayDecode[k] = arrayCode[k + j + 3];
                }
                codeSecret = 0;
                for (int u=0; u<7; u++)
                {
                  codeSecret= codeSecret*2+arrayDecode[u];
                }
                memcpy(arrayCode, arrayBigReset, 32);
                memcpy(arrayDecode, arraySmallReset, 7);
                for(int k = 0; k < 4; k++){
                  arrayManchester[k] = char(codeSecret);
                }
                writeString(String(arrayManchester));
                complete = true;
                i = 32;
                break;
              }
            }
            else{
              nombreDeSuite = 1;
            }
          }
        }
      }
      compteur = 0;
    }
  }
  detachInterrupt(digitalPinToInterrupt(pinClock));
}
