import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendacerealtime-92c0b-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "534":
        {
            "name": "Modi",
            "major": "Politics",
            "starting_year": 2020,
            "total_attendance": 8,
            "standing": "G",
            "year":4,
            "last_attendance_time": "2024-05-19 12:13:00",
        },
"777":
        {
            "name": "Dhoni",
            "major": "Cricket",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "vG",
            "year":3,
            "last_attendance_time": "2024-05-19 12:13:00",
        },
"987":
        {
            "name": "Rajnikant",
            "major": "Actor",
            "starting_year": 2022,
            "total_attendance": 9,
            "standing": "B",
            "year":2,
            "last_attendance_time": "2024-05-19 12:13:00",
        }

}

for key, value in data.items():
    ref.child(key).set(value)