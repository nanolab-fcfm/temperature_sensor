#include <SPI.h>
#include <Adafruit_MAX31865.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// MAX31865 configuration
#define MAX31865_CS_PIN 4    // GPIO15 (was D2)
#define RTD_NOMINAL 100.0     // PT100
#define RREF 430.0            // Reference resistor
#define ONE_WIRE_BUS 2  // D4 corresponds to GPIO2 on the ESP8266

Adafruit_MAX31865 max31865 = Adafruit_MAX31865(MAX31865_CS_PIN);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

String commandBuffer = ""; // Buffer to store received characters

void setup() {
  // Initialize Serial communication at 115200 baud
  Serial.begin(115200);

  // Initialize MAX31865
  max31865.begin(MAX31865_2WIRE);

  Serial.println("ESP8266 is ready.");
  sensors.begin();
  Serial.println("Dallas sensor is ready.");
}

void loop() {
  // Check if data is available on Serial
  while (Serial.available() > 0) {
    char received = Serial.read();
    
    // Ignore newline and carriage return characters
    if (received == '\n' || received == '\r') {
      continue;
    }

    // Add the character to the command buffer
    commandBuffer += received;

    // If a complete command is received, process it
    if (commandBuffer == "R") {
      // Read temperature
      float temperature = max31865.temperature(RTD_NOMINAL, RREF);
      sensors.requestTemperatures();
      
      // Get current time in milliseconds since the program started
      unsigned long currentTime = millis();

      // Send timestamp and temperature over Serial
      Serial.print(currentTime);
      Serial.print(",");
      Serial.print(temperature, 2);
      Serial.print(",");
      Serial.println(sensors.getTempCByIndex(0));

      // Clear buffer after processing
      commandBuffer = "";
    } else if (commandBuffer == "*IDN?") {
      Serial.println("ROSATECH,TSN100,P0000002,1.0.1");
      
      // Clear buffer after processing
      commandBuffer = "";
    }
  }

  // Small delay to prevent excessive CPU usage
  delay(10);
}
