import threading

from BlazeposeDepthaiEdge import BlazeposeDepthai
from BlazeposeRenderer import BlazeposeRenderer

from math import atan2, degrees
import sys, time, os, ffmpeg, threading
sys.path.append("../..")
from mediapipe_utils import KEYPOINT_DICT

margin_of_error_on_angle = 10 #degrees

body_position_array = []

def detect_fall(body):
    def angle_with_y(v):
        # v: 2d vector (x,y)
        # Returns angle in degree of v with y-axis of image plane

        # v[0] = x = is verschil in breedte
        # v[1] = y = is verschil in hoogte
        if v[1] == 0:
            return 90
        angle = atan2(v[0], v[1])
        return degrees(angle)

    def add_angle_to_list(angle):
        if len(body_position_array) >= 30:
            body_position_array.remove(0)
        body_position_array.append([time.time_ns(),angle])

    def person_is_on_the_ground(angle):
        return -margin_of_error_on_angle < angle < margin_of_error_on_angle

    def person_has_fallen(angle):
        add_angle_to_list(angle)

        timestamps = []
        angles = []
        for position in body_position_array:
            timestamps = timestamps + [position[0]]
            angles = angles + [position[1]]
        return (max(angles) - min(angles)) >= 45 and max(timestamps) - min(timestamps) >= 500000000 and person_is_on_the_ground(angle)

    upper_body_angle_with_y = angle_with_y(body.landmarks[KEYPOINT_DICT['nose'],:2] - (body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_hip'],:2])/2)
    lower_body_angle_with_y = angle_with_y((body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_heel'],:2])/2 - (body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_heel'],:2])/2)

    average_body_angle = (upper_body_angle_with_y + lower_body_angle_with_y) / 2

    fall = False
    if len(body_position_array) >= 30:
        fall = person_has_fallen(average_body_angle)

    return fall

# The argparse stuff has been removed to keep only the important code

tracker = BlazeposeDepthai(lm_model="lite",
                           xyz=True,
                           internal_frame_height=720)

def init_renderer():
    return BlazeposeRenderer(
                    tracker,
                    show_3d="mixed",
                    output="test.avi")
renderer = init_renderer()

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

while True:
    # Run blazepose on next frame
    frame, body = tracker.next_frame()
    if frame is None: break
    # Draw 2d skeleton
    frame = renderer.draw(frame, body)
    key = renderer.waitKey(delay=1)
    if detect_fall(body): # Dit zou normaal de opname moeten stoppen en een nieuwe moeten maken
        body_position_array = []
        #renderer.exit()
        #tracker.exit()
        new_file_name = "detection_"+str(time.time())+".avi"
        #os.rename("test.avi",new_file_name) #Dit zou normaal de laatste nieuwe detectie moeten geven met tijd en datum

        #thread = threading.Thread(target=trim_and_send, args=(new_file_name))
        #thread.start()
        #thread.join()

        #renderer = init_renderer()
        #Hier moet de file nog bijgeknipt (laatste 10 sec) en verstuurd worden in een thread

    if key == 27 or key == ord('q'):
        renderer.exit() #Misschien werkt het zo beter
        tracker.exit()
        break

renderer.exit()
tracker.exit()

# Hier is een voorbeeld van positie bepalen, dat in een array bijhouden met de timestamps en dan kijken hoe snel die valt
# https://github.com/geaxgx/depthai_blazepose/blob/main/examples/semaphore_alphabet/demo.py

# Knippen van de video ffmpeg
# https://stackoverflow.com/questions/68403072/how-can-i-cut-a-video-to-a-certain-length-and-add-an-intro-video-to-it-using-ffm