#include <WiFi.h>
#include <HTTPClient.h>

#define DOOR_SENSOR_PIN  25  // ESP32 pin GPIO19 connected to door sensor's pin

// Replace with your network credentials
const char* ssid = "";
const char* password = "";

// Replace with your Supabase project API URL and anon key
const char* supabaseUrl = "";
const char* supabaseKey = "";

// Table insert endpoint
String tableUrl = String(supabaseUrl) + "/rest/v1/door_sensor";

int doorState;

void setup() {
  Serial.begin(115200);                      // Initialize serial
  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);  // Set ESP32 pin to input pull-up mode

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  // Read door sensor state
  doorState = digitalRead(DOOR_SENSOR_PIN); // read the state of the door sensor

  bool isOpen = (doorState == HIGH);  // True if door is open (HIGH), false if closed (LOW)

  // Print the door state
  if (isOpen) {
    Serial.println("The door is open");
  } else {
    Serial.println("The door is closed");
  }

  // Send door state to Supabase
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Start connection to the Supabase REST API
    http.begin(tableUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", supabaseKey);  // Add Supabase API key to the headers

    // Prepare JSON data (send as true/false)
    String postData = "{\"is_open\":" + String(isOpen ? "true" : "false") + "}";

    // Send HTTP POST request
    int httpResponseCode = http.POST(postData);

    // Check the response
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      Serial.println("Supabase Response: " + response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    // Close connection
    http.end();
  }

  // Delay before next reading (e.g., 5 minutes)
  delay(300000); // millSec
}
