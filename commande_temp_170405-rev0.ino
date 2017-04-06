//pour le 280
#include <Wire.h>
#include "SPI.h" //Why? Because library supports SPI and I2C connection
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP280.h"
//pour le dht11
#include <dht.h>
//pour écran LCD
#include <LiquidCrystal.h>

dht DHT;
#define DHT11_PIN 8

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

//Setup connection of the sensor
Adafruit_BMP280 bmp; // I2C


//Variables
float pressure;   //To store the barometric pressure (Pa)
float temp_in;  //To store the temperature (oC)
int altimeter;    //To store the altimeter (m) (you can also use it as a float variable)
float humidity;  //To store the humidity (%)
float temp_ext;  //To store the DHT temparature
int statut_fan;  //état du ventialteur 1 On 0 off
int statut_chauff; // état du fil chauffant 1 On 0 off

//Instruction pour regulation de temperature
float temp_basse = 20;  // Limite basse de temperature (oC)
float temp_haute = 25;  // Limite haute de temperature (oC)
float zone_basse = 22;  // Limite basse de temperature (oC)
float zone_haute = 23;  // Limite haute de temperature (oC)

//déclaration sortie fan et chauffage
int pin_fan = 9;
int pin_chauff = 10;

void setup() {
  bmp.begin();    //Begin the sensor
  pinMode(pin_fan,OUTPUT);
  pinMode(pin_chauff,OUTPUT);
  Serial.begin(9600); //Begin serial communication at 9600bps
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Tin:");
  
}

void loop() {
  //Read values from the sensor:
  pressure = bmp.readPressure()/100;
  temp_in = bmp.readTemperature();
  altimeter = bmp.readAltitude (1050.35); //Change the "1050.35" to your city current barrometric pressure (https://www.wunderground.com)
  int chk = DHT.read11(DHT11_PIN);
  humidity = DHT.humidity;
  temp_ext = DHT.temperature;
  
  //controle du fan et du chauff
    if (temp_in > temp_haute) {
    analogWrite(pin_fan,255);
    statut_fan = 1;
     } 
    else if (temp_in < temp_basse) {
    analogWrite(pin_fan,255);
    analogWrite(pin_chauff,255);
    statut_fan = 1;
    statut_chauff = 1;
     } 
    else if (temp_in < zone_haute && temp_in > zone_basse) {
    analogWrite(pin_fan,0);
    analogWrite(pin_chauff,0);
    statut_fan = 0;
    statut_chauff = 0;
     } 
  
  //Print values to serial monitor:
  
  Serial.print(temp_in);
  Serial.print((","));
  Serial.print(temp_ext);
  Serial.print((","));
  Serial.print(statut_fan);
  Serial.print((","));
  Serial.println(statut_chauff);
  Serial.print((","));
  Serial.print(pressure);
  Serial.print((","));
  Serial.print(humidity);
   
 lcd.setCursor(0, 0);
 lcd.print("Tin:");
 lcd.print(temp_in);
 lcd.print((char)223);
 lcd.print("C");
 lcd.print("rad:");
 lcd.print(statut_chauff);
 lcd.setCursor(0, 1);
 lcd.print("Tex:");
 lcd.print(temp_ext);
 lcd.print((char)223);
 lcd.print("C");
 lcd.print("fan:");
 lcd.print(statut_fan);
 
  delay(2500); //Update every 5 sec
 } 

