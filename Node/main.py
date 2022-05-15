import live_fall_test, os, datetime, time, ffmpeg, sftp_send, mqtt_send

room_nr = 12


def run():
    live_fall_test.run()
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    new_file_name = "detection_" + timestamp + ".mp4"
    rename_file(new_file_name)
    trim_and_send(timestamp,new_file_name)

def rename_file(new_file_name):
    try:
        os.rename("test.mp4", new_file_name)  # Dit zou normaal de laatste nieuwe detectie moeten geven met tijd en datum
    except Exception as e:
        print("Error while trying to rename file: "+str(e))

def get_total_video_lentgh(video_file_name):
    #https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
    import subprocess, json

    result = subprocess.check_output(
        f'ffprobe -show_streams -select_streams v:0 -of json "{video_file_name}"',
        shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = fields['duration']
    return float(duration)

def trim_last_10_sec_from_video_file(video_file_name):
    duration = 0
    try:
        duration = get_total_video_lentgh(video_file_name)
        print("Total video length: " + str(duration))
    except Exception as e:
        print("Could not determine video length: " + str(e))

    if duration > 20:
        # https://gist.github.com/georgechalhoub/e9c1c50507f651c8af90c5f40e8376c7
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
    mqtt_send.send(video_file_name) #This will become a json file
    sftp_send.send(video_file_name)

def trim_and_send(timestamp,video_file_name):
    trim_last_10_sec_from_video_file(video_file_name)
    send_notification_and_video_file(timestamp,video_file_name)

def finish():
    print()
    # thread = threading.Thread(target=trim_and_send, args=(new_file_name))
    # thread.start()
    # thread.join()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        os.remove("test.mp4") # In case an old video file was still present, it will be deleted before continuing
    except:
        print("No leftover file to remove, continuing...")

    while True:
        run()