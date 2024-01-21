import numpy
import cv2
import numpy as np
import time
import handTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#################################################################
Wcam,Hcam = 640,480
#################################################################

Ptime = 0
cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)
detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]











volBAR = 400
vol = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),7,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1,y2,y1)
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volBAR = np.interp(length,[50,int(volBAR)],[400,150])

        volume.SetMasterVolumeLevel(vol, None)

        print(int(length),vol)
        if length <300:
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img,(50,50),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBAR)),(85,400),(0,255,0),cv2.FILLED)

    Ctime = time.time()
    fps = 1 / (Ctime - Ptime)
    Ptime = Ctime
    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break
        cap.release()
        cv2.destroyWindow('img')