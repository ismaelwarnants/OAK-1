import fall_detection, os, datetime, time, ffmpeg


def run():
    fall_detection.run()

    new_file_name = "detection_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".avi"
    rename_file(new_file_name)
    trim_and_send(new_file_name)

def rename_file(new_file_name):

    try:
        os.rename("test.avi", new_file_name)  # Dit zou normaal de laatste nieuwe detectie moeten geven met tijd en datum
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

    if duration > 10:
        print("Video too long, clipping video...")
        end_time = duration + 1
        start_time = duration - 10
        os.system("ffmpeg -i " + str(video_file_name) + " -ss  " + str(start_time) + " -to " + str(end_time) + " -c copy " + "Clipped_" + str(video_file_name))

        '''input = ffmpeg.input(video_file_name)
        
        trimmed = ffmpeg.trim(input, start=start_time,end=end_time)
        out = ffmpeg.output(trimmed, video_file_name)'''

def trim_and_send(video_file_name):
    trim_last_10_sec_from_video_file(video_file_name)
    # Send de video file code komt hier

def finish():
    print()
    # thread = threading.Thread(target=trim_and_send, args=(new_file_name))
    # thread.start()
    # thread.join()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        os.remove("test.avi") # In case an old video file was still present, it will be deleted before continuing
    except:
        print("No leftover file to remove, continuing...")

    while True:
        run()