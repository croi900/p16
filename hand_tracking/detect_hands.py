"""
dedicating this code to teo
"""

import time
from subprocess import call
from collections import deque
import cv2
import mediapipe as mp
import numpy as np
from aop import angle_between_points, angle_between_points_2d
from scipy.spatial.distance import squareform, pdist
import pyautogui

INDEX_FINGER_IDX = 8
THUMB_IDX = 4

videoCap = cv2.VideoCapture(0)

handSolution = mp.solutions.hands
hands = handSolution.Hands()

FIST_TRESHOLD = 100
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
                dists.append((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        sums = (np.array(dists) / np.max(dists)).sum()
        return sums

    f1 = normalized_pairwise_distance(points[1:5])
    f2 = normalized_pairwise_distance(points[5:9])
    f3 = normalized_pairwise_distance(points[9:13])
    f4 = normalized_pairwise_distance(points[13:16])
    f5 = normalized_pairwise_distance(points[17:21])

    return (f1 + f2 + f3 + f4 + f5)/5

def pinch(points):
    angle408 = angle_between_points(points[4], points[0], points[8])
    sumdists = []
    for i in range(3,5):
        for j in range(5,9):
            sumdists.append((points[i][0] - points[j][0])**2 + (points[i][1] -
                                                         points[j][1])**2)

    sumdists = (np.array(sumdists) / np.max(sumdists)).sum()

    # dist2d_40 = (points[4][0] - points[0][0])**2 + (points[4][1] - points[0][1])**2
    # dist2d_80 = (points[8][0] - points[0][0])**2 + (points[8][1] - points[0][1])**2
    # dist2d_50 = (points[4][0] - points[5][0])**2 + (points[4][1] - points[5][1])**2
    #
    # angle_2d = angle_between_points_2d(points[4], points[8], points[17])
    # angle_2d2 = angle_between_points_2d(points[3], points[7], points[17])
    # angle_2d3 = angle_between_points_2d(points[5], points[6], points[8])
    angle_3d = angle_between_points(points[5], points[6], points[8])
    # print(angle408, sumdists, angle_2d, angle_2d2, angle_2d3, angle_3d)
    return angle_3d

t1 = 0
t2 = 1

touch_buffer = deque([], maxlen = 10)
arm_pos_buf = deque([], maxlen = 10)
pinch_pos_buf = deque([], maxlen = 10)
pinch_buffer = deque([], maxlen = 2)
arm_buffer = deque([], maxlen = 2)

next_pinch_time = time.time()
pinch_count = 0
while True:
    succs = 0
    while succs < 10:
        success, img = videoCap.read()
         # showing image on separate window (only if read was successfull)
        if success:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            recHands = hands.process(img)
            if recHands.multi_hand_landmarks:
                for hand in recHands.multi_hand_landmarks:
                    coords = []
                    h, w, c = img.shape

                    for datapoint_id, point in enumerate(hand.landmark):
                        coords.append([point.x, point.y, point.z])
                        x, y = int(point.x * w), int(point.y * h)
                        cv2.circle(img, (x, y), 2, (255, 0, 255), cv2.FILLED)



                    arm_pos_buf.append(coords[0])
                    pinch_pos_buf.append(coords[8])


                    touch_buffer.append(
                        angle_between_points(coords[8], coords[5], coords[0]))
                    succs += 1


                    def calculate_derivative(points):
                        if len(points) != 2:
                            return 0

                        # Convert points to numpy arrays
                        p1 = np.array(points[0])
                        p2 = np.array(points[1])

                        # Compute the derivative (difference vector)
                        derivative = p2 - p1
                        return np.log10(np.linalg.norm(derivative))

                    r_arm1 = np.sum(np.array(list(arm_pos_buf)[:5]))/5
                    r_arm2 = np.sum(np.array(list(arm_pos_buf)[5:]))/5

                    r_pinch1 = np.sum(np.array(list(pinch_pos_buf)[:5]))/5
                    r_pinch2 = np.sum(np.array(list(pinch_pos_buf)[5:]))/5

                    pinch_speed = calculate_derivative([r_pinch1,r_pinch2])
                    arm_speed = calculate_derivative([r_arm1,r_arm2])
                    if pinch_speed > -2 and arm_speed < -2.5:
                        pinch_count += 1

                    if pinch_count > 2:
                        next_pinch_time = time.time() + 0.45
                        pinch_count = 0
                        execute_click(coords,w,h,True)
                    execute_click(coords,w,h,False)


            cv2.imshow("CamOutput", img)
            cv2.waitKey(1)



    #
    # touch_val = sum(touch_buffer) / len(touch_buffer)
    # pinch_val = sum([np.sign((pinch_buffer[i+1] - pinch_buffer[i]) )
    #                  for i in range(len(pinch_buffer)-1)])
    # print(pinch_val)
    # # print(pinch_val)
    # # print(fist_val, pinch_val, sep=' ')
    # # if -3.5 < pinch_val < -2.3:
    # #     print("pinch")
    # # else:
    # #     if fist_val > 4.65:
    # #         print("fist")
    # # print(touch_val, pinch_val)
    #
    # pinch_buffer.clear()
    # touch_buffer.clear()