import cv2
import tkinter as tk
from tkinter import font 
from tkinter import Button, Label, PhotoImage, Scrollbar
from PIL import Image, ImageTk
from pytesseract import pytesseract
import os

# Initialize the camera
camera = cv2.VideoCapture(0)


camera.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


def detect_phone_screen(image): #Assists with detecting phone screens to ensure best possible quality for the text conversion.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(approx)
            cropped = image[y:y+h, x:x+w]
            return cropped
        return image
    

'''while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    cropped = detect_phone_screen(frame)
    cv2.imshow("Cropped Screen", cropped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()'''


def update_frame():
    _, frame = camera.read()
    if frame is not None:
        detect_phone_screen(frame) #Calls the detect_phone_screen function using the 'frame' (image from camera being captured)
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
        image_check()
        conversion()  # Call the conversion function after saving the frame


def image_check():
    img = Image.open('test.jpg')
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    result = pytesseract.image_to_string(img, config=custom_config)
    print (result)
    update_console(result)

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
    #update_console(translated_text)


def update_console(text): # Function to update text that gets displayed in console and allow it to be copied
    console_text.delete(1.0, tk.END)
    console_text.insert(tk.END, text)
    console_text.bind("<Button-1>", lambda event: console_text.config(state=tk.NORMAL))
    console_text.bind("<FocusOut>", lambda event: console_text.config(state=tk.DISABLED))

# Create a Tkinter window
root = tk.Tk()
root.title("iPhone Info Detection (click window first)")
custom_font = font.Font(family='Courier',size=12)

# Set the window size and background
root.geometry("1920x1080")
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
console_text = tk.Text(console, wrap='word',height=100, width=100,font=custom_font)
console_text.pack()




# Set up key bindings for save and close
root.bind('<s>', lambda e: save_frame())
root.bind('<q>', lambda e: close_window())

# Start updating the frame
update_frame()

# Run the Tkinter event loop
root.mainloop()



