import Handtrackingmodule as htm
import cv2
import time
import numpy as np 

cap = cv2.VideoCapture(0)
cap.set(3,1288)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
xp,yp = 0,0

imgcanvas=np.zeros((720,1280,3),np.uint8)
while True:
    success ,img =cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList =detector.findPosition(img ,draw=False)

    #tip of index
    if len(lmList) > 8 :
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        #print(fingers)
        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            print("blank mode")
            drawcolor = (0,0,0)
            cv2.line(img, (xp, yp), (x1, y1), drawcolor, 15)   
        if fingers[1] and fingers[2] == False:
            print("drawing mode")
            
            if xp == 0  and yp ==0:
                xp ,yp = x1,y1
            drawcolor = (0,0,255)
            cv2.line(img, (xp, yp), (x1, y1), drawcolor, 15)
            cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, 15)
            xp,yp = x1,y1   
        if fingers[1] and fingers[2] and fingers[3]:
            print("eraser mode")
            drawcolor = (0,0,0)
            cv2.circle(img, (x1,y1), 15, drawcolor, cv2.FILLED)
            cv2.circle(imgcanvas, (x1, y1), 30, drawcolor, cv2.FILLED)
            xp,yp = x1,y1
            
    img = cv2.addWeighted(img,0.5,imgcanvas,0.5,0)        
    cv2.imshow("Image",img)
    cv2.waitKey(1)