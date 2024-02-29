#the gui
import backend
import sys
import os
import shutil
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QGridLayout, QComboBox, QMainWindow, QWidget, QLabel, QFileDialog, QStyle, QCheckBox, QHBoxLayout

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_label = QLabel("VIDEO OPTIONS:")
        self.video_label.setFont(QFont("", 15))
        #File path label and entry + a button that opens a file browser to populate the entry with
        self.file_path_label = QLabel("Enter the path to the file:")
        self.file_path_edit = QLineEdit("")
        self.file_search_button = QPushButton()
        pixmap = QStyle.SP_DirIcon
        icon = self.style().standardIcon(pixmap)
        self.file_search_button.setIcon(icon)
        self.file_search_button.clicked.connect(self.browse_files)
        #start time label and entry
        self.start_time_label = QLabel("Enter the starting time:")
        self.start_time_edit = QLineEdit("")
        self.start_time_edit.setPlaceholderText("HH:MM:SS.MS")
        self.start_time_label.setToolTip("must be in the form of HH:MM:SS.MS")
        #end time label and entry
        self.end_time_label = QLabel("Enter the ending time:")
        self.end_time_edit = QLineEdit("")
        self.end_time_edit.setPlaceholderText("HH:MM:SS.MS")
        self.end_time_label.setToolTip("must be in the form of HH:MM:SS.MS")
        #audio track label and entry
        self.audio_track_label = QLabel("Enter the audio track to use:")
        self.audio_track_label.setToolTip("Takes Integer Values starting from 0")
        self.audio_track_edit = QLineEdit("")
        self.audio_track_edit.setPlaceholderText("leave blank for default")
        #subtitle track label and entry
        self.subtitle_track_label = QLabel("Enter the subtitle track to use:")
        self.subtitle_track_label.setToolTip("Takes Integer Values starting from 0")
        self.subtitle_track_edit = QLineEdit("")
        self.subtitle_track_edit.setPlaceholderText("leave blank for none")
        #checkbox to keep the cut video, if yes moves the video out, if no then leaves in the temp dir
        self.keep_video = QCheckBox("Keep cut video?")
        self.keep_video.setToolTip("copies and moves video file out of the temporary directory")
        #cut video button, trims the video to the specifications the user puts in
        self.trim_video_button = QPushButton("Cut Video")
        self.trim_video_button.setToolTip("Cuts the video to the timing needed, gets it ready for GIF making")
        self.trim_video_button.clicked.connect(self.trim_video)

        self.gif_label = QLabel("GIF OPTIONS:")
        self.gif_label.setFont(QFont("", 15))
        #keep original resolution for the gif checkbox, if yes then it keeps the gif the original res while sacrificing quality and speed
        self.keep_original_res_check = QCheckBox("Keep original resolution?")
        self.keep_original_res_check.setToolTip("worse quality and manually needs font size editing, also adds a LOT longer to the GIF generation time")
        #speed multiplier label and entry
        self.speed_label = QLabel("Speed Multiplier:")
        self.speed_label.setToolTip("Takes an integer value")
        self.speed_edit = QLineEdit()
        self.speed_edit.setPlaceholderText("Leave blank for 1")
        #caption text label and entry
        self.text_label = QLabel("Text to go on the GIF:")
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Leave blank for no text")
        #font to use label and entry
        self.font_label = QLabel("Font for the text:")
        self.font_label.setToolTip("Font must be installed on the system, spaces turn into -")
        self.font_edit = QLineEdit()
        self.font_edit.setPlaceholderText("Leave blank for defaults")
        #font size label and entry
        self.font_size_label = QLabel("Font size for the text:")
        self.font_size_label.setToolTip("integer values only")
        self.font_size_edit = QLineEdit()
        self.font_size_edit.setPlaceholderText("Leave blank for defaults")
        #text location combobox, dropdown between two choices either above the image in a white box or on top of the image in impact font
        self.text_location_label = QLabel("Where should the text be placed?")
        self.text_location_box = QComboBox()
        self.text_location_box.insertItem(0, "above_image")
        self.text_location_box.insertItem(1, "on_image")
        #create gif button, creates a gif from the outputted video with user specifications
        self.create_gif_button = QPushButton("Create GIF")
        self.create_gif_button.clicked.connect(self.create_gif)
        #reset all button, deletes everything in the temp folder to be ready for another gif creation
        self.reset_button = QPushButton("Reset All")
        self.reset_button.setToolTip("This deletes all files in the temp directory")
        self.reset_button.clicked.connect(self.delete_all)
        #reset gif button, resets just the gif componenets in case something went wrong and the gif needs to be remade
        self.reset_gif_button = QPushButton("Reset GIF")
        self.reset_gif_button.setToolTip("This deletes all of the GIF generation files while keeping the trimmed video file")
        self.reset_gif_button.clicked.connect(self.delete_failure)
        sublayout1 = QHBoxLayout()
        sublayout1.addWidget(self.reset_button)
        sublayout1.addWidget(self.reset_gif_button)
        #creates the grid layout for the widgets
        self.setWindowTitle("Video-Trimmer-GIFer")
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
        layout.addWidget(self.create_gif_button, 25, 0)
        layout.addLayout(sublayout1, 26, 0, 1, 1)

        #creates a container for the main window using the grid and then sets that as the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_files(self):
        #opens a file browser dialog when the button is pressed, then sets the text in the line to what file was chosen
        dialog = QFileDialog(self)
        if dialog.exec():
            fileName = dialog.selectedFiles()
        self.file_path_edit.setText(fileName[0])

    def trim_video(self):
        if "output.mp4" in os.listdir():
            os.remove("output.mp4") #if creating another video and one currently exists, the old one is deleted for the new
        filepath = self.file_path_edit.text().encode('unicode-escape').decode()#need to escape special characters
        backend.trim_and_encode(filepath, self.start_time_edit.text(), self.end_time_edit.text(), self.audio_track_edit.text(), self.subtitle_track_edit.text())
        if self.keep_video.isChecked(): #moves video out of the temp dir and then adds information to the filename
            start = self.start_time_edit.text().replace(":", "-")
            end  = self.end_time_edit.text().replace(":", "-")
            shutil.copyfile("output.mp4", f"../output-[{start}_{end}].mp4")

    def create_gif(self):
        #uses the create gif function from the backend.py file
        filepath = self.file_path_edit.text().encode('unicode-escape').decode()
        keep_original_res = self.keep_original_res_check.isChecked()
        text = self.text_edit.text().encode('unicode-escape').decode()
        speed = self.speed_edit.text()
        if speed == "": #sets speed to 1 if not set, needed for gifski
            speed = "1"
        backend.create_gif(filepath, keep_original_res, speed, text, self.font_edit.text(),self.font_size_edit.text(), self.text_location_box.currentText())
        start = self.start_time_edit.text().replace(":", "-")
        end  = self.end_time_edit.text().replace(":", "-")
        #adds extra info to the files when complete and moves them up a directory and out of the temp one
        if text != "":
            shutil.move("text-gif.gif", f"../output_text-[{start}_{end}].gif")
        else:
            shutil.move("gif.gif", f"../output-[{start}_{end}].gif")

    def delete_all(self):
        #dont delete unless in directory
        if "temporary-directory" not in os.getcwd():
            print("something is wrong, not deleting files...")
        else:
            for image in os.listdir("."):
                #only delete the types of files that the program will generate
                if (image.endswith(".png")) or (image.endswith(".mp4")) or (image.endswith(".gif")):
                    os.remove(image)

    def delete_failure(self):
        #dont delete unless in directory
        if "temporary-directory" not in os.getcwd():
            print("something is wrong, not deleting files...")
        else:
            for image in os.listdir("."):
                #only delete the types of files that the program will generate, doesnt delete video as this is meant for if the gif is messed up but the video is fine
                if (image.endswith(".png")) or (image.endswith(".gif")):
                    os.remove(image)

if __name__ == '__main__':
    #create temp directory
    if "temporary-directory" not in os.listdir() and "temporary-directory" not in os.getcwd():
        os.mkdir("temporary-directory")
        os.chdir("temporary-directory")
    elif "temporary-directory" in os.listdir():
        os.chdir("temporary-directory")
    #create qt app
    app = QApplication(sys.argv)
    #create and show form
    form = Form()
    form.show()
    #run the qt app
    sys.exit(app.exec())