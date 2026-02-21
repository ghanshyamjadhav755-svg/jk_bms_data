## JK BMS Data Reader

### Overview

This repository contains a Python-based battery data reader developed to interface with a **JK BMS** using a USB-to-CAN hardware converter. The system directly communicates with the converter device and does **not** use SocketCAN.

---

## Hardware Configuration

### BMS Model

* **JK BMS (CAN Protocol 000 Version)**
* Communication: CAN Bus
* Configured as per JK default CAN output profile

### CAN Interface Converter

* **Waveshare USB-CAN-2A**
* Dual-channel USB to CAN adapter
* Integrated 32-bit MCU
* Direct USB communication (driver-based access, not SocketCAN)

### USB Interface

* CH340 / FTDI USB bridge (depending on board variant)

---

## Physical Wiring

| JK BMS | USB-CAN-2A        |
| ------ | ----------------- |
| CAN-H  | CAN-H             |
| CAN-L  | CAN-L             |
| GND    | GND (if required) |

**Important:**

* Ensure 120Ω termination across CAN-H and CAN-L
* Maintain correct polarity
* Use shielded twisted pair for signal stability

---

## Communication Architecture

```
JK BMS  →  CAN Bus  →  USB-CAN-2A  →  USB  →  Python Script
```

The Python script communicates directly with the USB-CAN device via its driver/API interface. No Linux SocketCAN configuration is required.

---

## Software Requirements

* Ubuntu Linux
* Python 3.x
* Vendor driver / USB communication library
* Custom CAN frame decoding logic

---

## Execution

```bash
python3 battery_status.py
```

---

## Data Extracted

* Total Battery Voltage
* Charge / Discharge Current
* State of Charge (SOC)
* Maximum / Minimum Cell Voltage
* Alarm & Protection Status

---

## Repository Structure

```
battery_status.py
README.md
```

---

## Application Scope

Designed for integration into:

* Autonomous Mobile Robots (AMR)
* Battery health monitoring systems
* Auto-docking validation modules
* Industrial energy monitoring platforms

The architecture supports future expansion for extended CAN frame parsing and alarm classification logic.
