import threading, cv2

from BlazeposeDepthaiEdge import BlazeposeDepthai
from BlazeposeRenderer import BlazeposeRenderer

from math import atan2, degrees
import sys, time, os, ffmpeg, datetime
sys.path.append("../..")
from mediapipe_utils import KEYPOINT_DICT

margin_of_error_on_angle = 10 #degrees
testing = True
max_length_of_array = 30
body_position_array = []

def detect_fall(body):
    def angle_with_x(v):
        # v: 2d vector (x,y)
        # Returns angle in degree of v with x-axis of image plane

        # v[0] = x = is verschil in breedte
        # v[1] = y = is verschil in hoogte
        if v[0] == 0:
            return 0
        angle = atan2(v[1], v[0])
        return degrees(angle)

    def add_angle_to_list(angle):
        #print("Length: "+ str(len(body_position_array)))
        if len(body_position_array) >= max_length_of_array:
            try:
                body_position_array.pop(0)
            except:
                print("List is empty")
        body_position_array.append([time.time_ns(),angle])

    def person_is_on_the_ground(angle):
        return -margin_of_error_on_angle < angle < margin_of_error_on_angle

    def person_has_fallen(angle):
        if not testing:
            add_angle_to_list(angle)

        timestamps = []
        angles = []

        if testing:
            return person_is_on_the_ground(angle)
        else:
            for position in body_position_array:
                timestamps.append(position[0])
                angles.append(position[1])
            angle_diff = (max(angles) - min(angles))
            time_diff = max(timestamps) - min(timestamps)
            fall = person_is_on_the_ground(angle)
            print("Angle: " + str(angle_diff) + "degrees \t Time: " + str(time_diff/1000000) + "ms\t Fall: "+ str(fall))
            print("Angles: \n"+str(angles))
            print("Timestamps: \n"+str(timestamps))
            #return (max(angles) - min(angles)) >= 70 and max(timestamps) - min(timestamps) >= 500000000 and person_is_on_the_ground(angle)
            return angle_diff>=45 and time_diff>= 500000000 and fall

    upper_body_angle_with_x = 0
    lower_body_angle_with_x = 0

    try:
        upper_body_angle_with_x = angle_with_x(body.landmarks[KEYPOINT_DICT['nose'],:2] - (body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_hip'],:2])/2)
        print("Estimated angle upper body:" + str(upper_body_angle_with_x))
    except:
        print("No upperbody landmarks detected")
    try:
        lower_body_angle_with_x = angle_with_x((body.landmarks[KEYPOINT_DICT['left_hip'],:2]+body.landmarks[KEYPOINT_DICT['right_hip'],:2])/2 - (body.landmarks[KEYPOINT_DICT['left_heel'],:2]+body.landmarks[KEYPOINT_DICT['right_heel'],:2])/2)
        print("Estimated angle lower body:" + str(lower_body_angle_with_x))
    except:
        print("No lowerbody landmarks detected")

    average_body_angle = (upper_body_angle_with_x) #+ abs(lower_body_angle_with_x)) / 2 # bij een kleine verschuiving over naar onder x-as wordt ineens een bijna 360° overgang

    fall = False
    if len(body_position_array) >= max_length_of_array and (not testing):
        fall = person_has_fallen(average_body_angle)
    else:
        fall = person_has_fallen(average_body_angle)

    return fall

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
    old_time = time.time_ns() / 1000000000

    while not fall_detected:
        new_time = time.time_ns()/1000000000
        time_diff = new_time-old_time
        old_time = new_time
        # print("Delay per cycle: "+str(time_diff))

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