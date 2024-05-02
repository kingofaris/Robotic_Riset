import cv2
import os
import shutil

# Global counter
counter = 0

# Crate Directory
dr_path = "dataset"
if os.path.exists(dr_path):
    shutil.rmtree(dr_path)
os.mkdir(dr_path)

# File .txt
file_txt = open("dataset/orb_dataser.txt", "w")

# Open webcam using Opencv
cam_video = cv2.VideoCapture(0)


if not cam_video.isOpened():
    print("Device can't open")
    exit()

while(True):
    # Perulangan mengambil file gambar
    ret, frame = cam_video.read()
    cv2.imshow("Kamera saya",frame)
    cv2.imwrite("dataset/Gambar"+ str(counter) + ".png", frame)

    # Perulagan mencatat data pada file
    file_txt.write("Gambar"+ str(counter) + ".png" + "\n")
    counter += 1

    # Penutup looping
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

file_txt.close()
