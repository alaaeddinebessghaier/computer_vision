import cv2
import time
import handTrackingModule as htm
import mediapipe as mp



cap = cv2.VideoCapture(0)
detector = htm.handDetector()
Ptime = 0
Ctime = 0
while True:
    succes, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findHands(img)
    if len(lmlist) !=0:
        print(lmlist[4])
    Ctime = time.time()
    fps = 1 / (Ctime - Ptime)
    Ptime = Ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow('image', img)
    cv2.waitKey(1)