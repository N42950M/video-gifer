#the gui
import backend
from tkinter import BOTTOM, Button, Entry, Frame, Label, StringVar, Tk

def label_entry_pack(label_desc, entry_text, frame, entry_list:list):
    # creates the labels 
    text = StringVar()
    text.set(label_desc)
    label = Label(frame, textvariable=text)
    label.pack()
    entry = Entry(frame, width = 30,bd=2,)
    entry.insert(0,entry_text)
    entry.pack(padx=5,pady=5)
    entry_list.append(entry)

def gui():
    #creates the gui
    e_list = []
    base = Tk()
    base.geometry("200x500")
    frame = Frame(base)
    frame.pack()
    file_label_text = "Path to File:"
    file_entry_text = ""
    start_label_text = "Start Time:"
    start_entry_text = ""
    end_label_text = "End Time:"
    end_entry_text = ""
    scale_label_text = "Scale gif to same size as video? (True or False)"
    scale_entry_text = "False"
    speed_label_text = "Multiply Speed By:"
    speed_entry_text = "1"
    text_label_text = "Text for the GIF:"
    text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    # text_label_text = "Text for the GIF:"
    # text_entry_text = ""
    label_entry_pack(file_label_text,file_entry_text,frame,e_list)
    label_entry_pack(start_label_text,start_entry_text,frame,e_list)
    label_entry_pack(end_label_text,end_entry_text,frame,e_list)
    label_entry_pack(scale_label_text,scale_entry_text,frame,e_list)
    label_entry_pack(speed_label_text,speed_entry_text,frame,e_list)
    label_entry_pack(text_label_text,text_entry_text,frame,e_list)
    bottom_frame = Frame(base)
    bottom_frame.pack(side=BOTTOM)
    run_button = Button(bottom_frame, text = "", command=lambda:run_all(e_list[0],e_list[1],e_list[2],e_list[3],e_list[4],e_list[5]), font = ("Impact 15"))
    run_button.pack(pady=5)
    base.title("")
    #loops to wait for inputs
    base.mainloop()

def run_all():
    print("hi")