from tkinter import *
from PIL import Image, ImageTk


root = Tk()


def second_win():
    root = Tk()
    root.title("Main page")
    root.geometry("700x500")
    b3 = Label(root, text="let see", relief="solid")
    b3.place(x=200, y=10)


root.geometry("700x500")
load = Image.open("images\\bg.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.place(x=0, y=0)
img1 = PhotoImage(file="images\\button.png")
b1 = Button(root, image=img1, bd=0, bg="#34495e",
            activebackground="#34495e", command=second_win)
b1.place(x=255, y=443)
img2 = PhotoImage(file="images\\Startsidan.png")
b2 = Label(root, image=img2, bg="#34495e")
b2.place(x=200, y=5)
root.mainloop()
