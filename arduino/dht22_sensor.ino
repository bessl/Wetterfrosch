#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(t) || isnan(h)) {
    Serial.println("DHT22 read error!");
  } else {
    Serial.println("Humidity: " +  String(h) + "%\t" + " Temperature:" +  String(t) + "C");  
  }
  delay(5000);
}
