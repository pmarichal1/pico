#include <WiFi.h>
#include <DHT.h>
const char* ssid = 'SpectrumSetup-AC';      // Updated Wi-Fi network SSID
const char* password = 'winedrama832;       // Updated Wi-Fi network password
define DHTPIN 28                            // Digital pin connected to the DHT sensor
DHT dht(DHTPIN, DHT11);
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  { delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
  dht.begin();
  server.begin();
}

void loop() {
    float humidity = dht.readHumidity();   
    float temperature = dht.readTemperature();
    Serial.println("Temperature: "+(String)temperature);
    Serial.println("Humidity: "+(String)humidity);
    delay(1000);  
    WiFiClient client = server.available();
    if (client) {
      Serial.println("New client connected");
      String response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
      response += "<!DOCTYPE html><html><body>";
      response += "<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
      response += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
      response += "body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;}\n";
      response += "p {font-size: 24px;color: #444444;margin-bottom: 10px;}\n";
      response += "</style>\n";
      response += "</head>\n";
      response += "<body>\n";
      response += "<h1>Raspberry Pi Pico W Weather Station</h1>";
      response += "<p>Temperature: <span id=\"temperature\"></span>" + String(temperature)+ "&deg;C</p>";
      response += "<p>Humidity: <span id=\"humidity\"></span> " + String(humidity) + " %</p>";
      response += "</body></html>";
      client.print(response);
      delay(10);
      client.stop();
      Serial.println("Client disconnected");
  }
}
