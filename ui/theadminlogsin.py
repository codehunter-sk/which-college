from tkinter import *
from tkinter import messagebox as msgbox
import myconn as myconn
import admin_module as a_m
import frontwindow as fw3
from PIL import Image, ImageTk
def cnx2():
	global connection2, cursor2
	connection2 = myconn.myconn()
	cursor2 = connection2.cursor()
	cursor2.execute('use highedu')
def rootsw():
	global roots
	roots = Tk()
	roots.title('ColGenie')
	roots.geometry('1200x600')
	roots.resizable(0,0)
	photoicon = PhotoImage(file = '.\\images\\genieblueicon.png')
	roots.iconphoto(False, photoicon)
def onenter_valueadminid(*args):
	entryboxadminpasswd.focus_set()
def onenter_valueadminid2(*args):
	entryboxadminsecretkey.focus_set()
def showpasswdfunc(x):
	global passwd_count, valueadminpasswd, entryboxadminpasswd , showpasswdbutton
	passwd_count = x
	passwd_count += 1
	value = valueadminpasswd.get()
	if passwd_count % 2 != 0 :
		entryboxadminpasswd.destroy()
		entryboxadminpasswd = Entry(frame3, font = ('arial',15) , width = 25  , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminpasswd)
		entryboxadminpasswd.place(x = 380, y = 290)
		entryboxadminpasswd.delete(0,END)
		entryboxadminpasswd.insert(0,value)
		entryboxadminpasswd.focus_set()
		showpasswdbutton.configure(text = 'Hide password')
	else:
		entryboxadminpasswd.configure(show = '*')
		entryboxadminpasswd.focus_set()
		showpasswdbutton.configure(text = 'Show password')
def checkadmin() :
	global entryboxadminid , entryboxadminpasswd
	userid = valueadminid.get()
	passwd = valueadminpasswd.get()
	cursor2.execute(f"select md5('{passwd}')")
	passwdcrypted = cursor2.fetchall()
	passwdcrypted = passwdcrypted[0][0]
	cursor2.execute('select * from admin')
	admintablerows = cursor2.fetchall()
	if userid == '' :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
		entryboxadminid.focus_set()
	elif passwdcrypted == '' :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
		entryboxadminpasswd.focus_set()
	else:
		for row in admintablerows :
			if row[0] == userid :
				if row[2] == passwdcrypted :
					roots.destroy()
					return a_m.adminpage(row[1])
				else:
					entryboxadminpasswd.delete(0,END)
					labelcheckpwd  = Label(frame3, text = ' * Incorrect password! ' , font = ('Times New Roman', 14 ) , bg = 'brown' , fg = '#fffdd0')
					labelcheckpwd.place(x = 380 , y = 325)
					entryboxadminpasswd.focus_set()
					break
		else:
			entryboxadminpasswd.delete(0,END)
			labelcheckpwd  = Label(frame3, text = '* Check your userid!  ' , font = ('Times New Roman', 14 ) , bg = 'brown' , fg = '#fffdd0')
			labelcheckpwd.place(x = 380 , y = 325)
			entryboxadminid.focus_set()
def forgotpasswdfunc():
	global frame3a , labeladminid2 , entryboxadminid2 , labeladminsecretkey , entryboxadminsecretkey , adminloginbutton , valueadminid2 , valueadminsecretkey
	entryboxadminid.delete(0,END)
	entryboxadminpasswd.delete(0,END)

	valueadminid2 = StringVar()
	valueadminsecretkey = StringVar()

	frame3a = Frame(frame3, height = 370, width = 745 ,bd = 2, bg = '#ffcce5')
	frame3a.place(x = 240, y = 100)

	adminloginbutton.configure(state = DISABLED)

	labeladminid2 = Label(frame3a, text = 'Enter your userid:', bg = '#ffcce5', fg = '#222244',font = ('arial',28))
	labeladminid2.place(x = 10, y = 10)

	entryboxadminid2 = Entry(frame3a, font = ('Comic Sans MS',15) , width = 25 , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminid2)
	entryboxadminid2.place(x = 150, y = 60)
	entryboxadminid2.focus_set()
	entryboxadminid2.bind("<Return>",onenter_valueadminid2)

	labeladminsecretkey = Label(frame3a, text = 'Enter your secret key:', bg = '#ffcce5', fg = '#222244',font = ('MS Serif',28, 'italic'))
	labeladminsecretkey.place(x = 10, y = 110)

	entryboxadminsecretkey = Entry(frame3a, font = ('Comic Sans MS',15) , width = 25  , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminsecretkey)
	entryboxadminsecretkey.place(x = 150, y = 160)

	forgotpasswdsubmitbtn = Button(frame3a, text = 'Submit' , font = ('arial',14) , cursor = 'hand2', bg = '#ffcce5', fg = '#123456', bd = 0 , activebackground = '#bfefff', command = forgotpasswdsubmitbtncheckfunc)
	forgotpasswdsubmitbtn.place(x = 500, y = 160)

	rememeredpwdbtn = Button(frame3a, text = '    I remembered my password!     ' , font = ('arial',14) , cursor = 'hand2', bg = '#bdbdbd', fg = '#123456', bd = 0 , activebackground = '#bfefff' , command = irmbtnfunc)
	rememeredpwdbtn.place(x = 150 , y = 250)
