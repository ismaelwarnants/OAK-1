import live_fall_test, os, datetime


def run():
    live_fall_test.run()
    rename_file()

def rename_file():
    new_file_name = "detection_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".avi"
    try:
        os.rename("test.avi",
                  new_file_name)  # Dit zou normaal de laatste nieuwe detectie moeten geven met tijd en datum
    except:
        print("Error while trying to rename file")

def get_total_video_lentgh(video_file_name):
    #https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
    import cv2
    video = cv2.VideoCapture(video_file_name)

    duration = video.get(cv2.CAP_PROP_POS_MSEC)

    return duration

def trim_last_10_sec_from_video_file(video_file_name):
    input = ffmpeg.input(video_file_name)
    end_time = get_total_video_lentgh(video_file_name)
    start_time = end_time - 10
    trimmed = ffmpeg.trim(input, start=start_time,end=end_time)
    out = ffmpeg.output(trimmed, video_file_name)

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
    while True:
        run()