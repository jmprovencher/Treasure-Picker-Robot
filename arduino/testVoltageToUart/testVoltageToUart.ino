#include <stdlib.h>

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);

}
float voltage = 4.3567;
float complete = 9;
int count = 0;
void loop() {
String output = String(voltage);

String commandComplete = String("done");
delay(1000);
writeString(commandComplete);
delay(1000);
writeString(output);

}

void writeString(String stringData) { // Used to serially push out a String with Serial.write()

  for (int i = 0; i < stringData.length(); i++)
  {
      Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }

}// end writeString
