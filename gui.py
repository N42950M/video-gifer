#the gui
import backend
import sys
import shutil
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QGridLayout, QComboBox, QMainWindow, QWidget, QLabel, QFileDialog, QStyle, QCheckBox

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_label = QLabel("VIDEO OPTIONS:")
        self.video_label.setFont(QFont("", 15))

        self.file_path_label = QLabel("Enter the path to the file:")
        self.file_path_edit = QLineEdit("")
        self.file_search_button = QPushButton()
        pixmap = QStyle.SP_DirIcon
        icon = self.style().standardIcon(pixmap)
        self.file_search_button.setIcon(icon)
        self.file_search_button.clicked.connect(self.browse_files)

        self.start_time_label = QLabel("Enter the starting time:")
        self.start_time_edit = QLineEdit("")
        self.start_time_edit.setPlaceholderText("HH:MM:SS.MS")

        self.end_time_label = QLabel("Enter the ending time:")
        self.end_time_edit = QLineEdit("")
        self.end_time_edit.setPlaceholderText("HH:MM:SS.MS")

        self.audio_track_label = QLabel("Enter the audio track to use:")
        self.audio_track_label.setToolTip("Takes Integer Values starting from 0")
        self.audio_track_edit = QLineEdit("")
        self.audio_track_edit.setPlaceholderText("leave blank for default")

        self.subtitle_track_label = QLabel("Enter the subtitle track to use:")
        self.subtitle_track_label.setToolTip("Takes Integer Values starting from 0")
        self.subtitle_track_edit = QLineEdit("")
        self.subtitle_track_edit.setPlaceholderText("leave blank for none")

        self.trim_video_button = QPushButton("Cut Video")
        self.trim_video_button.clicked.connect(self.trim_video)

        self.keep_video = QCheckBox("Keep cut video?")
        self.keep_video.setToolTip("copies and moves video file out of the temporary directory")

        self.gif_label = QLabel("GIF OPTIONS:")
        self.gif_label.setFont(QFont("", 15))

        self.keep_original_res_check = QCheckBox("Keep original resolution?")
        self.keep_original_res_check.setToolTip("worse quality and manually needs font size editing")

        self.speed_label = QLabel("Speed Multiplier:")
        self.speed_label.setToolTip("Takes an integer value")
        self.speed_edit = QLineEdit()
        self.speed_edit.setPlaceholderText("Leave blank for 1")

        self.text_label = QLabel("Text to go on the GIF:")
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Leave blank for no text")

        self.font_label = QLabel("Font for the text:")
        self.font_label.setToolTip("Font must be installed on the system, spaces turn into -")
        self.font_edit = QLineEdit()
        self.font_edit.setPlaceholderText("Leave blank for defaults")

        self.font_size_label = QLabel("Font Size for the text:")
        self.font_size_label.setToolTip("integer values only")
        self.font_size_edit = QLineEdit()
        self.font_size_edit.setPlaceholderText("Leave blank for defaults")

        self.text_location_label = QLabel("Where should the text be placed?")
        self.text_location_box = QComboBox()
        self.text_location_box.insertItem(0, "above_image")
        self.text_location_box.insertItem(1, "on_image")

        self.setWindowTitle("thing")
        layout = QGridLayout(self)
        layout.addWidget(self.video_label, 0, 0)
        layout.addWidget(self.file_path_label, 1, 0)
        layout.addWidget(self.file_search_button, 2, 1)
        layout.addWidget(self.file_path_edit, 2, 0)
        layout.addWidget(self.start_time_label, 3, 0)
        layout.addWidget(self.start_time_edit, 4, 0)
        layout.addWidget(self.end_time_label, 5, 0)
        layout.addWidget(self.end_time_edit, 6, 0)
        layout.addWidget(self.audio_track_label, 7, 0)
        layout.addWidget(self.audio_track_edit, 8, 0)
        layout.addWidget(self.subtitle_track_label, 9, 0)
        layout.addWidget(self.subtitle_track_edit, 10, 0)
        layout.addWidget(self.keep_video, 11, 0)
        layout.addWidget(self.trim_video_button, 12, 0)

        layout.addWidget(self.gif_label, 13, 0)
        layout.addWidget(self.keep_original_res_check, 14, 0)
        layout.addWidget(self.speed_label, 15, 0)
        layout.addWidget(self.speed_edit, 16, 0)
        layout.addWidget(self.text_label, 17, 0)
        layout.addWidget(self.text_edit, 18, 0)
        layout.addWidget(self.font_label, 19, 0)
        layout.addWidget(self.font_edit, 20, 0)
        layout.addWidget(self.font_size_label, 21, 0)
        layout.addWidget(self.font_size_edit, 22, 0)
        layout.addWidget(self.text_location_label, 23, 0)
        layout.addWidget(self.text_location_box, 24, 0)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_files(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            fileName = dialog.selectedFiles()
        self.file_path_edit.setText(fileName[0])

    def trim_video(self):
        filepath = self.file_path_edit.text().encode('unicode-escape').decode()
        backend.trim_and_encode(filepath, self.start_time_edit.text(), self.end_time_edit.text(), self.audio_track_edit.text(), self.subtitle_track_edit.text())
        if self.keep_video.isChecked():
            shutil.copyfile("output.mp4", f"../output_[{self.start_time_edit.text()}-{self.end_time_edit.text()}].mp4")

if __name__ == '__main__':
    #create qt app
    app = QApplication(sys.argv)
    #create and show form
    form = Form()
    form.show()
    #run the qt app
    sys.exit(app.exec())