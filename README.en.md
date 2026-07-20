# ArduinoCpuTemp

*Read this in other languages: **English** · [Русский](README.md)*

CPU temperature indication with three LEDs connected to an Arduino.
A Windows script reads the CPU temperature via Open Hardware Monitor and sends it
over USB (Serial) to the board once per second. The Arduino lights the matching LED
depending on the temperature range.

## How it works

```
┌────────────────────┐   Serial 9600   ┌──────────────────┐
│  PC (Windows)      │ ──────────────► │   Arduino        │
│  control.py        │   "<temp>\n"    │   sketch.ino     │
│  reads CPU temp    │                 │  lights an LED   │
│  via WMI / OHM     │                 │  by range        │
└────────────────────┘                 └──────────────────┘
```

Indication thresholds (defined in the sketch):

| CPU temperature | LED             | Pin |
|-----------------|-----------------|-----|
| below 56 °C     | LED1 (normal)   | 3   |
| 56–69 °C        | LED2 (warm)     | 4   |
| 70 °C and above | LED3 (hot)      | 5   |

Thresholds are set in the sketch via `#define TEMP_WARN` and `#define TEMP_HOT`.

## Requirements

Hardware:
- Arduino (Uno / Nano / any compatible board)
- 3 LEDs + current-limiting resistors (usually 220–330 Ω)
- USB cable

Software (Windows only):
- [Open Hardware Monitor](https://openhardwaremonitor.org/) — the temperature data source
- Python 3
- Python packages: `wmi`, `pyserial`

  ```bash
  pip install wmi pyserial
  ```

> The script uses the Open Hardware Monitor WMI provider (`root\OpenHardwareMonitor`),
> so it only works on Windows. It will not run as-is on Linux/macOS.

## Wiring

The LEDs connect to digital pins through resistors:

```
Pin 3 ──[220Ω]──►|── GND   (LED1)
Pin 4 ──[220Ω]──►|── GND   (LED2)
Pin 5 ──[220Ω]──►|── GND   (LED3)
```

## Setup and run

### 1. Flash the Arduino

1. Open `sketch_dec31a.ino` in the Arduino IDE.
2. Select your board and port under **Tools**.
3. Click **Upload**.

### 2. Start Open Hardware Monitor

It must be open and running in the background, otherwise the temperature cannot be read.

### 3. Configure and run the script

In `control.py`, set your COM port (default is `COM5`):

```python
ARDUINO_PORT = "COM5"  # replace with your port
```

You can find the port in the Arduino IDE (**Tools → Port**) or in Device Manager.

Then run:

```bash
python control.py
```

The console prints the current temperature, and the matching LED lights up on the
board. Stop with `Ctrl+C`.

> Order matters: flash the board first, then run `control.py`.

## Troubleshooting

- **`could not open port COM5`** — wrong port or it is busy. Close the Serial Monitor
  in the Arduino IDE and check the port number. The script will wait and retry the connection.
- **`Не удалось подключиться к Open Hardware Monitor`** (failed to connect to OHM) — the
  program is not running. Open it and keep it in the background.
- **`Сенсор температуры CPU не найден`** (CPU temperature sensor not found) — OHM does not
  expose the sensor; make sure the CPU temperature is visible in its window.
- **LEDs do not react** — make sure the 9600 baud rate matches in both the sketch and the
  script, and that the LEDs are wired to pins 3, 4, 5.

## Project files

- `control.py` — Windows host script: reads the CPU temperature and sends it over Serial.
- `sketch_dec31a.ino` — Arduino sketch: receives the temperature and drives the LEDs.
