from BlazeposeDepthaiEdge import BlazeposeDepthai
from BlazeposeRenderer import BlazeposeRenderer

# The argparse stuff has been removed to keep only the important code

tracker = BlazeposeDepthai(lm_model="lite",
                           xyz=True,
                           internal_frame_height=720)

renderer = BlazeposeRenderer(
                tracker,
                show_3d="mixed",
                output="test.avi")

while True:
    # Run blazepose on next frame
    frame, body = tracker.next_frame()
    if frame is None: break
    # Draw 2d skeleton
    frame = renderer.draw(frame, body)
    key = renderer.waitKey(delay=1)
    if key == 27 or key == ord('q'):
        break
renderer.exit()
tracker.exit()

# Hier is een voorbeeld van positie bepalen, dat in een array bijhouden met de timestamps en dan kijken hoe snel die valt
# https://github.com/geaxgx/depthai_blazepose/blob/main/examples/semaphore_alphabet/demo.py

# Knippen van de video ffmpeg
# https://stackoverflow.com/questions/68403072/how-can-i-cut-a-video-to-a-certain-length-and-add-an-intro-video-to-it-using-ffm