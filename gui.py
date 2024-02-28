#the gui
import backend
import sys
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QGridLayout, QComboBox, QMainWindow, QWidget, QLabel, QFileDialog, QStyle

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.trim_video_button = QPushButton("Trim the Video")
        self.trim_video_button.clicked.connect(self.trim_video)
        # self.box = QComboBox()
        # self.box.insertItem(0, "a")
        # self.box.insertItem(1, "b")
        # self.box.insertItem(2, "c")
        #self.button.clicked.connect(self.greetings)

        self.setWindowTitle("thing")
        layout = QGridLayout(self)
        layout.addWidget(self.file_path_label, 0, 0)
        layout.addWidget(self.file_search_button, 1, 1)
        layout.addWidget(self.file_path_edit, 1, 0)
        layout.addWidget(self.start_time_label, 2, 0)
        layout.addWidget(self.start_time_edit, 3, 0)
        layout.addWidget(self.end_time_label, 4, 0)
        layout.addWidget(self.end_time_edit, 5, 0)
        layout.addWidget(self.audio_track_label, 6, 0)
        layout.addWidget(self.audio_track_edit, 7, 0)
        layout.addWidget(self.subtitle_track_label, 8, 0)
        layout.addWidget(self.subtitle_track_edit, 9, 0)
        layout.addWidget(self.trim_video_button, 10, 0)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_files(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            fileName = dialog.selectedFiles()
        self.file_path_edit.setText(fileName[0])

    def trim_video(self):
        backend.trim_and_encode(self.file_path_edit.text().encode('unicode-escape').decode(), self.start_time_edit.text(), self.end_time_edit.text(), self.audio_track_edit.text(), self.subtitle_track_edit.text())
        

if __name__ == '__main__':
    #create qt app
    app = QApplication(sys.argv)
    #create and show form
    form = Form()
    form.show()
    #run the qt app
    sys.exit(app.exec())