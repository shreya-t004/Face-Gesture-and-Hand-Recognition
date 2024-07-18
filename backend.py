from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize camera
cap = cv2.VideoCapture(0)

# Function to perform required action based on gesture
def perform_action(action):
    if action == 'up':
        # Perform action for increasing volume, turning on lights, etc.
        print("Volume Up")
    elif action == 'down':
        # Perform action for decreasing volume, turning off lights, etc.
        print("Volume Down")
    elif action == 'left':
        # Perform action for moving to previous track, changing channel, etc.
        print("Previous")
    elif action == 'right':
        # Perform action for moving to next track, changing channel, etc.
        print("Next")

# Function to detect gesture from a frame
def detect_gesture(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding the image to make binary
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the maximum area
    if contours:
        max_area_contour = max(contours, key=cv2.contourArea)

        # Find convex hull
        hull = cv2.convexHull(max_area_contour, returnPoints=False)

        # Find convexity defects
        defects = cv2.convexityDefects(max_area_contour, hull)

        # Count the number of defects
        count_defects = 0
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                if d > 10000:  # Filter defects based on distance
                    count_defects += 1
        # Detect gestures based on the number of defects
        if count_defects == 1:
            return 'up'
        elif count_defects == 2:
            return 'down'
        elif count_defects == 3:
            return 'left'
        elif count_defects == 4:
            return 'right'
    return 'no gesture'

# Route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to receive frames from the frontend and perform gesture detection
@socketio.on('detect_gesture')
def handle_frame(frame_data):
    # Decode base64 frame
    frame_bytes = base64.b64decode(frame_data.split(",")[1])

    # Convert bytes to numpy array
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect gesture from the frame
    gesture = detect_gesture(frame)

    # Perform action based on detected gesture
    perform_action(gesture)

    # Emit detected gesture to the frontend
    emit('gesture_detected', gesture)

if __name__ == '__main__':
    socketio.run(app, debug=True)
