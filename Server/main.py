import paho.mqtt.client as mqtt
from os.path import exists
import telegrambot

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("node/detection")

def on_message(client, userdata, msg):
  if msg.payload.decode() != "":
    file_ready = False
    while not file_ready:
        file_ready = exists("~/demo/"+msg.payload.decode())

    telegrambot.send_message(msg.payload.decode())
    telegrambot.send_video("~/demo/"+msg.payload.decode())
    #client.disconnect()

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

if __name__ == '__main__':
    main()