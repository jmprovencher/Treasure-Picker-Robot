int pinClock = 2;
int pinManchester = 50;
bool stateClock = 0;
bool stateManchester = 0;
bool transmission = 0;
bool bitDecode = 0;
bool arrayCode[32] = {0};
int compteur = 0;
int nombreDeSuite = 1;
int compteurCode = 0;
bool arrayDecode[7] = {0};



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
  if (compteur == 31)
  {
    while (nombreDeSuite != 8)  //peut rester coincer dans while ?
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
            if (nombreDeSuite == 8 && arrayCode[j+2] == 0)
              {
                for (int k = j+3; k < j+9; k++)
                {
                  arrayDecode[compteurCode] = arrayCode[k];
                  compteurCode++;
                }
              }
            }
          }
        }
      }
    }
    compteur = 0;
  }
}

void Reading()
{
  // ajouter delay ?
  stateClock = digitalRead(pinClock);
  stateManchester = digitalRead(pinManchester);
  bitDecode = stateClock ^ stateManchester;
  arrayCode[compteur] = bitDecode;
  compteur++;
}




