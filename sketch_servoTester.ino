#define SENSOR_KARTONG 8
#define SENSOR_METALL 7
#define SENSOR_PLAST 6

void setup() 
{
  // put your setup code here, to run once:
  pinMode(SENSOR_KARTONG, INPUT);
  pinMode(SENSOR_METALL, INPUT);
  pinMode(SENSOR_PLAST, INPUT);
  Serial.begin(9600);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  if(digitalRead(SENSOR_KARTONG) == HIGH)
  {
    Serial.println("K");
  }
  else if(digitalRead(SENSOR_METALL) == HIGH)
  {
    Serial.println("M");
  }
  else if(digitalRead(SENSOR_PLAST) == HIGH)
  {
    Serial.println("P");
  }
  else
  {
    Serial.println(0);
  }
    
  delay(1000);
}
