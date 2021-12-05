from tkinter import *
from PIL import Image, ImageTk
import frontwindow as fw3

def rootfw() :
	global rootf
	rootf = Tk()
	rootf.title('ColGenie')
	rootf.geometry('1200x600')
	rootf.resizable(0,0)
	photoicon = PhotoImage(file = '.\\images\\genieblueicon.png')
	rootf.iconphoto(False, photoicon)

def go2guestpgbtnfunc():
	rootf.destroy()
	return fw3.guestpage()

def mainpg() :
	rootfw()

	framemaina = Frame(rootf,height = 1200,width = 600,bd = 0)
	framemaina.place(x = 0,y = 0)

	imagload = Image.open('.\\images\\genieblue2.png')
	imag = ImageTk.PhotoImage(imagload)
	imaglabel = Label(framemaina , image = imag, bd = 0,  bg = '#000000').grid(row = 0, column = 0)

	go2guestpgbtn = Button(framemaina,cursor = 'hand2',font = ('calibri',15), bd = 0,width = 12, bg = '#F2F0F9',text = "Enter", command = go2guestpgbtnfunc)
	go2guestpgbtn.place(x = 720,y = 520)

	rootf.mainloop()

mainpg()
