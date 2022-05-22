from math import atan2, degrees
import sys, time, os, ffmpeg, datetime, threading, cv2
sys.path.append("../..")
sys.path.append('depthai_blazepose')
from depthai_blazepose.mediapipe_utils import KEYPOINT_DICT
from depthai_blazepose.BlazeposeDepthaiEdge import BlazeposeDepthai
from depthai_blazepose.BlazeposeRenderer import BlazeposeRenderer

margin_of_error_on_angle = 10 #degrees
demo = True

# This file is an adaptation from this source:
# https://github.com/geaxgx/depthai_blazepose/blob/main/examples/semaphore_alphabet/demo.py

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

    def person_has_fallen(angle):
        return -margin_of_error_on_angle < abs(angle)-90 < margin_of_error_on_angle

    angle = 0
    if demo: # This if statement can be removed if the demo is not necessary
        arm_angle = 0
        try:
            arm_angle = angle_with_y(
                body.landmarks[KEYPOINT_DICT['left_wrist'], :2] - body.landmarks[KEYPOINT_DICT['left_shoulder'], :2])
        except:
            print("No person in frame")
        angle = arm_angle

    else:
        upper_body_angle_with_y = 0
        lower_body_angle_with_y = 0

        try:
            upper_body_angle_with_y = angle_with_y(body.landmarks[KEYPOINT_DICT['nose'], :2] - (
                    body.landmarks[KEYPOINT_DICT['left_hip'], :2] + body.landmarks[KEYPOINT_DICT['right_hip'], :2]) / 2)
        except:
            print("No upperbody landmarks detected")
        try:
            lower_body_angle_with_y = angle_with_y(
                (body.landmarks[KEYPOINT_DICT['left_hip'], :2] + body.landmarks[KEYPOINT_DICT['right_heel'], :2]) / 2
                - (body.landmarks[KEYPOINT_DICT['left_hip'], :2] + body.landmarks[KEYPOINT_DICT['right_heel'], :2]) / 2)
        except:
            print("No lowerbody landmarks detected")

        angle = (upper_body_angle_with_y + lower_body_angle_with_y) / 2

    return person_has_fallen(angle) #person_has_fallen(average_body_angle)

def init_tracker():
    return BlazeposeDepthai(lm_model="lite",
                               xyz=True,
                               internal_frame_height=480)

def init_renderer(tracker):
    return BlazeposeRenderer(
                    tracker,
                    show_3d="mixed",
                    output="test.mp4")

def run():
    tracker = init_tracker()
    renderer = init_renderer(tracker)
    old_time = 0
    time_diff = 0 # This measures the time difference, so the recording will continue for 10 seconds after the fall

    while not (time_diff > 10):
        if old_time != 0:
            new_time = time.time()
            time_diff = new_time-old_time

        # Run blazepose on next frame
        frame, body = tracker.next_frame()
        if frame is None: break
        # Draw 2d skeleton
        frame = renderer.draw(frame, body)

        if body:
            fall_detected = detect_fall(body)
            letter = ''
            if fall_detected:
                if old_time == 0:
                    old_time = time.time()
                letter = 'T'
            else:
                letter = 'F'
            cv2.putText(frame, letter, (frame.shape[1] // 2, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 190, 255), 3)
            key = renderer.waitKey(delay=1)

    renderer.exit()
    tracker.exit()
