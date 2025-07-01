import cv2
import mediapipe as mp

class handDetector:
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds =[4,8,12,16,20]

    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw = True):
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id ,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h, w,c = img.shape
                cx, cy = int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])        
                cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        return self.lmlist            
    def fingersUp(self):
        fingers = []
        if len(self.lmlist) != 21:
            return [0,0,0,0,0]
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers                                        
def main():  
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList:
            fingers = detector.fingersUp()
            print(fingers)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


