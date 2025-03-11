import paho.mqtt.client as mqtt
from miio import ChuangmiPlug  # Recommended class for Xiaomi plugs

# --- Configuration ---
MQTT_BROKER = "mosquitto"  # Use the service name defined in docker-compose
MQTT_PORT = 1883

# Topics for Plug 1
COMMAND_TOPIC_PLUG1 = "xiaomi/plug1/command"
RESPONSE_TOPIC_PLUG1 = "xiaomi/plug1/response"

# Topics for Plug 2
COMMAND_TOPIC_PLUG2 = "xiaomi/plug2/command"
RESPONSE_TOPIC_PLUG2 = "xiaomi/plug2/response"

# Replace with your plugs' IP addresses and tokens
# Plug 1 details
PLUG1_IP = ""         # Example: Plug 1 IP address
PLUG1_TOKEN = ""  # Replace with your actual token

# Plug 2 details
PLUG2_IP = ""         # Example: Plug 2 IP address
PLUG2_TOKEN = ""  # Replace with your actual token

# Create plug instances using the ChuangmiPlug class.
plug1 = ChuangmiPlug(PLUG1_IP, PLUG1_TOKEN, model="zhimi.plug.m1")
plug2 = ChuangmiPlug(PLUG2_IP, PLUG2_TOKEN, model="zhimi.plug.m1")

# --- MQTT Callback Functions ---
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    # Subscribe to command topics for both plugs
    client.subscribe(COMMAND_TOPIC_PLUG1)
    client.subscribe(COMMAND_TOPIC_PLUG2)

def on_message(client, userdata, msg):
    topic = msg.topic
    command = msg.payload.decode().strip().upper()
    print(f"Received command '{command}' on topic '{topic}'")
    
    try:
        if topic == COMMAND_TOPIC_PLUG1:
            if command == "ON":
                plug1.on()
                response = "Plug 1 turned ON"
            elif command == "OFF":
                plug1.off()
                response = "Plug 1 turned OFF"
            else:
                response = "Unknown command for Plug 1"
            client.publish(RESPONSE_TOPIC_PLUG1, response)
        elif topic == COMMAND_TOPIC_PLUG2:
            if command == "ON":
                plug2.on()
                response = "Plug 2 turned ON"
            elif command == "OFF":
                plug2.off()
                response = "Plug 2 turned OFF"
            else:
                response = "Unknown command for Plug 2"
            client.publish(RESPONSE_TOPIC_PLUG2, response)
        else:
            print("Received command on unknown topic")
    except Exception as e:
        error_message = f"Error handling command on {topic}: {e}"
        print(error_message)
        if topic == COMMAND_TOPIC_PLUG1:
            client.publish(RESPONSE_TOPIC_PLUG1, error_message)
        elif topic == COMMAND_TOPIC_PLUG2:
            client.publish(RESPONSE_TOPIC_PLUG2, error_message)

# --- Setup MQTT Client ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