def forgotpasswdsubmitbtncheckfunc():
	global user
	cursor2.execute('select * from admin')
	admintablerows = cursor2.fetchall()
	user = valueadminid2.get()
	secretkey = valueadminsecretkey.get()
	secretkey.replace(' ','')
	if user == '' :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
		entryboxadminid2.focus_set()
	elif secretkey == '' :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
		entryboxadminsecretkey.focus_set()
	else:
		for row in admintablerows:
			if row[0] == user :
				if row[3].replace(' ','') == secretkey.replace(' ','') :
					return forgotpasswdchangepasswdfunc()
				else:
					entryboxadminsecretkey.delete(0,END)
					labelchecksecretkey = Label(frame3a , text = ' * Incorrect secretkey! ' , font = ('Times New Roman', 18 ) , bg = '#ffcce5' , fg = '#ff0dcf')
					labelchecksecretkey.place(x = 150 , y = 200)
					entryboxadminsecretkey.focus_set()
					break
		else:
			entryboxadminsecretkey.delete(0,END)
			labelchecksecretkey = Label(frame3a , text = ' * Incorrect userid!     ' , font = ('Times New Roman', 18 ) , bg = '#ffcce5' , fg = '#ff0dcf')
			labelchecksecretkey.place(x = 150 , y = 200)
			entryboxadminid2.focus_set()
def forgotpasswdchangepasswdfunc():
	global entryboxadminsecretkey , entryboxadminid2 , valueadminpasswdnew , valueadminpasswdnew2

	valueadminpasswdnew = StringVar()
	valueadminpasswdnew2 = StringVar()

	entryboxadminid2.delete(0,END)
	entryboxadminsecretkey.delete(0,END)

	labelchecksecretkey = Label(frame3a , text = '                                    ' , font = ('Times New Roman', 18 ) , bg = '#ffcce5' , fg = '#ff0dcf')
	labelchecksecretkey.place(x = 150 , y = 200)

	labeladminid2 = Label(frame3a, text = 'Enter your new password:', bg = '#ffcce5', fg = '#222244',font = ('MS Serif',28, 'italic'))
	labeladminid2.place(x = 10, y = 10)

	entryboxadminid2 = Entry(frame3a, font = ('Comic Sans MS',15) , width = 25 , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminpasswdnew)
	entryboxadminid2.place(x = 150, y = 60)
	entryboxadminid2.focus_set()
	entryboxadminid2.bind("<Return>",onenter_valueadminid2)

	labeladminsecretkey = Label(frame3a, text = 'Confirm your new password:', bg = '#ffcce5', fg = '#222244',font = ('MS Serif',28, 'italic'))
	labeladminsecretkey.place(x = 10, y = 110)

	entryboxadminsecretkey = Entry(frame3a, font = ('Comic Sans MS',15) , width = 25  , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminpasswdnew2)
	entryboxadminsecretkey.place(x = 150, y = 160)

	forgotpasswddonebtn = Button(frame3a, text = 'Done   ' , font = ('arial',14) , cursor = 'hand2', bg = '#ffcce5', fg = '#123456', bd = 0 , activebackground = '#bfefff', command = lambda : forgotpasswdchange(user))
	forgotpasswddonebtn.place(x = 500, y = 160)
