int pinClock = 48;
int pinManchester = 50;
int stateClock = 0;
int stateManchester = 0;
int lastStateClock = 0;
int lastStateManchester = 0;
int code = 0;

//double sum=0;
//int count=0;

void setup()
{
  pinMode(pinClock, INPUT);
  pinMode(pinManchester, INPUT);
  Serial.begin(9600);
}


void loop()
{
  stateClock = digitalRead(pinClock);
//  Serial.println(stateClock);
  stateManchester = digitalRead(pinManchester);
//  Serial.println(stateManchester);
  if (stateClock != lastStateClock && stateClock == HIGH)
  {
    if (stateManchester != lastStateManchester && stateManchester == HIGH)
    {
      Serial.println(0);
    }
    if (stateManchester != lastStateManchester && stateManchester == LOW)
    {
      Serial.println(1);
    }
//    else
//    {
//      Serial.println("Error");
//    }
  }
  lastStateClock = stateClock;
  lastStateManchester = stateManchester;
}



