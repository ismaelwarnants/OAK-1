import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read('config.txt')

server_ip = str(config['NODE']['ServerIP'])

# This is the Publisher
def send(message):
    client = mqtt.Client()
    client.connect(server_ip,1883,60)
    print("Mqtt is ready to send: "+message)
    client.publish("node/detection", message)
    client.disconnect()