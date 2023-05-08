#include <WiFi.h>
#include <Wire.h>           
#include <PubSubClient.h> 
#include <WebServer.h>
#include <HTTPClient.h>
#include "DHTesp.h"

#define DHTpin 15
DHTesp dht;
float temperature_velue, humidity_velue;

const char* ssid = "F-19"; 
const char* password = "qwe123456";

String payload = "";

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); 
    Serial.print(".");
  }
  Serial.print("Connected!");
  dht.setup(DHTpin, DHTesp::DHT11);
}

 void loop()
{
  temperature_velue = dht.getTemperature();
  humidity_velue = dht.getHumidity();

  Serial.println(temperature_velue);
  Serial.println(humidity_velue);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "https://zct-tuke.azurewebsites.net/?";
    url += "temperature=";
    url += temperature_velue;
    url += "&humidity=";
    url += humidity_velue;

    http.begin(url);
    int httpCode = http.GET();
    if (httpCode > 0){
      payload = http.getString(); 
    }
    else{
      Serial.print("pizdec");
    }
    http.end();
  } 

  delay(600000); 
}