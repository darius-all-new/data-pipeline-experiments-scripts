# Experimenting with Data Pipelines (Scripts)

This is intended to provide industrial engineers and others interested in the field with a solid starting point for exploring data acquisition, storage, and visualization in the context of Industry 4.0 (I4.0) and Industrial Internet of Things (IIoT) applications.

## Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Instructions](#instructions)
- [Disclaimer](#disclaimer-experimental-and-prototyping-use-only)

## Overview

Two repos make up the standard project providing an end-to-end pipeline going from a Raspberry Pi to a React-based frontend interface.

This is the scripts repo and contains the backend components.

For the user interface see the [frontend repo](https://github.com/darius-all-new/data-pipeline-experiments-frontend).

## Why use this? 🤷‍♂️

There are loads of platforms and tools that connect to assets and handle data. They are all very capable and many are even free (or have a free tier). All of these platforms have loads of features and often learning curves that go along with that.

Sometimes though, when you're experimenting with I4.0 type projects, what you really need is something simple and under your control. That is the purpose of this pipeline.

I made this pipeline for my own experiments and thought I'd open it up in case anyone else also finds it useful! I'll also be adding functionality periodically.

## Requirements

You will need:

- A Raspberry Pi (or similar "edge" device)
- An [Enviro+ sensor board](https://shop.pimoroni.com/products/enviro?variant=31155658457171) (or your own sensors)
- An InfluxDB account (you can get this working on the free tier)
- A Cloudflare account (you can get this working on the free tier)

## Instructions

This repo contains:

- 🐍 A Python script (`rpi_agent.py`) for connecting to an Enviro+ sensor and sending data to an InfluxDB instance in the cloud
- ⏰ A script (`rpi_agent.service`) for automatically running the above Python script
- 🛠️ A script (`worker.js`) for a Cloudflare worker that will query the InfluxDB database and make data available via an API endpoint that the frontend can query.

### The Python Script

The Python script as-provided simply reads data from an Enviro+ board and periodically writes the data to your InfluxDB cloud database.

1. Make sure the rpi_agent.py script is on your Raspberry Pi and make a note of the location.

2. Install the requirements (found in requirements.txt)

```
pip install -r requirements.txt
```

3. Add your InfluxDB credentials and settings to the lines below. You will need an InfluxDB token and URL plus the organisation, bucket and measurement you want to add data to.

```
INFLUXDB_TOKEN = "YOUR INFLUXDB TOKEN"
INFLUXDB_ORG = "YOUR INFLUXDB"
INFLUXDB_URL = "YOUR INFLUXDB URL"
INFLUXDB_BUCKET = "YOUR INFLUXDB BUCKET"
INFLUXDB_MEASUREMENT = "YOUR INFLUXDB MEASUREMENT"
```

4. You can run the script now or use a service to automatically run the script even after a reboot.

### Setup a Service

To setup a service to run the agent script:

1. In rpi_agent.service make sure the line calling the script is setup correctly:

```
ExecStart=/usr/bin/python3 /path/to/script/rpi_agent.py
```

2. Place the service file on your Raspberry Pi at this location:

```
/lib/systemd/system/rpi_agent.service
```

3. Set the right permissions on the service file:

```
sudo chmod 644 /lib/systemd/system/rpi_agent.service
```

Note: change the chmod number based on your requirements ([more info](https://en.wikipedia.org/wiki/Chmod)).

4. Reload and enable:

```
sudo systemctl daemon-reload
```

```
sudo systemctl enable rpi_agent.setvice
```

5. If you need to check the status or restart the service:

```
sudo systemctl status rpi_agent.setvice
```

```
sudo systemctl restart rpi_agent.setvice
```

### Create a Cloudflare Worker

The Cloudflare worker is a bridge between the frontend interface and the data stored in InfluxDB.

All you need to do is create a Cloudflare worker and add the contents of `worker.js` to the default script (also called worker.js) that comes with the new worker.

Once you've added the code and clicked "save and deploy" your worker should be up and ready to go. Try navigating to the endpoint in a browser and you should see your data returned to you!

### Done!

With all 3 parts running you will have a data pipeline covering your sensor and edge device, cloud storage and cloud data retreival. Everything is ready for the frontend ()

The data is ready to feed into the frontend [frontend repo](https://github.com/darius-all-new/data-pipeline-experiments-frontend).

## Disclaimer: Experimental and Prototyping Use Only

Please note that the code in this repository is intended solely for experimentation and prototyping purposes. It is not intended for use in production environments or critical systems. By accessing or using the code in this repository, you acknowledge and agree that:

The code provided is for educational and exploratory purposes only. It may contain errors, bugs, or other issues that could affect its functionality, reliability, or security.

The code may not have undergone rigorous testing, validation, or verification processes required for production-ready software.

The code may not adhere to best practices, coding standards, or industry-specific regulations applicable to production systems.

The code is provided "as is" without any warranties or guarantees of any kind. The author(s) of this repository shall not be held liable for any direct, indirect, incidental, special, or consequential damages arising out of the use or inability to use the code.

It is your responsibility to review, modify, and adapt the code according to your specific needs and requirements, taking into consideration the necessary safety, security, and performance considerations.

It is highly recommended that you exercise caution and prudence when using the code in this repository. If you intend to use the concepts, techniques, or code in a production or critical system, it is essential to conduct thorough testing, validation, and verification processes to ensure its suitability, reliability, and security.

By using this repository, you agree to indemnify and hold harmless the author(s) from any claims, damages, or liabilities arising out of the use, misuse, or reliance on the code provided.

Remember, always prioritize safety, security, and reliability when implementing code in production or critical systems.
