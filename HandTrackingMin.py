import cv2

import mediapipe as mp
import time


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

Ptime = 0
Ctime = 0
while True:
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            for id, lm in enumerate(handLMS.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w) , int(lm.y*h)
                print(id,cx,cy)
                # if id == 8:
                cv2.circle(img,(cx,cy), 25 ,(255,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handLMS,mpHands.HAND_CONNECTIONS)









    Ctime = time.time()
    fps= 1 / (Ctime - Ptime)
    Ptime = Ctime
    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break
cap.release()
cv2.destroyWindow('image')