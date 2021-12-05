from tkinter import *
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
import myconn as myconn
import user_module as u_m
import theadminlogsin as tali

def cnx():
	global connection2 , cursor2
	connection2 = myconn.myconn()
	cursor2 = connection2.cursor()
	cursor2.execute('use highedu')

def rootw():
	global root
	root = Tk()
	root.title('ColGenie')
	root.geometry('1200x600')
	root.resizable(0,0)
	photoicon = PhotoImage(file = '.\\images\\genieblueicon.png')
	root.iconphoto(False, photoicon)

def entryfunc(x):
	global entryboxguestid
	try:
		entryboxguestid.destroy()
		gobutton.destroy()
		gobackbutton.destroy()
	except:
		pass

	def typing(event):
		entryboxguestid.delete(0,END)

	def nottyping(event):
		if x:
			entryboxguestid.insert(0,'Enter your new guest id')
		else:
			entryboxguestid.insert(0,'Enter your guest id')

	valueguestid = StringVar()

	getstartedbuttonold.destroy()
	getstartedbuttonnew.destroy()

	entryboxguestid = Entry(frame1, width = 20 , font = ('arial',20) , bg = '#cfdfe6' , bd = 1, fg ='#150D46', textvariable = valueguestid)
	entryboxguestid.place(x = 450,y = 170)

	entryboxguestid.bind("<FocusIn>", typing)
	entryboxguestid.bind('<FocusOut>', nottyping)

	gobutton = Button(frame1, image = gobutton_img , cursor = 'hand2', bd = 0, command = lambda : checkuser(valueguestid.get(),x))
	gobutton.place(x = 800, y = 170)

	gobackbutton = Button(frame1, cursor = 'hand2', bd = 0)
	gobackbutton.place(x = 465, y = 223)

	if x:
		gobackbutton.config(image = getstartedbuttonold_img, command = lambda : entryfunc(0))
		entryboxguestid.insert(0,'Enter your new guest id')

		msgbox.showinfo(title = 'Alert!' , message = 'Enter a 8 character id\n(And make sure to remember it!)')
	else:
		gobackbutton.config(image = getstartedbuttonnew_img, command = lambda : entryfunc(1))
		entryboxguestid.insert(0,'Enter your guest id')


def checkuser(id,new):
	cnx()
	cursor2.execute('select * from user')
	tablerows = cursor2.fetchall()
	
	if id == '' or id == 'Enter your guest id' or id == 'Enter your new guest id' :
		entryboxguestid.delete(0,END)
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
		if new:
			entryboxguestid.insert(0,'Enter your new guest id')
			entryboxguestid.select_to(len('Enter your new guest id'))
		else:
			entryboxguestid.insert(0,'Enter your guest id')
			entryboxguestid.select_to(len('Enter your guest id'))
	elif not new :
		for row in tablerows :
			if row[0] == id :
				root.destroy()
				u_m.userpage(row[0],row[1],0)
				break
		else:
			msgbox.showinfo(title = 'Alert!' , message = 'Sorry id doesn\'t exist\nMake sure everything is correct!')
			entryboxguestid.delete(0,END)
	elif new:
		if len(id) != 8 :
			msgbox.showinfo(title = 'Alert!' , message = 'Make sure that your id has\nexactly 8 characters!')
			entryboxguestid.delete(0,END)
		else:
			for row in tablerows :
				if row[0] == id :
					msgbox.showinfo(title = 'Alert!' , message = 'Sorry...\nTry out another id!')
					entryboxguestid.delete(0,END)
					break
			else:
				root.destroy()
				u_m.userpage(id,'i\'m ColGenie. (To exit, just type exit or quit).\nEnter your name to get started.',1)


def helpbtnfunc():
	msgbox_msg = "If you've logged in before,click I've been here button.\nIf you're new, click I'm new and type in a 8 character guestid of your choice.\nThis is just to make sure that if you come back again, you will not have to enter all the data again"
	msgbox.showinfo(title = 'Log in Help' , message = msgbox_msg)


def adminbtnfunc():
	root.destroy()
	return tali.adminloginpage()

def guestpage():
	global frame1 , gobutton_img ,  getstartedbuttonold , getstartedbuttonold_img , getstartedbuttonnew , getstartedbuttonnew_img , adminbutton
	rootw()
	cnx()

	try:
		entryboxadminid.delete(0,END)
		entryboxadminpasswd.delete(0,END)
		frame3.destroy()
	except :
		pass

	frame1 = Frame(root, height = 600, width = 1200, bg = 'black')
	frame1.grid(row = 0, column = 0)

	gobutton_img = ImageTk.PhotoImage(Image.open('.\\images\\loginblue.png'))

	imagbgload = Image.open('.\\images\\colbg_fw.png')
	imagbg = ImageTk.PhotoImage(imagbgload)
	imagbglabel = Label(frame1, image = imagbg).place(x = 0,y = 0)

	helpbutton_img = ImageTk.PhotoImage(Image.open('.\\images\\helpbtn.png'))
	helpbutton = Button(frame1, image = helpbutton_img , cursor = 'hand2',bd = 0 , command  = helpbtnfunc)
	helpbutton.place(x = 1035,y = 20)

	getstartedbuttonold_img = ImageTk.PhotoImage(Image.open('.\\images\\beenhere.png'))
	getstartedbuttonold = Button(frame1, image = getstartedbuttonold_img , cursor = 'hand2', bd = 0, command = lambda : entryfunc(0))
	getstartedbuttonold.place(x = 465, y = 223)

	getstartedbuttonnew_img = ImageTk.PhotoImage(Image.open('.\\images\\iamnew.png'))
	getstartedbuttonnew = Button(frame1, image = getstartedbuttonnew_img , cursor = 'hand2', bd = 0, command = lambda : entryfunc(1))
	getstartedbuttonnew.place(x = 715, y = 223)

	adminbutton_img = ImageTk.PhotoImage(Image.open('.\\images\\adminbtn.png'))
	adminbutton = Button(frame1, image = adminbutton_img , cursor = 'hand2',  bd = 0  , command  = adminbtnfunc)
	adminbutton.place(x = 1035,y = 80)

	root.mainloop()

if __name__ == '__main__':
	guestpage()
