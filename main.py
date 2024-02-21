import os

import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

img_background = cv2.imread('Resources/background.png')

folder_mode_path = 'Resources/Modes'
mode_path_list = os.listdir(folder_mode_path)
image_mode_list = []
for path in mode_path_list:
    image_mode_list.append(cv2.imread(os.path.join(folder_mode_path, path)))

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    img_background[162:162+480, 55:55+640] = img
    img_background[44:44 + 633, 808:808 + 414] = image_mode_list[0]

    cv2.imshow("Face Attendance", img_background)
    cv2.waitKey(1)