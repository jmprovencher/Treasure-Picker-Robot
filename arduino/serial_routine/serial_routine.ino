#include <LiquidCrystal.h>


// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// global value that corresponds to the byte sent by the micro PC by UART.
int incomingByte = 0; 
boolean mode = false;
String action = "";
int pins[4] = {2, 3, 4, 7};
int spd[4] = {0, 0, 0, 0};

void setup() {
  // put your setup code here, to run once:
   Serial.begin(115200);
   
   lcd.begin(16, 2);              // start the library
   lcd.setCursor(0,0);
   lcd.print("Capacitor charge: none"); // print a simple message
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();
                for(int i = 0; i<4; i++){
                  analogWrite(spd[i], pins[i]);
                }
                
                if(!mode){
                  if(incomingByte == 56){
                    action = "Moving forward ";
                  }
                  else if(incomingByte == 50){
                    action = "Moving backwards ";
                  }
                  else if(incomingByte == 52){
                    action = "Turning left ";
                  }
                  else if(incomingByte == 54){
                    action = "Turning right ";
                  }
                  else{
                    action = "Invalid action ";
                  }
                  delay(10);
                  mode = !mode;
                }
                else if(mode){
                  for(int i = 0; i < incomingByte; i++){
                    if(Serial.available() > 0){
                      mode = !mode;
                      break;
                    }
                    lcd.setCursor(1,0);
                    Serial.print(action);
                    Serial.println(incomingByte - i, DEC);
                    delay(10);
                  }
                  mode = !mode;
                }
        }
}