def forgotpasswdchange(x):
	pd1 = valueadminpasswdnew.get()
	pd2 = valueadminpasswdnew2.get()
	entryboxadminid2.delete(0,END)
	entryboxadminsecretkey.delete(0,END)
	if pd1 == '' or pd2 == '' :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill out the\nempty fields!')
	elif pd1 == pd2 :
		if len(pd1) >= 8 :
			cursor2.execute(f"select md5('{pd1}')")
			passwdcrypted = cursor2.fetchall()
			passwdcrypted = passwdcrypted[0][0]
			cursor2.execute(f"update admin set password = '{passwdcrypted}' where userid = '{x}'")
			msgbox.showinfo(title = 'Alert!' , message = 'Password changed!\nUse your new password to login')
			adminloginbutton.configure(state = ACTIVE)
			frame3a.destroy()
		else:
			labelchecksecretkey = Label(frame3a , text = ' * make sure your password has atleast 8 characters ' , font = ('Times New Roman', 18 ) , bg = '#ffcce5' , fg = '#ff0dcf')
			labelchecksecretkey.place(x = 150 , y = 200)
	else:
		labelchecksecretkey = Label(frame3a , text =     ' * Sorry, try again                                                       ' , font = ('Times New Roman', 18 ) , bg = '#ffcce5' , fg = '#ff0dcf')
		labelchecksecretkey.place(x = 150 , y = 200)
def irmbtnfunc():
	entryboxadminid2.delete(0,END)
	entryboxadminsecretkey.delete(0,END)
	frame3a.destroy()
	adminloginbutton.configure(state = ACTIVE)
	entryboxadminid.focus_set()
def adminloginbackbtnfunc():
	roots.destroy()
	return fw3.guestpage()
def adminloginpage():
	global frame3, valueadminid, valueadminpasswd, entryboxadminid, entryboxadminpasswd , adminloginbutton , showpasswdbutton
	rootsw()
	cnx2()
	valueadminid = StringVar()
	valueadminpasswd = StringVar()
	try:
		frame3a.destroy()
	except:
		pass

	frame3 = Frame(roots, height = 600, width = 1200, bg = 'brown')
	frame3.grid(row = 0, column = 0)

	amod_imag = ImageTk.PhotoImage(Image.open('.\\images\\adminlnbg2.png'))
	amod_imaglabel = Label(frame3 , image = amod_imag,  bg = '#000000').place(x = 0, y = 0)

	labeladminid = Label(frame3, text = 'Enter your userid:', bg = '#090D29', fg = '#ffffff',font = ('arial',24))
	labeladminid.place(x = 240, y = 140)

	entryboxadminid = Entry(frame3, font = ('arial',15) , width = 25 , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminid)
	entryboxadminid.place(x = 380, y = 190)
	entryboxadminid.focus_set()
	entryboxadminid.bind("<Return>",onenter_valueadminid)

	labeladminpasswd = Label(frame3, text = 'Enter your password:', bg = '#090D29', fg = '#ffffff',font = ('arial',24))
	labeladminpasswd.place(x = 240, y = 240)

	entryboxadminpasswd = Entry(frame3, font = ('arial',15) , width = 25  , fg = '#123456' , bg = '#fffdd0' , textvariable = valueadminpasswd, show = '*')
	entryboxadminpasswd.place(x = 380, y = 290)

	adminloginbackbutton_img = ImageTk.PhotoImage(Image.open('.\\images\\guestbtn.png'))
	adminloginbackbutton = Button(frame3, image = adminloginbackbutton_img ,bd = 0,bg = '#000033', cursor = 'hand2',activebackground = '#000033', command  = adminloginbackbtnfunc)
	adminloginbackbutton.place(x = 1035,y = 10)

	adminloginbutton_img = ImageTk.PhotoImage(Image.open('.\\images\\loginbtn.png'))
	adminloginbutton = Button(frame3,image = adminloginbutton_img,bg = '#0b204d', cursor = 'hand2',activebackground  = '#000033', bd = 0 , command  = checkadmin )
	adminloginbutton.place(x = 462, y = 350)

	showpasswdbutton = Button(frame3, text = 'Show password' , font = ('arial',14) , cursor = 'hand2' ,bd = 0, bg = '#0b1538' , activebackground = '#000033' , fg = '#fffdd0' , command = lambda : showpasswdfunc(passwd_count) )
	showpasswdbutton.place(x = 690, y = 290)

	forgotpasswdbutton = Button(frame3, text = 'Forgot password?' , font = ('arial',14) , cursor = 'hand2' ,bd = 0, bg = '#0b1538' , activebackground = '#000033' , fg = '#fffdd0' , command = forgotpasswdfunc )
	forgotpasswdbutton.place(x = 450, y = 435)

	roots.mainloop()
passwd_count = 0
if __name__ == '__main__':
	adminloginpage()
