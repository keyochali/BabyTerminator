import cv2
import dlib
import face_recognition
import numpy as np
import serial

#ser=serial.Serial('COM5',9600)

def quit():
    exit(0)

pcCam=cv2.VideoCapture(0)
carCam= cv2.VideoCapture(2)


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





#for face recognition
def addFaces(thePicture,theName,info):
    global faceList, nameList, infoList
    aPic = face_recognition.load_image_file(thePicture)
    encodedPic =face_recognition.face_encodings(aPic)[0]
    faceList.append(encodedPic)
    nameList.append(theName)
    infoList.append(info)

faceList=[]
nameList=[]
infoList=[]
addFaces("revan.JPEG","Revan",["student","Group B"])
addFaces("keyo.jpg","Keyo",["student","Group A","Pirmam"])
addFaces("Marwan.jpeg","Mr. Marwan",["Lecturer","SE","07518079373"])

faceLocations=[]
faceEncodings=[]
faceNames=[]
faceInfo=[]
fra = False
carProcessing = True


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
ltx=90
lty=90

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

    if fra:
        smallframe1 = cv2.resize(carFrame, (0, 0), fx=0.25, fy=0.25)

        rgbframe1 = smallframe1[:, :, ::-1]
        if carProcessing:
            faceLocations = face_recognition.face_locations(rgbframe1)
            faceEncodings = face_recognition.face_encodings(rgbframe1, faceLocations)
            faceNames = []
            faceInfo = []
            for faceEncoding in faceEncodings:
                matches = face_recognition.compare_faces(faceList, faceEncoding)
                name = "Unknown"
                fInfo = ["Nothing!!!"]
                if True in matches:
                    firstMatchIndex = matches.index(True)
                    name = nameList[firstMatchIndex]
                    fInfo = infoList[firstMatchIndex]
                faceNames.append(name)
                faceInfo.append(fInfo)
        carProcessing = not carProcessing

        for (top, right, bottom, left), name, fInfo in zip(faceLocations, faceNames, faceInfo):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(carFrame, (left, top), (right, bottom), (255, 255,0), 2)

            cv2.rectangle(carFrame, (left, top- 50), (right, top), (255, 255,0), cv2.FILLED)

            cv2.putText(carFrame, name, (left + 6, top - 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 1)

            for infi in range(len(fInfo)):
                cv2.putText(carFrame, fInfo[infi], (right, top + 50 * infi + 20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0),
                            1)
        # _____________________end of face recognition_______________



    HSVFrame=cv2.cvtColor(pcFrame,cv2.COLOR_BGR2HSV)
    cnf=cv2.inRange(HSVFrame,np.array(cnMIN),np.array(cnMAX))
    cnMorph = cv2.morphologyEx(cnf, cv2.MORPH_OPEN, kernel)
    cnx, cny, cnw, cnh = cv2.boundingRect(cnMorph)


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
