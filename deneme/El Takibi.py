import cv2
import numpy as np
import time
import mediapipe as mp


cap=cv2.VideoCapture(0)#Video'da yüklenebilir
mpHands=mp.solutions.hands
hands=mpHands.Hands()#Kaç el kullanılacağı ve optimizasyon ayarları yapılabilir
mpDraw=mp.solutions.drawing_utils
cTime=0
pTime=0
while True:
    ret,frame=cap.read()
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if id==4:
                    cv2.circle(frame,(cx,cy),15,(255,0,0),cv2.FILLED)
            mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(frame,str(int(fps)),(18,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    cv2.imshow("frame",frame)
    if cv2.waitKey(1)==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
