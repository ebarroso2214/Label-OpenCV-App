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
    root.destroy() # Closes window

def conversion():
    path_to_tesseract = r'/opt/homebrew/bin/tesseract'  # Adjust path as necessary
    Imagepath = 'test.jpg'
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(Imagepath))
    translated_text = text.strip()
    # print(translated_text) # Tests to see if information does get saved and displayed
    update_console(translated_text)


def update_console(text): # Function to update text that gets displayed in console and allow it to be copied
    console_text.delete(1.0, tk.END)
    console_text.insert(tk.END, text)
    console_text.bind("<Button-1>", lambda event: console_text.config(state=tk.NORMAL))
    console_text.bind("<FocusOut>", lambda event: console_text.config(state=tk.DISABLED))

# Create a Tkinter window
root = tk.Tk()
root.title("iPhone Info Detection (click window first)")

# Set the window size and background
root.geometry("400x800")
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


#Create an output console for text to be displayed in
console = tk.Toplevel(root)
console.title('Output console')
console.geometry('400x300+400+100')
console_text = tk.Text(console, wrap='word',height=100, width=100)
console_text.pack()




# Set up key bindings for save and close
root.bind('<s>', lambda e: save_frame())
root.bind('<q>', lambda e: close_window())

# Start updating the frame
update_frame()

# Run the Tkinter event loop
root.mainloop()



