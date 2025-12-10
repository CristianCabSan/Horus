# Horus – Automatic Weapon Detection System

## Table of Contents

- [Description](#description)  
- [Repository Structure](#repository-structure)  
- [Setup](#setup)  
  - [ESP32 Settings](#esp32-settings)  
  - [YOLOv8 Model Settings](#yolov8-model-settings)  
- [Execution](#execution)  
- [Results](#results)  
- [Disclaimer](#disclaimer)  

---

## Description

**Horus** is an automatic weapon detection system in video using an **ESP32-CAM** and a **YOLOv8** computer vision model. The system performs real-time inference and triggers a physical signal (buzzer or LED) when weapons are detected in the scene.  

Requirements:  
- A **device running the YOLOv8 model**.  
- An **MQTT broker** to communicate detections to the ESP32 board.  
- An **ESP32-Wrover board with a camera** (or equivalent board with an integrated camera).

---

## Repository Structure

### 1. `esp32cam-rtsp`

Based on the [original repository by rzeldent](https://github.com/rzeldent/esp32cam-rtsp), this module contains the code for the **ESP32-CAM board**, which:  
- Streams **real-time video** from the integrated camera.  
- Integrates **MQTT** to receive model notifications and trigger the physical signal (buzzer or LED).  

### 2. `yolov8`

Contains the **Ultralytics YOLOv8 model** trained for the specific use case of weapon detection. Includes:  
- **MQTT functionality** to send detections to the ESP32.  
- Inference code and visualization of **bounding boxes** over detected objects.

---

## Setup

### ESP32 Settings

In `esp32cam-rtsp/include/settings.h`, configure the Wi-Fi connection and MQTT broker:

```cpp
#define WIFI_SSID "wifi-name"
#define WIFI_PASSWORD "wifi-password"
#define MQTT_BROKER_IP "mqtt-broker-ip"
```

In yolov8/ultralytics/yolo/utils/mqtt.py, set the MQTT broker address:
```python
def connect_client():
    mqtt_broker = "mqtt-broker-ip"
    client = mqtt.Client(client_id="yolo")
    client.connect(mqtt_broker, 1883)
    return client
```

**Note:**  
- If using a local broker, the ESP32 must be on the same Wi-Fi network as the device running the model.  
- You may need to disable the firewall or create exceptions to allow communication.

---

## Execution

1. **Upload the code to the ESP32-CAM.**  
2. Access the **board’s IP** from a browser to get the **camera stream URL**.  
3. From the `yolov8` folder, run the model with:

```bash
yolo detect predict model=weights/yolo.pt source=<stream-URL> show
```

- A video window will appear showing the ESP32 camera feed and detections.  

- When the model detects a weapon:  
    - A red bounding box is drawn around the object.
      
    - An MQTT message is sent.
      
    - The ESP32 triggers the physical signal (buzzer or LED), by default on pin 33, configurable in `main.cpp`.

---

## Disclaimer

This project was developed during my time at the DeepKnowledge group of the University of Sevilla as a research technician. Part of the work was performed by other team members; my main contribution was the implementation of the model on the ESP32 and the MQTT connection.
