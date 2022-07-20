# Sensoric

Collects system and sensor data which is then submitted to a time series database such as InfluxDB, and victoria-metrics.

## Requirements
- python3-influxdb
- python3-psutil


## Usage:

Call `sensoric-daemon.py` with the list of sensors to use as outlined below

```bash
pyton3 sensoric-daemon.py cpu_sensor memory_sensor network_sensor disk_sensor power_consumption_sensor
``` 


## systemd

You can also start sensoric-daemon from systemd:

```systemd
Unit]
Description=Sensoric daemon service

[Service]
Type=simple
WorkingDirectory=/srv/sensors
ExecStart=/srv/sensors/sensoric-daemon.py cpu_sensor memory_sensor network_sensor disk_sensor power_consumption_sensor
Restart=always
User=sensors

[Install]
WantedBy=multi-user.target
Alias=sensor.service
```
