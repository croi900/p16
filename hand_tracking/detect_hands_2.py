import threading
import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

from aop import angle_between_points

INDEX_FINGER_IDX = 8
THUMB_IDX = 4

videoCap = cv2.VideoCapture("udp://192.168.34.119:1234")

# Mediapipe hands with GPU support enabled
handSolution = mp.solutions.hands
hands = handSolution.Hands(static_image_mode=False,
                           max_num_hands=2,

                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)

FIST_THRESHOLD = 100

# Shared data structures
frame_buffer = deque([], maxlen=1)
touch_buffer = deque([], maxlen=10)
arm_pos_buf = deque([], maxlen=10)
pinch_pos_buf = deque([], maxlen=10)
pinch_buffer = deque([], maxlen=2)
arm_buffer = deque([], maxlen=2)

next_pinch_time = time.time()
pinch_count = 0


from scipy.interpolate import interp1d
mx = interp1d([0.1,0.9],[0,1], bounds_error=False)
my = interp1d([0.1,0.9],[0,1], bounds_error=False)
def clamp(x, a, b):
    return max(min(x, b), a)

def execute_click(points,w,h,pinching):
    x, y = points[0][0], points[0][1]
    print(w,h)
    x = clamp(x, 0.1,0.9)
    y = clamp(y, 0.1,0.9)
    x = mx(x)
    y = my(y)
    print(x,y)
    x = int(x * 640*1.3)
    y = int(y * 480*1.3)

    pyautogui.moveTo(x, y)
    if(pinching):
        pyautogui.click()


def fist(points):
    def normalized_pairwise_distance(points):
        dists = []
        for p1 in points:
            for p2 in points:
                dists.append((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        sums = (np.array(dists) / np.max(dists)).sum()
        return sums

    f1 = normalized_pairwise_distance(points[1:5])
    f2 = normalized_pairwise_distance(points[5:9])
    f3 = normalized_pairwise_distance(points[9:13])
    f4 = normalized_pairwise_distance(points[13:16])
    f5 = normalized_pairwise_distance(points[17:21])

    return (f1 + f2 + f3 + f4 + f5) / 5


def pinch(points):
    angle_3d = angle_between_points(points[5], points[6], points[8])
    return angle_3d


def calculate_derivative(points):
    if len(points) != 2:
        return 0

    p1 = np.array(points[0])
    p2 = np.array(points[1])
    derivative = p2 - p1
    return np.log10(np.linalg.norm(derivative))


# UDP receiving thread function
def receive_frames():
    global frame_buffer
    while True:
        success, img = videoCap.read()

        if success:
            frame_buffer.append(img)

        time.sleep(0.01)  # Slight delay to prevent overwhelming the loop


# Frame processing thread function
def process_frames():
    global pinch_count, next_pinch_time
    while True:
        if frame_buffer:
            img = frame_buffer.popleft()

            h, w, c = img.shape
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            recHands = hands.process(imgRGB)

            if recHands.multi_hand_landmarks:
                for hand in recHands.multi_hand_landmarks:
                    coords = []

                    for datapoint_id, point in enumerate(hand.landmark):
                        coords.append([point.x, point.y, point.z])
                        x, y = int(point.x * w), int(point.y * h)
                        cv2.circle(img, (x, y), 2, (255, 0, 255), cv2.FILLED)

                    arm_pos_buf.append(coords[0])
                    pinch_pos_buf.append(coords[8])

                    touch_buffer.append(
                        angle_between_points(coords[8], coords[5], coords[0])
                    )

                    r_arm1 = np.sum(np.array(list(arm_pos_buf)[:5])) / 5
                    r_arm2 = np.sum(np.array(list(arm_pos_buf)[5:])) / 5

                    r_pinch1 = np.sum(np.array(list(pinch_pos_buf)[:5])) / 5
                    r_pinch2 = np.sum(np.array(list(pinch_pos_buf)[5:])) / 5

                    pinch_speed = calculate_derivative([r_pinch1, r_pinch2])
                    arm_speed = calculate_derivative([r_arm1, r_arm2])

                    if pinch_speed > -2 and arm_speed < -2.5:
                        pinch_count += 1

                    if pinch_count > 2:
                        next_pinch_time = time.time() + 0.45
                        pinch_count = 0
                        execute_click(coords, w, h, True)

                    execute_click(coords, w, h, False)

            cv2.imshow("CamOutput", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(0.01)  # Avoid high CPU usage


# Start the receiving thread
receive_thread = threading.Thread(target=receive_frames)
receive_thread.daemon = True
receive_thread.start()

# Start the processing thread
process_thread = threading.Thread(target=process_frames)
process_thread.start()

# Keep main thread alive
while True:
    time.sleep(1)
