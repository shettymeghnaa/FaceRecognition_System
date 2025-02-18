import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendacerealtime-92c0b-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-92c0b.appspot.com"
})


#Importing student images
folderPath='Images'
PathList=os.listdir(folderPath)
print(PathList)
imgList=[]
studentIds=[]
for path in PathList:
    if not path.startswith('.') and path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        # Load the image
        img = cv2.imread(os.path.join(folderPath, path))
        # Append the loaded image to imgList
        imgList.append(img)
        # Extract student ID from the filename and append to studentIds
        student_id = os.path.splitext(path)[0]
        studentIds.append(student_id)

        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)


print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding started......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
