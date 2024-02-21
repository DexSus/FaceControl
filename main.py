import os
import pickle
from datetime import datetime

import cvzone
import numpy as np

import cv2
import face_recognition

from DataBase import get_people, get_img, update_data

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

img_background = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folder_mode_path = 'Resources/Modes'
mode_path_list = os.listdir(folder_mode_path)
image_mode_list = []
for path in mode_path_list:
    image_mode_list.append(cv2.imread(os.path.join(folder_mode_path, path)))

# Load encoding file
print("Load encode file...")
file = open('EncodeFile.p', 'rb')
encode_list_known_with_ids = pickle.load(file)
file.close()
encode_list_known, people_ids = encode_list_known_with_ids
print("Encode file loaded!")

mode_type = 0
counter = 0
id = -1
image_of_people = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    small_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    face_cur_frame = face_recognition.face_locations(small_img)
    encode_cur_frame = face_recognition.face_encodings(small_img, face_cur_frame)

    img_background[162:162 + 480, 55:55 + 640] = img
    img_background[44:44 + 633, 808:808 + 414] = image_mode_list[mode_type]

    if face_cur_frame:
        for encode_face, face_location in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_distance = face_recognition.face_distance(encode_list_known, encode_face)

            match_index = np.argmin(face_distance)

            if matches[match_index]:
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                img_background = cvzone.cornerRect(img_background, bbox, rt=0)

                id = people_ids[match_index]

                if counter == 0:
                    cvzone.putTextRect(img_background, "Loading...", (275, 400))
                    cv2.imshow("Face Attendance", img_background)
                    cv2.waitKey(1)
                    counter = 1
                    mode_type = 1

        if counter != 0:
            if counter == 1:
                people_info = get_people(f'People/{id}')
                print(people_info)
                blob = get_img(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                image_of_people = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                datetime_object = datetime.strptime(people_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                seconds_elapsed = (datetime.now() - datetime_object).total_seconds()
                if seconds_elapsed > 30:
                    update_data(id, 'last_attendance_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    mode_type = 3
                    counter = 0
                    img_background[44:44 + 633, 808:808 + 414] = image_mode_list[mode_type]

            if mode_type != 3:
                if 10 < counter < 20:
                    mode_type = 2

                img_background[44:44 + 633, 808:808 + 414] = image_mode_list[mode_type]

                if counter <= 10:
                    cv2.putText(img_background, str(people_info['total_attendance']), (850, 125), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(img_background, str(people_info['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(img_background, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(img_background, str(people_info['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(img_background, str(people_info['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(img_background, str(people_info['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(people_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(img_background, str(people_info['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (50, 50, 50), 1)

                    img_background[175:175 + 216, 909:909 + 216] = image_of_people

                counter += 1

                if counter >= 20:
                    counter = 0
                    mode_type = 0
                    people_info = []
                    image_of_people = []
                    img_background[44:44 + 633, 808:808 + 414] = image_mode_list[mode_type]
    else:
        mode_type = 0
        counter = 0

    cv2.imshow("Face Attendance", img_background)
    cv2.waitKey(1)
