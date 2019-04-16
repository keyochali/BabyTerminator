import cv2
import dlib
import face_recognition
import numpy as np
import serial

#ser=serial.Serial('COM4',9600)

def quit():
    exit(0)

pcCam=cv2.VideoCapture(0)
carCam= cv2.VideoCapture(1)


cv2.namedWindow("Home")
cv2.namedWindow("carCam")

colorFrame=np.zeros((100,100,3),np.uint8)
cv2.namedWindow("ColorFrame")


detector =dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# default colors

kernel = np.ones((5,5),np.uint16)
cnMIN = [0, 173, 154]
cnMAX = [70, 255, 255]







#mouse events and functions
"""
0 for laser selecting the point
1 for selecting face area
2 for slecting the first color
3 for selectin the second color
"""
md=False
fax1 = int(pcCam.get(3) / 4)
fax2 = int(pcCam.get(3) - pcCam.get(3) / 4)
fay1 = int(pcCam.get(4) / 4)
fay2 = int(pcCam.get(4) - pcCam.get(4) / 4)
ffax1,ffax2,ffay1,ffay2=0,5,0,5

def CallBackFuncCar(event,x,y,flags,param):
    global lx,ly,carFrame,carCam
    if event==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(carFrame,(x,y),9,(255,0,0),6)
        lx=int((x/carCam.get(3))*180)
        ly = int((y / carCam.get(4)) * 180)


def CallBackFuncHome(event,x,y,flags,param):
    global cond,cnMIN,cnMAX,cmMIN,cmMAX,md,pcFrame,theArr,fax1,fax2,fay1,fay2,ffax1,ffax2,ffay1,ffay2

    if cond == 1:
        if event == cv2.EVENT_MOUSEMOVE:
            if md:
                ffax2=x
                ffay2=y
                cv2.rectangle(pcFrame,(ffax1,ffay1),(ffax2,ffay2),(255,100,100),5,-1)

        if event == cv2.EVENT_LBUTTONDOWN:
            md=True
            ffax1=x
            ffay1=y
        if event == cv2.EVENT_LBUTTONUP:

            fax1=min(ffax1,ffax2)
            fax2 = max(ffax1, ffax2)
            fay1=min(ffay1,ffay2)
            fay2 = max(ffay1, ffay2)
            md=False


#default for the car
hD=2
lx=90
ly=90
ch=5
cv=3
ltx=120
lty=120

pcnx=pcny=cnx=cny=90

cond=0
while True:
    ret, pcFrame = pcCam.read()
    ret, carFrame = carCam.read()



    pcFrame = cv2.flip(pcFrame, 1)
    #carFrame = cv2.flip(carFrame,1)


    key=cv2.waitKey(5)
    if key==ord('e'):
        cond=0
    if key==ord('f'):
        if cond ==1:
            cond=0
        else:
            cond=1
    if key==ord('p'):
        fra=not fra
    if key==ord('a'):
        if ch==1:
            ch=5
        else:
            ch=1
    if key==ord('d'):
        if ch == 2:
            ch = 5
        else:
            ch = 2
    if key==ord('w'):
        if ch == 3:
            ch = 5
        else:
            ch = 3
    if key==ord('s'):
        if ch == 4:
            ch = 5
        else:
            ch = 4

    if key==32:
        lx,ly=ltx,lty
    if key==27:
        break
        quit()

    #default face area


    faceArea=pcFrame[fay1:fay2,fax1:fax2]
    cv2.rectangle(pcFrame, (fax1, fay1), (fax2, fay2), (40, 120, 160), 2, -1)
    gray=cv2.cvtColor(faceArea,cv2.COLOR_BGR2GRAY)
    faces=detector(gray)

    #for face recognition in action



    HSVFrame=cv2.cvtColor(pcFrame,cv2.COLOR_BGR2HSV)
    cnf=cv2.inRange(HSVFrame,np.array(cnMIN),np.array(cnMAX))
    cnMorph = cv2.morphologyEx(cnf, cv2.MORPH_OPEN, kernel)
    cnx, cny, cnw, cnh = cv2.boundingRect(cnMorph)

    """
    if pcnx<cnx:
        ltx+=10
    if pcnx>cnx:
        ltx-=10
    if pcny<cny:
        lty+=10
    if pcny>cny:
        lty-=10

    cv2.circle(carFrame, (cnx, cny), 5, (255, 0, 0), 1, -1)
    cv2.circle(carFrame,(ltx,lty),5,(0,0,255),1,-1)
    """
    pcnx=cnx
    pcny=cny
    for face in faces:
        fl=face.left()
        ft=face.top()
        fr=face.right()
        fb=face.bottom()
        landmarks = predictor(gray, face)
        for i in range(68):
            cv2.circle(faceArea,(landmarks.part(i).x,landmarks.part(i).y),1,(0,0,255),1,-1)

        nx = landmarks.part(30).x
        c0 = landmarks.part(1).x
        c3 = landmarks.part(15).x
        c1 = c0 + (c3 - c0) * 0.4
        c2 = c1 + (c3 - c0) * 0.2

        if nx > c0 and nx < c1:
            cv2.putText(pcFrame, "left", (fax1,fay1), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 255, 255), 2, cv2.LINE_AA)
            hD = 180
        elif nx > c1 and nx < c2:
            cv2.putText(pcFrame, "center", (fax1, fay1), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 255, 255), 2, cv2.LINE_AA)
            hD = 90
        elif nx > c2 and nx < c3:
            cv2.putText(pcFrame, "right", (fax1, fay1), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 255, 255), 2, cv2.LINE_AA)
            hD = 1

    theStr="C"+str(hD)+"X"+str(lx)+"Y"+str(ly)+"D"+str(ch)+",/."
    cv2.putText(pcFrame,theStr,(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,1)

    cv2.setMouseCallback("Home",CallBackFuncHome)
    cv2.setMouseCallback("Car", CallBackFuncCar)
    #ser.write(bytes(theStr, 'UTF-8'))
    cv2.imshow("Home",pcFrame)
    cv2.imshow("face area", faceArea) #for face area
    cv2.imshow("Car",carFrame)



pcCam.release()
carCam.release()
cv2.destroyAllWindows()
