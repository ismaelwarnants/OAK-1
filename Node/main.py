import fall_detection, os, datetime, sftp_send, mqtt_send, configparser

config = configparser.ConfigParser()
config.read('config.txt')

server_ip = str(config['NODE']['ServerIP'])
room_nr = str(config['NODE']['RoomNR'])

def run():
    fall_detection.run()

    # When the fall detection is finished, the message and recording are sent to the server
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    new_file_name = "detection_" + timestamp + ".mp4"
    rename_file(new_file_name)
    trim_and_send(timestamp,new_file_name)

def rename_file(new_file_name):
    try:
        os.rename("test.mp4", new_file_name)
    except Exception as e:
        print("Error while trying to rename file: "+str(e))

def get_total_video_lentgh(video_file_name):
    # Source: https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
    import subprocess, json

    result = subprocess.check_output(
        f'ffprobe -show_streams -select_streams v:0 -of json "{video_file_name}"',
        shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = fields['duration']
    return float(duration)

def trim_last_20_sec_from_video_file(video_file_name):
    duration = 0
    try:
        duration = get_total_video_lentgh(video_file_name)
        print("Total video length: " + str(duration))
    except Exception as e:
        print("Could not determine video length: " + str(e))

    if duration > 20:
        # Source: https://gist.github.com/georgechalhoub/e9c1c50507f651c8af90c5f40e8376c7
        print("Video too long, clipping video...")
        end_time = duration + 1
        start_time = duration - 20
        os.system("ffmpeg -i " + str(video_file_name) + " -ss  " + str(start_time) + " -to " + str(end_time) + " -c copy " + "clipped_" + str(video_file_name))
        try:
            os.remove(str(video_file_name))
            os.rename("clipped_" + str(video_file_name), str(video_file_name))
        except Exception as e:
            print("Error while trying to rename file: " + str(e))

def send_notification_and_video_file(timestamp,video_file_name):
    mqtt_send.send(format_message(timestamp,video_file_name))
    sftp_send.send(video_file_name)

def trim_and_send(timestamp,video_file_name):
    trim_last_20_sec_from_video_file(video_file_name)
    send_notification_and_video_file(timestamp,video_file_name)

def format_message(timestamp, video_file_name):
    # The message is sent over mqtt in the json format
    message = '{"timestamp": "'+str(timestamp)+'", "room_nr": "'+str(room_nr)+'", "video_file_name": "'+str(video_file_name)+'"}'
    return str(message)

if __name__ == '__main__':
    try:
        # In case an old video file was still present, it will be deleted before continuing
        os.remove("test.mp4")
    except:
        print("No leftover file to remove, continuing...")

    while True:
        run()