import os

import cv2
import face_recognition
import pickle

from DataBase import save_img_to_storage

folder_path = 'Images'
path_list = os.listdir(folder_path)
image_list = []
people_ids = []
for path in path_list:
    image_list.append(cv2.imread(os.path.join(folder_path, path)))
    people_ids.append(os.path.splitext(path)[0])

    save_img_to_storage(f"{folder_path}/{path}")


def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)

    return encode_list


print("Starting encode...")
encode_list_known = find_encodings(image_list)
encode_list_known_with_ids = [encode_list_known, people_ids]
print("Encoding complete!")

file = open("EncodeFile.p", 'wb')
pickle.dump(encode_list_known_with_ids, file)
file.close()
