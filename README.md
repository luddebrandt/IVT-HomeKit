# IVT Heat Pump HomeKit Bridge

A Raspberry Pi bridge that exposes an IVT heat pump's sensors and thermostats to Apple HomeKit via the HAP-python library. Temperature readings and compressor state are read over CAN bus and updated every 2 minutes. Reading are saved in a SQLite database and can be visualized using Grafana. Works with IVT Premiumline HQ and the Rego 1000 controller.

## Overview

The project communicates with an IVT heat pump using CAN bus (via an MCP2515 module on SPI), reads temperature sensors and control values, stores them in a local SQLite database, and makes them available as HomeKit accessories through a HAP bridge.

## Hardware Requirements

- Raspberry Pi (any model with SPI support)
- MCP2515 CAN bus module (connected via SPI)
- IVT heat pump with CAN bus interface

## Software Requirements

- Python 3
- Dependencies listed in `requirements.txt`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Raspberry Pi CAN Bus Setup

Enable SPI and configure the MCP2515 overlay by adding the following to `/boot/config.txt`:

```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```

Then reboot:
```bash
sudo reboot
```

## Project Structure

```
.
├── main.py         # HAP bridge and accessory definitions
├── readIVT.py      # CAN bus communication and SQLite logging
└── requirements.txt
```

## HomeKit Accessories

The bridge exposes the following accessories:

### Thermostats
| Name | Description |
|------|-------------|
| Golvvärme | Radiator forward temperature and setpoint (VK1) |
| Varmvatten | Warm water temperature and setpoint (VV1 + offset) |
| Värmepump | Heat pump — heat fluid in/out temperatures |

### Temperature Sensors
| Name | Sensor | Variable |
|------|--------|----------|
| Golvvärme | Radiator forward | GT1 |
| Utomhus | Outdoor | GT2 |
| Varmvatten | Warm water | GT3 |
| Kompressor | Hot gas | GT6 |
| VP ut | Heat fluid out | GT8 |
| VP retur | Heat fluid in | GT9 |
| Brine retur | Cold fluid in | GT10 |
| Brine ut | Cold fluid out | GT11 |
| Börvärde | Radiator setpoint | VK1 |

Sensor readings are updated every **120 seconds**.

## Data Logging

All readings are stored in a local SQLite database (`IVT.db`) with the following schema:

```sql
CREATE TABLE ivt (
    Time, GT1, GT2, GT3, GT6, GT8, GT9, GT10, GT11, VK1, VV1, VV1o, CS
);
```

`CS` is the compressor state: `1` = heating, `2` = hot water, `0` = idle.

## Running

```bash
python main.py
```

The HAP bridge runs on port **51826**. Scan the QR code printed to the terminal (or use the setup code) to add it to the Home app.

To run as a background service, consider using `systemd` or `screen`.

## CAN Bus Variable Reference

Variables are derived from the IVT Rego 1000 protocol. The CAN IDs are computed as:

```python
hex((idx << 14) | 201342944)
```

where `idx` is the variable index from the Rego 1000 variable list.

## Grafana

<img width="1331" height="1048" alt="Skärmbild 2026-06-25 143128" src="https://github.com/user-attachments/assets/c485fbf4-d420-49d4-9ef3-1b60b721715e" />

