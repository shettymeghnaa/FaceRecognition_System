import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendacerealtime-92c0b-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-92c0b.appspot.com"
})

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread('Resources/background.png')
#Importing the mode images into a list
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

#Load the encoding file
print("Loading Encode File.....")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load( file )
file.close()
encodeListKnown , studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")
# print(modePathList)

modeType = 0
counter = 0
id = -1

while True:
    success , img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        face_distances = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("Matches: ",matches)
        # print("Distance: ",face_distances)

        matchIndex = np.argmin(face_distances)
        # print("Match Index",matchIndex)

        if matches[matchIndex]:
            # print("Known face Detected")
            # print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
            # cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 2)
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]

            if counter == 0:
                counter = 1

    if counter != 0:

        if counter == 1:
            studentInfo = db.reference(f'students/{id}').get()
            print(studentInfo)

        cv2.putText(imgBackground,str(studentInfo['total_attendance']),)

        counter +=1

    # cv2.imshow('Webcam',img)
    cv2.imshow('Face Attendance',imgBackground)
    cv2.waitKey(1)
