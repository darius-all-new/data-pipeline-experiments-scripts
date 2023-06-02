'''

Run this script on a Raspberry Pi

This script reads data from an Enviro+ sensor and sends the data to an 
InfluxDB database.

'''

import datetime
import time
import certifi
import influxdb_client, os, time, datetime
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from smbus import SMBus
from bme280 import BME280
from enviroplus import gas
from pms5003 import PMS5003

# ENVIRO+ SETUP
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()

# TODO: HIVEMQ SETUP

# INFLUXDB SETUP
INFLUXDB_TOKEN = "YOUR INFLUXDB TOKEN"
INFLUXDB_ORG = "YOUR INFLUXDB"
INFLUXDB_URL = "YOUR INFLUXDB URL"
INFLUXDB_BUCKET = "YOUR INFLUXDB BUCKET"
INFLUXDB_MEASUREMENT = "YOUR INFLUXDB MEASUREMENT"

# How often to write data to the InfluxDB database
DATA_WRITE_RATE = 5

write_client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_URL, 
    token=INFLUXDB_TOKEN, 
    org=INFLUXDB_ORG,
    ssl_ca_cert=certifi.where())

# Define the write api
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# TODO: MQTT FUNCTIONS
# ====================

# DATA READ
# =========
def read_data():
    '''
    Reads data from the Enviro+ sensors and creates a simple dictionary 
    where each key-value pair is the sensor name and the value. There is also a timestamp included.
    
    Adapt this to read whatever data you need.
    '''
    temp = bme280.get_temperature()
    hum = bme280.get_humidity()
    pres = bme280.get_pressure()

    ts = datetime.datetime.utcnow().isoformat()

    # Return a dictionary with the sensor values and a timestamp
    return {
        "temperature": temp,
        "humidity": hum,
        "pressure": pres,
        "ts": ts
    }

# MAIN LOOP
# =========
if __name__=="__main__":

    while True:

        msg = read_data()

        point = (
                Point(INFLUXDB_MEASUREMENT)
                .tag("location", "All New HQ")
                .field("temperature", msg["temperature"])
                .field("humidity", msg["humidity"])
                .field("pressure", msg["pressure"])
                .time(msg["ts"])
            ) 
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        time.sleep(DATA_WRITE_RATE)
