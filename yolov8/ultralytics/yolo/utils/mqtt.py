import socket
import paho.mqtt.client as mqtt

lastState = None
falseCount = 0
noAlert = False

def get_ip():
    #For a lack of a better method of getting the actual WiFi IP and not other interfaces IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('10.0.0.0', 1)) #Test connection
    IP = s.getsockname()[0]
    return IP

def connect_client():
    mqtt_broker = "IP-del-broker-mqtt"  # Gets the IP address
    client = mqtt.Client(client_id="yolo")
    client.connect(mqtt_broker, 1883)
    return client

client = connect_client()
def publish_handler(state):
    global lastState, falseCount, client, noAlert

    #Keeps track of the numbers of falses in a row
    if state:
        falseCount = 0
    else:
        falseCount += 1

    #Only sends the alert if there is a False in topic
    if state != lastState:
        if state:
            client.publish("detection/alert",state)
            noAlert = False
    
    #Sent a no detection alert only if there has been at least 5 falses in a row and there isnt already a False in topic
    if falseCount >= 5 and noAlert == False:
            client.publish("detection/alert",state)
            noAlert = True #Ensures no repeated Falses emmited

    lastState = state