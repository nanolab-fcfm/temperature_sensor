# Usage

Once the device is assembled, flashed, and wired, it is ready to communicate over a serial port. It is designed to integrate with automation systems like **laser_setup** that use the PT100SerialSensor interface.

**Basic usage:**

Connect the device to a computer or lab system via USB-to-Serial converter. Open a serial terminal (e.g., `minicom`, `screen`, Arduino IDE Serial Monitor) at **115200 baud, 8 data bits, no parity, 1 stop bit**.

Send the command `R` (followed by a newline, though the firmware will process it immediately):
```
R
```

The device will respond with a single line of CSV data:
```
<milliseconds_since_boot>,<PT100_temperature>,<DS18B20_temperature>
```

Example output:
```
R
45023,24.32,23.8
```

This means 45023 ms have elapsed since boot, the PT100 sensor reads 24.32°C, and the DS18B20 reads 23.8°C.

To query the device identity, send `*IDN?`:
```
*IDN?
ROSATECH,TSN100,P0000002,1.0.1
```

**Integration with laser_setup:**

The PT100SerialSensor class in laser_setup expects to:
1. Open a serial port at 115200 baud
2. Send the command `R` followed by a newline
3. Receive a response line matching the pattern `<clock>,<plate>,<ambient>`
4. Parse the three comma-separated values as floats

The firmware output exactly matches this protocol. Ensure the serial port device path is correctly specified in laser_setup configuration (typically `/dev/ttyUSB0` on Linux or a COM port on Windows).

**Sensor characteristics:**

- **PT100 (MAX31865)**: Industry-standard platinum RTD. Provides precise, stable temperature readings over a wide range. Typical accuracy ±0.5°C after calibration. Used for "plate" temperature (main measurement).
- **DS18B20 (OneWire)**: Dallas digital temperature sensor. Fast response, good for ambient monitoring. Typical accuracy ±0.5°C. Used for "ambient" temperature (secondary channel).

Both sensors are read on each `R` command. If either sensor is disconnected or fails, the output may contain NaN or invalid values; implement error handling in the consuming application as needed.

**Troubleshooting:**

- **Device not responding**: Verify the serial port is connected at 115200 baud. Check that the ESP8266 is powered (LED should be lit). Confirm that the MAX31865 and DS18B20 are correctly wired.
- **MAX31865 returns 0 or invalid readings**: Check SPI wiring (MOSI, MISO, SCK, CS). Verify the CS pin is GPIO15 (D2) and properly pulled. Confirm the PT100 sensor is connected to the MAX31865 module.
- **DS18B20 missing or stuck at high temperature**: Check OneWire wiring to GPIO2 (D4). Verify the 4.7 kΩ pull-up resistor is present between VCC and the data line. Confirm the sensor is properly seated.
- **Garbage output on serial**: Verify baud rate is exactly 115200. Check USB-to-Serial converter drivers are installed. Try a different USB port or converter if issues persist.
