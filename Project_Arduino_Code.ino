#include <dht.h>
#define dht_apin A0 // Analog Pin sensor is connected to
#define soil_moisture A1 //Soil Moisture connected to

dht DHT;
float moisture_percentage;
int sensor_moisture;

void setup() 
{
  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);
  pinMode(soil_moisture, INPUT);  
  Serial.begin(9600);
}

void loop() 
{
  if(Serial.available() > 0)
  {
    if(Serial.read() == 's')
    {
    DHT.read11(dht_apin);
    
    digitalWrite(12,HIGH); //Turn on Soil moisture sensor if reading is needed
    delay(1000);  // Delay for the calibration of the sensor   
    
    sensor_moisture = analogRead(soil_moisture);
    moisture_percentage = ( 100 - ( (sensor_moisture/1003.00) * 100 ) );
    
    Serial.print(DHT.humidity);
    Serial.print("\t");
    Serial.print(DHT.temperature); 
    Serial.print("\t");
    Serial.print(moisture_percentage); 
    Serial.println("\t");
    
    delay(1000); // Delay for the calibration of the sensor
    digitalWrite(12,LOW); //Turn off Soil moisture sensor if reading is not needed
    delay(3000);//Wait 1 seconds before accessing sensor again.
    }
  }  

    else
    {
      digitalWrite(12,LOW);
    }
}
