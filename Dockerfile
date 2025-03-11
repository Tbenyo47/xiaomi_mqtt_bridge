# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bridge script into the container
COPY xiaomi_mqtt_bridge.py .

# Set the command to run the bridge script
CMD ["python", "xiaomi_mqtt_bridge.py"]
