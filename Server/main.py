import paho.mqtt.client as mqtt
from os.path import exists
import telegrambot, time, threading, configparser, json, sql

config = configparser.ConfigParser()
config.read('config.txt')

username = str(config['SERVER']['ServerUsername'])
video_destination = str(config['SERVER']['VideoDestination'])

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("node/detection")

def on_message(client, userdata, msg):
  if msg.payload.decode() != "":
    print(str(msg.payload.decode()))
    telegrambot.send_message(format_message(str(msg.payload.decode())))
    store_detection(str(msg.payload.decode()))
    thread = threading.Thread(target=send_video, args=(str(msg.payload.decode()), ))
    thread.start()
    #client.disconnect()

def send_video(message):
    video_file_name = json.JSONDecoder().decode(message)["video_file_name"]
    while True:
        time.sleep(0.5)
        file_ready = exists("/home/"+username+"/"+video_destination+"/"+video_file_name)
        if file_ready:
            time.sleep(2)
            telegrambot.send_video("/home/"+username+"/"+video_destination+"/"+video_file_name)
            break

def format_message(message):
    room_nr = json.JSONDecoder().decode(message)["room_nr"]
    timestamp = json.JSONDecoder().decode(message)["timestamp"]
    return "A person fell at "+timestamp+" in room "+room_nr

def store_detection(message):
    timestamp = json.JSONDecoder().decode(message)["timestamp"]
    room_nr = json.JSONDecoder().decode(message)["room_nr"]
    video_file_name = json.JSONDecoder().decode(message)["video_file_name"]
    sql.add_detection(timestamp,room_nr,video_file_name)

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

if __name__ == '__main__':
    main()