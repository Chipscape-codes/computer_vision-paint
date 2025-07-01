import Handtrackingmodule as htm
import cv2
import time
import numpy as np 
import pyautogui as pa
from math import hypot

cap = cv2.VideoCapture(0)
screen_width, screen_height = pa.size()
detector = htm.handDetector(detectionCon=0.85)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) > 8:
        x1, y1 = lmList[8][1:] 
        x2, y2 = lmList[12][1:]  
        fingers = detector.fingersUp()

        h, w, _ = img.shape
        if fingers[1] and not fingers[2]:

            cv2.putText(img, "MADHU", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            screen_x = np.interp(x1, (0, w), (0, screen_width))
            screen_y = np.interp(y1, (0, h), (0, screen_height))
            pa.moveTo(screen_x, screen_y)
            pa.mouseUp()

        if fingers[1] and fingers[0]:
            pa.mouseDown()
            screen_x = np.interp(x1, (0, w), (0, screen_width))
            screen_y = np.interp(y1, (0, h), (0, screen_height))
            pa.moveTo(screen_x, screen_y)
                

    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)