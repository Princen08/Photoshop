import tkinter
import numpy as np
import imutils
from tkinter import filedialog
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.ttk import Style
from PIL import ImageEnhance
from functools import partial
from PIL.ImageEnhance import Contrast
from numpy import asarray
from PIL import *
from cv2 import cv2
from matplotlib import image


global root
root = Tk()
root.title("Photo Editor")
root.geometry('2000x1500')
root.configure(bg='grey')



def ShowAllButton(path, canvas):
    back = Button(root, text="Back", command=lambda: showImage(path, canvas), height=3, width=15,
                  activebackground='#345', activeforeground='red')
    back.place(x=20, y=10)
    edgedetection = Button(root, text="Edge Detection", command=lambda: EdgeDetection(canvas, path), height=3, width=15,
                           activebackground='#345', activeforeground='red')
    edgedetection.place(x=20, y=70)
    blur = Button(root, text="Blur", command=lambda: Blur(canvas, path), height=3, width=15, activebackground='#345',
                  activeforeground='red')
    blur.place(x=20, y=130)
    cartoonize = Button(root, text="Cartoonize", command=lambda: Cartoonize(canvas, path), height=3, width=15,
                        activebackground='#345', activeforeground='red')
    cartoonize.place(x=20, y=190)
    blackandwhite = Button(root, text="Black and White", command=lambda: BlackandWhite(canvas, path), height=3,
                           width=15, activebackground='#345', activeforeground='red')
    blackandwhite.place(x=20, y=250)
    enhance = Button(root, text="Inhance", command=lambda: Enhancement(canvas, path), height=3, width=15,
                     activebackground='#345', activeforeground='red')
    enhance.place(x=20, y=310)
    bright = Button(root, text="Brightness", command=lambda: Brightness(path, canvas), height=3, width=15,
                    activebackground='#345', activeforeground='red')
    bright.place(x=20, y=370)
    rotate = Button(root, text="Rotate", command=lambda: Rotate(canvas, path), height=3, width=15,
                    activebackground='#345', activeforeground='red')
    rotate.place(x=20, y=430)
    text = Button(root, text="Add Text", command=lambda: takeText(canvas, path), height=3, width=15,
                  activebackground='#345', activeforeground='red')
    text.place(x=20, y=490)
    Contrast = Button(root, text="Contrast", command=lambda: contrast(canvas, path), height=3, width=15,
                  activebackground='#345', activeforeground='red')
    Contrast.place(x=20, y=550)



global last_value_of_con
last_value_of_con = 0

def contrast_change(x,path):
    global last_value_of_con
    img = cv2.imread(path)
    contrast_img = cv2.addWeighted(img, x, np.zeros(img.shape, img.dtype), 0, 0)
    cv2.imshow("Contrast", contrast_img)
    last_value_of_con = x


def contrast(canvas,path):
    trackbars_img = np.uint8(np.full((50, 500, 3), 255))
    cv2.imshow('Contrast', trackbars_img)
    cv2.createTrackbar('Contrast', 'Contrast', 1, 10, partial(contrast_change, path=path))
    cv2.waitKey(0)
    img = cv2.imread(path)
    contrast_img = cv2.addWeighted(img, last_value_of_con, np.zeros(img.shape, img.dtype), 0, 0)
    cv2.imwrite('Contrast.png', contrast_img)
    showImage('Contrast.png', canvas)

def take(canvas, path, inputtxt, add):
    txt = inputtxt.get("1.0", "end-1c")
    inputtxt.destroy()
    add.destroy()
    img = cv2.imread(path)
    new_img = cv2.putText(img, txt, org=(0, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 0, 0),thickness=2)
    cv2.imwrite('TextImage.png', new_img)
    showImage('TextImage.png', canvas)


def takeText(canvas, path):
    inputtxt = tkinter.Text(root, height=5, width=20)
    inputtxt.pack()
    add = Button(root, text="Done", command=lambda: take(canvas, path, inputtxt, add), height=3, width=10,
                 activebackground='#345', activeforeground='red')
    add.place(x=730, y=680)
    # add.destroy()


def BlackandWhite(canvas, path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    cv2.imwrite('BlackandWhite.png', gray)
    showImage('BlackandWhite.png', canvas)


def showImage(path, canvas):
    img = PhotoImage(file=path)
    canvas.create_image(0, 0, anchor=NW, image=img)
    root.mainloop()


def Cartoonize(canvas, path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    data = np.float32(img).reshape((-1, 3))
    cv2.imwrite('Cartoon.png', cartoon)
    showImage('Cartoon.png', canvas)


global last_value_of_rot
last_value_of_rot = 0


def rotate_change(x, path):
    global last_value_of_rot
    img = cv2.imread(path)
    Rotated_image = imutils.rotate(img, angle=x)
    cv2.imshow("Rotate", Rotated_image)
    last_value_of_rot = x


def Rotate(canvas, path):
    trackbars_img = np.uint8(np.full((50, 500, 3), 255))
    cv2.imshow('Rotate', trackbars_img)
    cv2.createTrackbar('Rotate', 'Rotate', 1, 360, partial(rotate_change, path=path))
    cv2.waitKey(0)
    img = cv2.imread(path)
    Rotated_image = imutils.rotate(img, angle=last_value_of_rot)
    cv2.imwrite('Rotate.png', Rotated_image)
    showImage('Rotate.png', canvas)


global last_value_of_brig
last_value_of_brig = 0


def brightness_change(x, path):
    global last_value_of_brig
    img = cv2.imread(path)
    in_matrix = np.ones(img.shape, dtype='uint8') * x
    new_img = cv2.add(img, in_matrix)
    cv2.imshow("Bright", new_img)
    last_value_of_brig = x


def Brightness(path, canvas):
    trackbars_img = np.uint8(np.full((50, 500, 3), 255))
    cv2.imshow('Brightness', trackbars_img)
    cv2.createTrackbar('Brightness', 'Brightness', 50, 100, partial(brightness_change, path=path))
    cv2.waitKey(0)
    img = cv2.imread(path)
    in_matrix = np.ones(img.shape, dtype='uint8') * last_value_of_brig
    new_img = cv2.add(img, in_matrix)
    cv2.imwrite('Bright.png', new_img)
    showImage('Bright.png', canvas)


def Blur(canvas, path):
    img = cv2.imread(path)
    Gaussian = cv2.GaussianBlur(img, (21, 21), 0)
    cv2.imwrite('Blur.png', Gaussian)
    showImage('Blur.png', canvas)


def EdgeDetection(canvas, path):
    img = cv2.imread(path)
    edges = cv2.Canny(img, 100, 200)
    cv2.imwrite('EdgeDetection.png', edges)
    showImage('EdgeDetection.png', canvas)


def Enhancement(canvas, path):
    img = cv2.imread(path)
    alpha = 1.5
    beta = 10
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    cv2.imwrite('Enhancement.png', adjusted)
    showImage('Enhancement.png', canvas)


global canvas


def CreateFrame(path):
    root.geometry('2000x1500')
    im = Image.open(path)
    canvas = Canvas(root, width=im.width, height=im.height)
    canvas.pack()
    ShowAllButton(path, canvas)
    showImage(path, canvas)


global path


def SelectImage():
    path = filedialog.askopenfilename()
    if path != "":
        b.pack_forget()
        CreateFrame(path)


global b

b = Button(root, text="Select Image", font=('arial bold', 10), command=SelectImage, height=3, width=10,
           activebackground='#345', activeforeground='red')
b.pack(pady=50)

root.mainloop()
