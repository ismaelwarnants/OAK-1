import paho.mqtt.client as mqtt

server_ip = "192.168.1.100"

# This is the Publisher
def send(message):
    client = mqtt.Client()
    client.connect(server_ip,1883,60)
    client.publish("node/detection", message)
    client.disconnect()
