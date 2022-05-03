'''import cv2
#Initialize video capture
cap = cv2.VideoCapture(0)
#scaling factor
scaling_factor = 0.5
# Loop until you hit the Esc key
while True:
    # Capture the current frame
    ret, frame = cap.read()
# Resize the frame
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
# Display the image
    cv2.imshow('Webcam', frame)
# Detect if the Esc key has been pressed
    c = cv2.waitKey(1)
    if c == 27:
        break
# Release the video capture object
cap.release()
# Close all active windows
cv2.destroyAllWindows()'''

import cv2

capture = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
videoWriter = cv2.VideoWriter('video.avi', fourcc, 20.0, (1280, 720))

while (True):

    ret, frame = capture.read()

    if ret:
        cv2.imshow('video', frame)
        videoWriter.write(frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()
videoWriter.release()

cv2.destroyAllWindows()