# Horus – Sistema de Detección Automática de Armas


## Tabla de Contenidos

- [Descripción](#descripción)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Configuración](#configuración)
  - [Ajustes de la ESP32](#ajustes-de-la-esp32)
  - [Ajustes del modelo YOLOv8](#ajustes-del-modelo-yolov8)
- [Ejecución](#ejecución)
- [Resultados](#resultados)

---

## Descripción

**Horus** es un sistema de detección automática de armas en vídeo utilizando un **ESP32-CAM** y un modelo **YOLOv8** de visión por computadora. El sistema realiza inferencias en tiempo real y activa una señal física (buzzer o LED) al detectar armas en la escena.  

Requisitos:  
- Un **dispositivo que ejecute el modelo YOLOv8**.  
- Un **broker MQTT** para comunicar las detecciones a la placa ESP32.  

---

## Estructura del repositorio

### 1. `esp32cam-rtsp`

Basado en el [repositorio original de rzeldent](https://github.com/rzeldent/esp32cam-rtsp), este módulo contiene el código para la **placa ESP32-CAM**, que:  
- Genera un **stream de vídeo** en tiempo real desde la cámara integrada.  
- Integra **MQTT** para recibir notificaciones del modelo y activar la señal física (buzzer o LED).  

### 2. `yolov8`

Contiene el **modelo YOLOv8 de Ultralytics** entrenado para el caso de uso específico de detección de armas. Incluye:  
- Funcionalidad **MQTT** para enviar detecciones al ESP32.  
- Código de inferencia y visualización de **bounding boxes** sobre los objetos detectados.

---

## Configuración

### Ajustes de la ESP32

En `esp32cam-rtsp/include/settings.h` debes configurar la conexión Wi-Fi y el broker MQTT:

```cpp
#define WIFI_SSID "nombre-wifi"
#define WIFI_PASSWORD "contraseña-wifi"
#define MQTT_BROKER_IP "IP-del-broker-mqtt"
```

En `yolov8/ultralytics/yolo/utils/mqtt.py` debes indicar la dirección del broker MQTT:

```python
def connect_client():
    mqtt_broker = "IP-del-broker-mqtt"
    client = mqtt.Client(client_id="yolo")
    client.connect(mqtt_broker, 1883)
    return client
```

Nota:
- Si usas un broker local, la ESP32 debe estar en la misma red Wi-Fi que el dispositivo que ejecuta el modelo.
- Puede ser necesario desactivar el firewall o crear excepciones para permitir la comunicación.

## Ejecución

1. **Subir el código a la ESP32-CAM**.  
2. Acceder a la **IP de la placa** desde un navegador para obtener la **URL del stream** de la cámara.  
3. Desde la carpeta `yolov8`, lanzar el modelo con:

```bash
yolo detect predict model=weights/yolo.pt source=URL-stream show
```

- Aparecerá una ventana de vídeo con la imagen de la cámara ESP32 y las detecciones.

- Cuando el modelo detecta un arma:

    - Se dibuja un bounding box rojo sobre el objeto.

    - Se envía un mensaje MQTT.

    - La ESP32 activa la señal física (buzzer o LED), por defecto en el pin 33, modificable desde main.cpp.

## Resultados

En esta carpeta de Drive se encuentran dos videos que muestran la demo del sistema en funcionamiento. Puedes verlos [aquí](https://drive.google.com/drive/folders/1wxoww2DgPTCWcgg2zoLQW8HTGOUgGXNf?usp=drive_link).

En ambos videos se muestran tres elementos principales:
1. **Vista general:** Se observa a la persona que porta el dispositivo. (En el primer video también aparece otra persona mostrando distintos objetos). 
2. **Vista de la ESP32:** Se visualizan las **bounding boxes** sobre los objetos cuando el sistema detecta un arma.  
3. **Consola del modelo:** Muestra en tiempo real en la línea de comandos si se ha realizado una detección o no.

**Detalles de los videos:**

- **DemoHorus:** Dos personas de pie. Uno sostiene el dispositivo ESP32-CAM mientras la otra persona muestra un mando (objeto inocuo) y una pistola. El sistema detecta correctamente el arma y activa la señal física (buzzer).  

- **DemoHorusMesa:** Vista desde la ESP32 sobre una mesa con varios objetos, incluyendo un arma. El sistema detecta correctamente el arma y activa la señal física (buzzer).

