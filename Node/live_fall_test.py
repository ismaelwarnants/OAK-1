from math import atan2, degrees
import sys, time, os, ffmpeg, datetime, threading, cv2
sys.path.append("../..")
sys.path.append('depthai_blazepose')
from depthai_blazepose.mediapipe_utils import KEYPOINT_DICT
from depthai_blazepose.BlazeposeDepthaiEdge import BlazeposeDepthai
from depthai_blazepose.BlazeposeRenderer import BlazeposeRenderer

margin_of_error_on_angle = 10 #degrees

#body_position_array = []

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

    '''def add_angle_to_list(angle):
        if len(body_position_array) >= 30:
            body_position_array.remove(0)
        body_position_array.append([time.time_ns(),angle])'''

    def person_is_on_the_ground(angle):
        return -margin_of_error_on_angle < angle < margin_of_error_on_angle

    def person_has_fallen(angle):
        #add_angle_to_list(angle)

        timestamps = []
        angles = []
        '''for position in body_position_array:
            timestamps = timestamps + [position[0]]
            angles = angles + [position[1]]'''
        return person_is_on_the_ground(angle)#(max(angles) - min(angles)) >= 45 and max(timestamps) - min(timestamps) >= 500000000 and person_is_on_the_ground(angle)

    upper_body_angle_with_y = 0
    lower_body_angle_with_y = 0

    try:
        upper_body_angle_with_y = angle_with_y(body.landmarks[KEYPOINT_DICT['nose'],:2] - (body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_hip'],:2])/2)
    except:
        print("No upperbody landmarks detected")
    try:
        lower_body_angle_with_y = angle_with_y((body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_heel'],:2])/2 - (body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_heel'],:2])/2)
    except:
        print("No lowerbody landmarks detected")

    average_body_angle = (upper_body_angle_with_y + lower_body_angle_with_y) / 2

    fall = False
    #if len(body_position_array) >= 30:
        #fall = person_has_fallen(average_body_angle)

    return person_has_fallen(average_body_angle)

# The argparse stuff has been removed to keep only the important code

def init_tracker():
    return BlazeposeDepthai(lm_model="lite",
                               xyz=True,
                               internal_frame_height=720)

def init_renderer(tracker):
    return BlazeposeRenderer(
                    tracker,
                    show_3d="mixed",
                    output="test.mp4")

def run():
    fall_detected = False
    tracker = init_tracker()
    renderer = init_renderer(tracker)
    while not fall_detected:
        # Run blazepose on next frame
        frame, body = tracker.next_frame()
        if frame is None: break
        # Draw 2d skeleton
        frame = renderer.draw(frame, body)

        if body:
            fall_detected = detect_fall(body)
            letter = ''
            if fall_detected:
                letter = 'T'
            else:
                letter = 'F'
            cv2.putText(frame, letter, (frame.shape[1] // 2, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 190, 255), 3)
        key = renderer.waitKey(delay=1)



    renderer.exit()
    tracker.exit()



# Hier is een voorbeeld van positie bepalen, dat in een array bijhouden met de timestamps en dan kijken hoe snel die valt
# https://github.com/geaxgx/depthai_blazepose/blob/main/examples/semaphore_alphabet/demo.py

# Knippen van de video ffmpeg
# https://stackoverflow.com/questions/68403072/how-can-i-cut-a-video-to-a-certain-length-and-add-an-intro-video-to-it-using-ffm