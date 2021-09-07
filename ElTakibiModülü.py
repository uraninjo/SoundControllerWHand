import cv2
import numpy as np
import time
import mediapipe as mp
import math



class El_Takibi():
    def __init__(self,mode=False,max_hands=2,detconf=0.5,trackconf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detconf = detconf
        self.trackconf = trackconf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,self.detconf,self.trackconf)  # Kaç el kullanılacağı ve optimizasyon ayarları yapılabilir
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def Takip(self,frame,çiz=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if çiz:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
        return frame
    def Pozisyon(self,frame,elNo=0,çiz=True):
        xList=[]
        yList=[]
        bbox=[]
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            el_lm=self.results.multi_hand_landmarks[elNo]
            for id, lm in enumerate(el_lm.landmark):
                # print(id,lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx,cy])
                    #if id == 4:
                if çiz:
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            xmin,xmax=min(xList),max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox=xmin,ymin,xmax,ymax
            if çiz:
                cv2.rectangle(frame,(bbox[0]-20,bbox[1]-20),(bbox[2]+30,bbox[3]+30),(0,255,0),2)
        return self.lmList,bbox

    def parmaklarYukarda(self):
        parmaklar=[]
        if self.lmList[self.tipIds[0]][1]>self.lmList[self.tipIds[0]-1][1]:
            parmaklar.append(1)
        else:
            parmaklar.append(0)
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                parmaklar.append(1)
            else:
                parmaklar.append(0)
        return parmaklar
    def uzaklıkBulma(self,p1,p2,frame,çiz=True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if çiz:
            cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.circle(frame, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
        uzunluk = math.hypot(x2 - x1, y2 - y1)
        return uzunluk,frame,[x1,y1,x2,y2,cx,cy]
def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)  # Video'da yüklenebilir
    detector=El_Takibi()
    while True:
        ret, frame = cap.read()
        frame=detector.Takip(frame)
        lmList=detector.Pozisyon(frame)
        if len(lmList)!=0:
            print(lmList)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (18, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()


