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
bucket = storage.bucket()

data = {
    "159753":
        {
            "name": "Iskenderov Arthur",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 212,
            "last_attendance_time": "2024-02-21 11:35:20",
            "standing": "A",
            "year": 3
        },
    "852741":
        {
            "name": "Kim Cherniy David",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 212,
            "last_attendance_time": "2024-02-21 11:35:20",
            "standing": "C",
            "year": 3
        },
    "963852":
        {
            "name": "Kim Valeria",
            "major": "Cadet",
            "starting_year": 2021,
            "total_attendance": 212,
            "last_attendance_time": "2024-02-21 11:35:20",
            "standing": "B",
            "year": 3
        }
}

for key, value in data.items():
    ref.child(key).set(value)


def save_img_to_storage(file_name):
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)


def get_people(reference):
    return db.reference(reference).get()


def get_img(reference):
    return bucket.get_blob(reference)


def update_data(id, key, value):
    reference = db.reference(f'People/{id}')
    reference.child(key).set(value)
