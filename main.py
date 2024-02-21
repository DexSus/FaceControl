import os
import pickle

import cvzone
import numpy as np

import cv2
import face_recognition

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

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    small_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    face_cur_frame = face_recognition.face_locations(small_img)
    encode_cur_frame = face_recognition.face_encodings(small_img, face_cur_frame)

    img_background[162:162 + 480, 55:55 + 640] = img
    img_background[44:44 + 633, 808:808 + 414] = image_mode_list[0]

    for encode_face, face_location in zip(encode_cur_frame, face_cur_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known, encode_face)

        match_index = np.argmin(face_distance)

        if matches[match_index]:
            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            cvzone.cornerRect(img_background, bbox, rt=0)

    cv2.imshow("Face Attendance", img_background)
    cv2.waitKey(1)
