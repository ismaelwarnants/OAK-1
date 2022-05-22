import paho.mqtt.client as mqtt
from os.path import exists
import telegrambot, time, threading, configparser

config = configparser.ConfigParser()
config.read('config.txt')

username = str(config['NODE']['ServerUsername'])
video_destination = str(config['NODE']['VideoDestination'])

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("node/detection")

def on_message(client, userdata, msg):
  if msg.payload.decode() != "":
    print(str(msg.payload.decode()))
    telegrambot.send_message(str(msg.payload.decode()))
    thread = threading.Thread(target=send_video, args=(str(msg.payload.decode()), ))
    thread.start()
    #client.disconnect()

def send_video(msg):
    while True:
        time.sleep(0.5)
        file_ready = exists("/home/"+username+"/"+video_destination+"/"+msg)
        if file_ready:
            time.sleep(2)
            telegrambot.send_video("/home/"+username+"/"+video_destination+"/"+msg, supports_streaming=True)
            break

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

if __name__ == '__main__':
    main()