import cv2
from pytesseract import pytesseract
import numpy as np

from PIL import Image

camera = cv2.VideoCapture(0)
translated_text = None

while True:
    _,image=camera.read()
    cv2.imshow('text detection',image)
    if cv2.waitKey(1)&0xFF==ord('s'):
        cv2.imwrite('test.jpg',image)
        break

camera.release()
cv2.destroyAllWindows
#usr/local/bin/tesseract.exe

def conversion():
    path_to_tesseract =r'/usr/local/bin/tesseract' ##For this to work, need to add tesseract to PATH
    Imagepath = 'test.jpg'
    pytesseract.tesseract_cmd=path_to_tesseract
    text= pytesseract.image_to_string(Image.open(Imagepath))
    #print(text[:-1]) test to see if it turns to text and prints accurately
    translated_text = text[:-1]
    print (translated_text)

    #This portion will open a txt file and save the image to text variable
    f = open("image2text.txt","w")
    f.write(translated_text)

    f = open('image2text.txt')

conversion()