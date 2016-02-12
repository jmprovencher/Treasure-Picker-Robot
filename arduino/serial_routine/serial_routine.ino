#include <LiquidCrystal.h>

// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0; 
boolean mode = false;
String action = "";
int pins[6] = {2, 3, 4, 7, 8, 9};
int spd[7] = {0, 0, 0, 0, 255, 0};

void setup() {
  // put your setup code here, to run once:
   Serial.begin(115200);
   for(int i = 0; i < 6; i++){
      pinMode(pins[i], OUTPUT);
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
                    spd[0] = 122; spd[1] = 122; spd[2] = 0; spd[3] = 0; spd[4] = 255, spd[5] = 0;
                  }
                  else if(incomingByte == 50){
                    action = "Moving backwards ";
                    spd[0] = 122; spd[1] = 122; spd[2] = 0; spd[3] = 0; spd[4] = 0, spd[5] = 255;
                  }
                  else if(incomingByte == 52){
                    action = "Turning left ";
                    spd[2] = 122; spd[3] = 122; spd[0] = 0; spd[1] = 0; spd[4] = 0, spd[5] = 255;
                  }
                  else if(incomingByte == 54){
                    action = "Turning right ";
                    spd[2] = 122; spd[3] = 122; spd[0] = 0; spd[1] = 0; spd[4] = 255, spd[5] = 0;
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
                      analogWrite(pins[i], spd[i]);
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
