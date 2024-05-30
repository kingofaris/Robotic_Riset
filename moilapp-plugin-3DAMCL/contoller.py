from src.plugin_interface import PluginInterface
from PyQt6.QtWidgets import QWidget
from .ui_main import Ui_Form
import cv2
import shutil
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

import os

class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.set_stylesheet()

        self.image_counter = 0
        self.cap = None
        self.cap2 = None
        self.camera_started = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.ui.pushButton_dataset.clicked.connect(self.streaminVideo) # Menghubungkan tombol dengan fungsi streaminVideo
        self.ui.pushButton_4.clicked.connect(self.stop_camera)

        # Membuat direktori dataset
        self.create_dataset_directory1()
        self.create_dataset_directory2()

    def streaminVideo(self):
        self.cap = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(2)
        if not self.cap.isOpened() and self.cap2.isOpened():
            print("Error: Failed to open camera.")
            return
        else:
            print("Cameras opened successfully")

        # Start timer to update frame
        self.timer.start(10)  # Mengatur waktu refresh frame
        self.camera_started = True

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened() and self.cap2 is not None and self.cap2.isOpened():
            ret, frame = self.cap.read()
            ret2, frame2 = self.cap2.read()
            if ret and ret2:
                # Convert frame 1 to QImage
                h1, w1, ch1 = frame.shape
                bytes_per_line1 = ch1 * w1
                q_img1 = QImage(frame.data, w1, h1, bytes_per_line1, QImage.Format.Format_BGR888)

                # Convert QImage to QPixmap
                pixmap1 = QPixmap.fromImage(q_img1)

                # Display frame 1 on label_cam_1
                self.ui.label_5.setPixmap(pixmap1)
                self.ui.label_5.setScaledContents(True)

                # Convert frame 2 to QImage
                h2, w2, ch2 = frame2.shape
                bytes_per_line2 = ch2 * w2
                q_img2 = QImage(frame2.data, w2, h2, bytes_per_line2, QImage.Format.Format_BGR888)

                # Convert QImage to QPixmap
                pixmap2 = QPixmap.fromImage(q_img2)

                # Display frame 2 on label_cam_2
                self.ui.label_7.setPixmap(pixmap2)
                self.ui.label_7.setScaledContents(True)

                print(h1,w1,ch1)

                # Simpan gambar ke dataset
                self.save_image_to_dataset1(frame)
                self.save_image_to_dataset2(frame2)
                self.saveText()
                self.showTerminal()


    def create_dataset_directory1(self):
        dr_path = "./plugins/moilapp-plugin-takeDataset/dataset1"
        if os.path.exists(dr_path):
            shutil.rmtree(dr_path)
        os.makedirs(dr_path)  # Menggunakan os.makedirs() agar dapat membuat direktori dan subdirektori jika belum ada

    def create_dataset_directory2(self):
        dr_path = "./plugins/moilapp-plugin-takeDataset/dataset2"
        if os.path.exists(dr_path):
            shutil.rmtree(dr_path)
        os.makedirs(dr_path)  # Menggunakan os.makedirs() agar dapat membuat direktori dan subdirektori jika belum ada



    def save_image_to_dataset1(self, frame):
        file_path = os.path.join("./plugins/moilapp-plugin-takeDataset/dataset1", f"Gambar{self.image_counter}.png")
        cv2.imwrite(file_path, frame)
        # Meningkatkan nilai counter untuk nama file selanjutnya




    def save_image_to_dataset2(self, frame):
        file_path = os.path.join("./plugins/moilapp-plugin-takeDataset/dataset2", f"Gambar{self.image_counter}.png")

        # Menyimpan frame sebagai gambar PNG
        cv2.imwrite(file_path, frame)


    def saveText(self):
        self.file_baru = f"Gambar{self.image_counter}.png \n"
        with open("./plugins/moilapp-plugin-takeDataset/dataset1/dataset.txt","a") as f:  # Menggunakan mode "a" untuk menambahkan ke file
            f.write(self.file_baru)

    def showTerminal(self):
        self.file_baru = f"Gambar{self.image_counter}.png \n"
        self.ui.label_terminal.setText("Image Saved " + self.file_baru)
        self.ui.label_terminal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_counter += 1

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
        if self.cap2 is not None:
            self.cap2.release()
        self.timer.stop()
        self.camera_started = False

    def set_stylesheet(self):
        self.ui.label.setStyleSheet("font-size:64px;")

        # push button
        self.ui.pushButton.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_2.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_3.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_4.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_5.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_dataset.setStyleSheet(self.model.style_pushbutton())
        self.ui.pushButton_7.setStyleSheet(self.model.style_pushbutton())

        # label
        self.ui.label.setStyleSheet(self.model.style_label())
        self.ui.label_2.setStyleSheet(self.model.style_label())
        self.ui.label_terminal.setStyleSheet(self.model.style_label())
        self.ui.label_4.setStyleSheet(self.model.style_label())
        self.ui.label_5.setStyleSheet(self.model.style_label())
        self.ui.label_6.setStyleSheet(self.model.style_label())
        self.ui.label_7.setStyleSheet(self.model.style_label())
        self.ui.label_8.setStyleSheet(self.model.style_label())
        self.ui.label_9.setStyleSheet(self.model.style_label())
        self.ui.label_10.setStyleSheet(self.model.style_label())

        # checkbox
        self.ui.checkBox.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_2.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_3.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_4.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_5.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_6.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_7.setStyleSheet(self.model.style_checkbox())
        self.ui.checkBox_8.setStyleSheet(self.model.style_checkbox())

        #Frame
        self.ui.frame_2.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_3.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_4.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_5.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_6.setStyleSheet(self.model.style_frame_main())
        self.ui.frame_7.setStyleSheet(self.model.style_frame_main())
        self.ui.frame_8.setStyleSheet(self.model.style_frame_object())







class Orb_Slam_Algorithm(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()
