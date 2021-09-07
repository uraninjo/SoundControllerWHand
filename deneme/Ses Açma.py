import cv2
import numpy as np
import time
import mediapipe as mp
import ElTakibiModülü as etm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=640,480
cap=cv2.VideoCapture(0)#Video'da yüklenebilir
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=etm.El_Takibi(detconf=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
while True:
    ret,frame=cap.read()
    frame=detector.Takip(frame)
    lmList=detector.Pozisyon(frame,çiz=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(frame, (x1,y1), 8, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
        cv2.line(frame, (x1,y1), (x2, y2), (0, 0, 0), 4)
        cv2.circle(frame, (cx,cy), 8, (255, 0, 0), cv2.FILLED)
        uzunluk=math.hypot(x2-x1,y2-y1)
        if uzunluk<50:
            cv2.circle(frame, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
        vol=np.interp(uzunluk,[50,230],[minVol,maxVol])
        volBar = np.interp(uzunluk, [50, 230], [400,150])
        volPerc=np.interp(uzunluk, [50, 230], [0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(frame, (50, 150), (85, 400), (0,255,0), 3)
        cv2.rectangle(frame, (50,int(volBar)), (85,400), (0,255,0), cv2.FILLED)
        cv2.putText(frame, str(int(volPerc)), (50,130), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (18, 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()