# Hardware

The temperature sensor is implemented as a custom PCB designed in KiCad, located at `hw/temperature_sensor.kicad_sch` (schematic), `hw/temperature_sensor.kicad_pcb` (layout), and `hw/temperature_sensor.kicad_pro` (project file). Custom footprints for the ESP8266 module and temperature sensor breakout are defined in `hw/temperature_sensor_footprints.pretty/`.

**Fabrication files** are provided in `hw/fab/` in standard Gerber format:
- `temperature_sensor-F_Cu.gbr` – Front copper layer
- `temperature_sensor-B_Cu.gbr` – Back copper layer
- `temperature_sensor-Edge_Cuts.gbr` – Board outline
- `temperature_sensor-PTH.drl` – Plated through-hole drill file
- `temperature_sensor-NPTH.drl` – Non-plated through-hole drill file
- `temperature_sensor-PTH-drl_map.gbr` – PTH legend
- `temperature_sensor-NPTH-drl_map.gbr` – NPTH legend
- `temperature_sensor-job.gbrjob` – Gerber job file for PCB manufacturers

**Components required:**
- **ESP8266** microcontroller board (e.g., NodeMCU, Wemos D1)
- **MAX31865 RTD-to-Digital Converter** breakout module (for PT100 sensor)
- **PT100 RTD sensor** (3-wire or 4-wire; firmware assumes 2-wire mode)
- **Dallas DS18B20** temperature sensor or module
- **SPI interconnect** for MAX31865 (MISO, MOSI, SCK, CS)
- **OneWire bus** connection for DS18B20
- **4.7 kΩ pull-up resistor** on DS18B20 data line
- **USB-to-Serial converter** (e.g., FTDI, CH340G) for programming and serial communication

**Wiring:**
| ESP8266 Pin | Signal | Component |
|------------|--------|-----------|
| GPIO15 (D2) | CS | MAX31865 chip select |
| GPIO13 | MOSI | MAX31865 data in |
| GPIO12 | MISO | MAX31865 data out |
| GPIO14 | SCK | MAX31865 clock |
| GPIO2 (D4) | OneWire Data | DS18B20 data line |
| 3.3V | Power | Both MAX31865 and DS18B20 modules |
| GND | Ground | Both modules |

Refer to the KiCad files and gerber drawings for PCB layout details. The design is ready for standard JLCPCB, PCBWay, or Oshpark fabrication.
