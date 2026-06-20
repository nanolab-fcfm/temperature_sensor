# Firmware

The firmware (`fw/main.ino`) is an Arduino sketch compiled and flashed to the ESP8266 microcontroller. It initializes both temperature sensors and implements a simple command-response protocol over serial.

**Board and toolchain:**
- **Board**: ESP8266 (NodeMCU, Wemos D1, or equivalent)
- **Arduino IDE**: Configure board as "NodeMCU 1.0 (ESP-12E Module)" or equivalent ESP8266 variant
- **Baud rate**: 115200 (8N1)

**Required libraries** (install via Arduino IDE Library Manager):
- `Adafruit MAX31865` – Adafruit's MAX31865 RTD converter library
- `DallasTemperature` – OneWire temperature sensor library
- `OneWire` – OneWire protocol library (usually bundled with DallasTemperature)

**Flashing:**
1. Connect the ESP8266 board via USB-to-Serial converter (TX → RX, RX → TX, GND → GND, 3.3V → 3.3V)
2. Select board type and COM port in Arduino IDE
3. Open `fw/main.ino` and click Upload
4. Monitor serial output at 115200 baud to confirm "ESP8266 is ready" and "Dallas sensor is ready"

**Protocol and commands:**

The device listens for ASCII commands on serial. Commands are case-sensitive and must be terminated with a newline or carriage return (or neither—the firmware processes them immediately upon completion).

| Command | Response | Description |
|---------|----------|-------------|
| `R` | `<clock>,<plate>,<ambient>` | Request timestamped temperatures. `clock` is milliseconds since boot. `plate` is PT100 temperature (°C, 2 decimals) from MAX31865. `ambient` is DS18B20 temperature (°C, 1 decimal) from OneWire. |
| `*IDN?` | `ROSATECH,TSN100,P0000002,1.0.1` | Request device identification: manufacturer, model, serial number, firmware version. |

**Example serial session (115200 baud):**
```
R
12345,23.45,22.1
R
12455,23.47,22.1
*IDN?
ROSATECH,TSN100,P0000002,1.0.1
```

**Key firmware details:**
- **MAX31865 configuration**: 2-wire mode, RTD nominal resistance 100 Ω (PT100), reference resistor 430 Ω
- **Timestamp source**: `millis()` wraps every ~49 days
- **Sensor reading timing**: DS18B20 is sampled after MAX31865; there is no inter-sample delay between the two readings
- **Buffer handling**: Commands are accumulated character-by-character and processed when the full command string is matched; newlines and carriage returns are ignored
