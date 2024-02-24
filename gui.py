#the gui
#import backend
from PyQt6.QtWidgets import QApplication, QWidget
import sys

def gui():
    #creates the gui
    print("HI")

def run_all():
    print("hi")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    app.exec()
    run_all()