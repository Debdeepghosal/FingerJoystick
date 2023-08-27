import cv2
import mediapipe as mp
import time
import math
from pynput.keyboard import Key,Controller #For ubuntu OS,use keyboard library in windows

keyboard = Controller()

# Set camera dimensions
wCam,hCam=640,480

# Initializing OpenCV's video capture function using the default camera
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

# Setting up mediapipe library
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

#These will be useful to calculate the frame rate
pTime=0
cTime=0


while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    cv2.rectangle(img, (480, 5), (560, 80), (255, 255, 255), 3)

    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            list=[]
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                list.append([id,cx,cy])
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            if len(list) !=0:
                # print(list[5],list[17])
                x1,y1=list[5][1],list[5][2]
                x2,y2=list[17][1],list[17][2]
                height=y2-y1
                base=x2-x1
                if height!=0 and base!=0:
                    angle_rad = math.atan(height / base)
                    angle_deg = math.degrees(angle_rad)
                    if angle_deg >0:
                        if 90-angle_deg>15:
                            print("Right")
                            cv2.arrowedLine(img, (500,40), (550,40), (0,0,255), 5)
                            keyboard.press('d')
                            time.sleep(0.05)
                            keyboard.release('d')
                    else:
                        if 90+angle_deg>15:
                            print("Left")
                            cv2.arrowedLine(img,(550,40),(500,40), (0,0,255), 5)
                            keyboard.press('a')
                            time.sleep(0.05)
                            keyboard.release('a')

                    print(angle_deg)
                    print(list[4], list[6])
                    x3, y3 = list[4][1], list[4][2]
                    x4, y4 = list[6][1], list[6][2]
                    x5, y5 = list[5][1], list[5][2]
                    x6, y6 = list[8][1], list[8][2]
                    print(y4-y3)
                    if y4-y3 > 50:
                        if abs(x6 - x5) > 50:
                            print("Shift")
                            cv2.arrowedLine(img, (525, 40), (525, 10), (0,0,255), 5)
                            cv2.arrowedLine(img, (525, 70), (525, 45), (0,0,255), 5)

                            with keyboard.pressed(Key.shift):
                                keyboard.press('w')
                                time.sleep(0.05)
                                keyboard.release('w')
                        else:
                            if height != 0 and base != 0:
                                angle_rad = math.atan(height / base)
                                angle_deg = math.degrees(angle_rad)
                                if angle_deg > 0:
                                    if 90 - angle_deg > 15:
                                        print("Right-forward")
                                        cv2.arrowedLine(img, (500, 40), (550, 40), (0,0,255), 5)

                                        with keyboard.pressed('w'):
                                            keyboard.press('d')
                                            time.sleep(0.05)
                                            keyboard.release('d')
                                    else:
                                        print("Forward")
                                        cv2.arrowedLine(img, (525, 40), (525, 10), (0,0,255), 5)
                                        keyboard.press('w')
                                        time.sleep(0.15)
                                        keyboard.release('w')

                                else:
                                    if 90 + angle_deg > 15:
                                        print("Left-forward")
                                        cv2.arrowedLine(img,(550, 40),(500, 40),  (0,0,255), 5)

                                        with keyboard.pressed('w'):
                                            keyboard.press('a')
                                            time.sleep(0.05)
                                            keyboard.release('a')
                                    else:
                                        print("Forward")
                                        cv2.arrowedLine(img, (525, 40), (525, 10), (0,0,255), 5)
                                        keyboard.press('w')
                                        time.sleep(0.15)
                                        keyboard.release('w')

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,'FPS: '+str(int(fps)),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)

