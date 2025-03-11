#Xiaomi MQTT Home Automation
A containerized solution using Docker Compose that integrates a Mosquitto MQTT broker and a Python bridge to control two Xiaomi smart plugs via MQTT.

Overview
This project consists of two main components:

Mosquitto MQTT Broker: 
-Runs in its own container with configuration, data, and logs stored under /opt/mosquitto.
-Xiaomi Bridge: A Python-based MQTT client container that connects to two Xiaomi smart plugs and allows you to control them via dedicated MQTT topics.

Prerequisites:

-Docker and Docker Compose installed on your machine.

-Xiaomi smart plug details:
IP addresses
Device tokens

Local Setup:
1. Clone the Repository
git clone https://github.com/your_username/your_repo.git
cd your_repo

2. Prepare Mosquitto Directories in /opt
Create a consistent, system-wide location for Mosquitto configuration, data, and logs:

sudo mkdir -p /opt/mosquitto/config /opt/mosquitto/data /opt/mosquitto/log
sudo chown -R $USER:$USER /opt/mosquitto


3. Configure Mosquitto
Create the configuration file at /opt/mosquitto/config/mosquitto.conf:

If defualt settings at the configuration file are not sufficient change them.

4. Build and Run the Containers
Ensure your docker-compose.yml is correctly configured. Then, from the repository root, run:

docker-compose up -d
This command builds and starts both the Mosquitto and Xiaomi bridge containers.

Usage:

MQTT Broker
Mosquitto is exposed on port 1883. You can test its functionality using MQTT clients (e.g., mosquitto_pub and mosquitto_sub).

Xiaomi Bridge
The Xiaomi bridge listens for commands to control two smart plugs using these topics:

Plug 1:
Command: xiaomi/plug1/command
Response: xiaomi/plug1/response
Plug 2:
Command: xiaomi/plug2/command
Response: xiaomi/plug2/response
Example Commands:

Turn on Plug 1:
mosquitto_pub -h localhost -t "xiaomi/plug1/command" -m "ON"
Turn off Plug 1:
mosquitto_pub -h localhost -t "xiaomi/plug1/command" -m "OFF"

Similarly, for Plug 2:
mosquitto_pub -h localhost -t "xiaomi/plug2/command" -m "ON"
mosquitto_pub -h localhost -t "xiaomi/plug2/command" -m "OFF"

Project Structure:

.
├── docker-compose.yml       # Docker Compose orchestration file
├── mosquitto/               # (Optional) Local configuration directory for Mosquitto (mounted from /opt/mosquitto)
│   ├── config/mosquitto.conf
│   ├── data/
│   └── log/
└── xiaomi_bridge/           # Xiaomi Bridge project
    ├── Dockerfile           # Dockerfile for the Python bridge container
    ├── requirements.txt     # Python dependencies
    └── xiaomi_mqtt_bridge.py# Python bridge script for controlling Xiaomi smart plugs

    
Troubleshooting


Container Issues:
  Check logs with:
    docker logs mosquitto
    docker logs xiaomi_bridge

MQTT Connectivity:
Verify that port 1883 is free and accessible. Test with:
mosquitto_pub -h localhost -t "test" -m "Hello, MQTT"


Configuration File Errors:
Ensure /opt/mosquitto/config/mosquitto.conf exists and is readable by Docker.


