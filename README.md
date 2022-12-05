# Sensoric

Collects system and sensor data which is then submitted to a time series database such as InfluxDB, and victoria-metrics.

## Requirements
- python3-influxdb
- python3-psutil


## Supported modules

- `cpu_sensor`: 
- `fritzbox_sensor`: network traffic (bytes sent, bytes received)
- `memory_sensor`: memory consumption

## Environment variables

**Required**
- `SENSORIC_DB_HOST`: IP address of the influxdb / victoria metrics host
- `SENSORIC_DB_PORT`: port of the influxdb / victoria metrics host
- `SENSORIC_DB_NAME`: name of the time series database
- `SENSORIC_BATCH_SIZE`: number of batches to collect before sending them to the time series database

**Disk sensor**
- `SENSORIC_DISKS`: space separated list of partitions to watch for disk usage

**Fritzbox sensor**
- `SENSORIC_FRITZ_HOST`: IP address of the Fritz!Box
- `SENSORIC_FRITZ_PORT`: port of the Fritz!Box


## Usage:

Call `sensoric-daemon.py` with the list of sensors to use as outlined below.

```bash
export SENSORIC_DB_HOST=192.168.0.120
export SENSORIC_DB_PORT=8999
export SENSORIC_DB_NAME=sensoric
export SENSORIC_FRITZ_HOST=192.168.0.200
python3 sensoric-daemon.py cpu_sensor memory_sensor network_sensor disk_sensor fritzbox_sensor
``` 


## systemd

You can also start sensoric-daemon from systemd:

```systemd
Unit]
Description=Sensoric daemon service

[Service]
Type=simple
WorkingDirectory=/srv/sensors
Environment=SENSORIC_DB_HOST=192.168.0.120 SENSORIC_DB_PORT=8999 SENSORIC_DB_NAME=sensoric SENSORIC_BATCH_SIZE=1 SENSORIC_DISKS="sda mmcblk1" SENSORIC_FRITZ_HOST=192.168.0.200 SENSORIC_FRITZ_PORT=49000
ExecStart=/srv/sensors/sensoric-daemon.py cpu_sensor memory_sensor network_sensor disk_sensor power_consumption_sensor
Restart=always
User=sensors

[Install]
WantedBy=multi-user.target
Alias=sensor.service
```
