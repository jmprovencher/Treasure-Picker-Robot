int pinClock = 2;
int pinManchester = 50;
bool stateClock = 0;
bool stateManchester = 0;
bool bitDecode = 0;
bool complete = false;
int compteur = 0;
int nombreDeSuite = 1;

bool arrayCode[32] = {0};
bool arrayBigReset[32] = {0};
bool arrayDecode[7] = {0};
bool arraySmallReset[7] = {0};

int codeSecret = 0;
unsigned int count = 0;
unsigned int countLoop = 0;



void setup()
{
  pinMode(pinClock, INPUT);
  pinMode(pinManchester, INPUT);
  attachInterrupt(digitalPinToInterrupt(pinClock), Reading, RISING);
  Serial.begin(9600);
}

//AttachInterrupt sur changement low a high sur clock pour commencer traitement, faire xor avec clock et manchester, puis mettre résultat dans buffer circulaire de 32 bits et écrire dedans,
//vérifier si on a la série qu'on veut (8x1, 0 et message) sinon reboucle puis écrit mot dans le résultat, mettre delay après clock (1µs ?)

void loop()
{
  if (count != countLoop)
  {
    countLoop = count;
    stateClock = digitalRead(pinClock);
    stateManchester = digitalRead(pinManchester);
    bitDecode = stateClock ^ stateManchester;
      //Serial.println(stateManchester);
      //Serial.println(stateClock);
      //Serial.println(bitDecode);
    arrayCode[compteur] = bitDecode;
    compteur++;
  }

  
  if (compteur == 32 && complete == false)
  {
    Serial.print("Reception:");
    for(int h=0;h<32;h++)
    {
      Serial.print(arrayCode[h]);
    }
    Serial.println(".");
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
              Serial.println("Serie terminee, voici le code secret :");
              for (int k = 0; k < 7; k++)
              {
                arrayDecode[k] = arrayCode[k + j + 3];
              }
              for (int b=0;b<7;b++)
              {
                Serial.print(arrayDecode[b]);
              }
              Serial.println(".");
              codeSecret = 0;
              for (int u=0; u<7; u++)
              {
                codeSecret= codeSecret*2+arrayDecode[u];
              }
              Serial.println(codeSecret);
              Serial.println(char(codeSecret));
              memcpy(arrayCode, arrayBigReset, 32);
              memcpy(arrayDecode, arraySmallReset, 7);
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

void Reading()
{
  count++;
}




