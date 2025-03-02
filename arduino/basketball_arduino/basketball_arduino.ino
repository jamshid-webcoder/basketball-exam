#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define SENSOR_PIN D7        

const char* ssid = "Tenda";
const char* password = "tenda2024";
const char* server = "http://192.168.1.113:8000/uz/counter/correct_attempts/";
const char* api_key = "1qw23er45ty67ui89o";

WiFiClient client;  

void setup() {
  pinMode(SENSOR_PIN, INPUT);

  Serial.begin(115200);
  delay(1000);

  Serial.println("Wi-Fi ga ulanmoqda...");
  WiFi.begin(ssid, password);
  
  int attempt = 0;
  int max_attempts = 5; 

  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    Serial.print("Ulanishga urinish: ");
    Serial.println(attempt + 1);
    
    attempt++;
    if (attempt >= max_attempts) {
      Serial.println("\nWi-Fi ulanib bo‘lmadi. Qurilma qayta yuklanmoqda...");
      delay(1000);
      ESP.restart();
    }
  }

  Serial.println("\nWi-Fi muvaffaqiyatli ulandi!");
  Serial.print("IP manzil: ");
  Serial.println(WiFi.localIP());
  delay(3000);
}

void loop() {
  int sensorValue = digitalRead(SENSOR_PIN); 

  if (sensorValue == LOW) {  

    Serial.println("To'p savatga tushdi!");
    sendPostRequest();
    delay(5000);
    
  } else {
    Serial.println("To'p savatga tushmadi!");
  }


}

void sendPostRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    Serial.println("POST so‘rovi yuborilmoqda...");
    
    http.begin(client, server);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("API-KEY", api_key);
    
    String payload = "{\"event\": \"ball_dropped\"}";
    
    int httpResponseCode = http.POST(payload);
    
    if (httpResponseCode > 0) {
      Serial.println("POST so‘rovi muvaffaqiyatli yuborildi.");
      Serial.println("Status Code: " + String(httpResponseCode));
      Serial.println("Serverdan javob: " + http.getString());
    } else {
      Serial.println("POST so‘rov yuborishda xatolik.");
      Serial.print("Xato kodi: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("Wi-Fi ulanmagan, POST so‘rov yuborilmadi.");
  }
}
