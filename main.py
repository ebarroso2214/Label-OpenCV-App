"""
import cv2
from pytesseract import pytesseract
import numpy as np
import os

from PIL import Image

camera = cv2.VideoCapture(0)
translated_text = None

while True:
    _,image=camera.read()
    cv2.imshow('text detection',image)
    if cv2.waitKey(1)&0xFF==ord('s'):
        cv2.imwrite('test.jpg',image)
        

    elif cv2.waitKey(1)&0xFF==ord('q'):
        break

camera.release()
cv2.destroyAllWindows()


def conversion():
    path_to_tesseract =r'/opt/homebrew/bin/tesseract' #File location can also be /usr/bin/tesseract depending on if you use M1+ macs or intel macs.
    Imagepath = 'test.jpg' 
    pytesseract.tesseract_cmd=path_to_tesseract
    text= pytesseract.image_to_string(Image.open(Imagepath))
    #print(text[:-1]) test to see if it turns to text and prints accurately
    translated_text = text[:-1]
    print (translated_text)

    #filepath = os.path.join('')

    #This portion will open a txt file and save the image to text variable
    with open("image2text.txt","w") as f:
        f.write(translated_text)

    with open('image2text.txt') as f:
        print(f.read())

conversion()
"""

import cv2
import tkinter as tk
from tkinter import Button, Label, PhotoImage, Scrollbar
from PIL import Image, ImageTk
from pytesseract import pytesseract
import os

# Initialize the camera
camera = cv2.VideoCapture(0)

def update_frame():
    _, frame = camera.read()
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
        lbl.image = imgtk  # keep a reference to prevent garbage collection
    lbl.after(10, update_frame)  # update every 10 ms

def save_frame():
    _, frame = camera.read()
    if frame is not None:
        cv2.imwrite('test.jpg', frame)
        conversion()  # Call the conversion function after saving the frame

def close_window():
    camera.release()
    root.destroy()

def conversion():
    path_to_tesseract = r'/opt/homebrew/bin/tesseract'  # Adjust path as necessary
    Imagepath = 'test.jpg'
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(Imagepath))
    translated_text = text.strip()
    print(translated_text)
    update_console(translated_text)


def update_console(text):
    console_text.insert(tk.END, text)
    console_text.bind("<Button-1>", lambda event: text_widget.config(state=tk.NORMAL))
    console_text.bind("<FocusOut>", lambda event: text_widget.config(state=tk.DISABLED))

# Create a Tkinter window
root = tk.Tk()
root.title("iPhone Info Detection (click window first)")

# Set the window size and background
root.geometry("400x300")
root.configure(bg="black")

# Create a label to display the video frame
lbl = tk.Label(root)
lbl.pack()

# Create a button to save the frame
btn_save = Button(root, text="Save Frame (Press 's')", command=save_frame)
btn_save.pack()

# Create a button to close the window
btn_close = Button(root, text="Close Window (Press 'q')", command=close_window)
btn_close.pack()

# Create a Label widget for the console output
'''console_label = Label(root,text="", bg="black", fg="white", wraplength=380, justify=tk.LEFT)
console_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)'''

console = tk.Toplevel(root)
console.title('Output console')
console.geometry('400x300+400+100')
console_text = tk.Text(console, wrap='word',height=5, width=30)
console_text.pack()




# Set up key bindings for save and close
root.bind('<s>', lambda e: save_frame())
root.bind('<q>', lambda e: close_window())

# Start updating the frame
update_frame()

# Run the Tkinter event loop
root.mainloop()



