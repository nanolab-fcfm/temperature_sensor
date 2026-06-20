# Temperature Sensor

This is a custom temperature measurement device built around an ESP8266 microcontroller that simultaneously reads two independent temperature sensors: a PT100 RTD via a MAX31865 interface (platinum resistance thermometer for precise plate temperature) and a Dallas DS18B20 digital sensor (for ambient temperature). Data is retrieved over serial communication, making it suitable for integration with automation systems like laser_setup.

The device responds to simple ASCII commands, returning timestamped temperature readings in CSV format. It requires minimal external wiring—primarily SPI for the MAX31865 and OneWire for the DS18B20—and communicates at 115200 baud. The hardware is fully documented as a KiCad project with fabrication-ready gerber files, and the firmware is a single Arduino sketch that handles sensor initialization and command processing.

**Key capabilities:**
- Dual temperature measurement (precise PT100 and fast DS18B20)
- Serial request/response protocol with millisecond-precision timestamps
- Device identification query
- Production-ready PCB design with fabrication files
