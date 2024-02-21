import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-control-c58f3-default-rtdb.firebaseio.com/",
    'storageBucket': "face-control-c58f3.appspot.com"
})

ref = db.reference('People')

data = {
    "159753":
        {
            "name": "Iskenderov Arthur",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 6,
            "last_attendance_time": "2024-02-21 11:35:20"
        },
    "852741":
        {
            "name": "Kim Cherniy David",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 6,
            "last_attendance_time": "2024-02-21 11:35:20"
        },
    "963852":
        {
            "name": "in future Kim, little bit niger Valeria",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 6,
            "last_attendance_time": "2024-02-21 11:35:20"
        }
}

for key, value in data.items():
    ref.child(key).set(value)


def save_img_to_storage(file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
