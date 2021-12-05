from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
from tkinter import *
import frontwindow as fw3
from college_uploads import *
import myconn as myconn
from PIL import Image, ImageTk

upd_option =''
def cnxa():
	global connection2, cursor2
	connection2 = myconn.myconn()
	cursor2 = connection2.cursor()
	cursor2.execute('use highedu')

def rootaw():
	global roota
	roota = Tk()
	roota.title('ColGenie')
	roota.geometry('1200x600')
	roota.resizable(0,0)
	photoicon = PhotoImage(file = '.\\images\\genieblueicon.png')
	roota.iconphoto(False, photoicon)

def adminlogoutbtnfunc():
	roota.destroy()
	return fw3.guestpage()

def comeoutofpg():
	frame4.destroy()

def bulk_upload(opt):
	global frame4
	upd_option = opt

	try:
		comeoutofpg()
	except :
		pass

	def get_file_name(file_entry):
		file_name = fd.askopenfilename(initialdir = "/", title = "Select file",filetypes = (("CSV Files","*.csv"),))
		file_entry.delete(0,END)
		file_entry.insert(0,file_name)
		if file_name.strip() != "" :
			csv_uploadbtn.configure(state = ACTIVE)
			adminmnpgbtn.configure(state = DISABLED)
		else:
			csv_uploadbtn.configure(state = DISABLED)
			adminmnpgbtn.configure(state = ACTIVE)
	def upload_csvfile(entrybox = None):
		if opt == 'college':
			retmsg = upload_coldata(entrybox.get())
			msgbox.showinfo(title = 'Alert!' , message = retmsg)
			entrybox.focus_set()
		elif opt == 'course':
			retmsg = upload_coursedata(entrybox.get())
			msgbox.showinfo(title = 'Alert!' , message = retmsg)
			entrybox.focus_set()
		elif opt == 'courseid':
			retmsg = upload_courseid(entrybox.get())
			msgbox.showinfo(title = 'Alert!' , message = retmsg)
			entrybox.focus_set()
		adminmnpgbtn.configure(state = ACTIVE)
		comeoutofpg()

	def select_reset(entrybox = None):
		entrybox.delete(0,END)
		adminmnpgbtn.configure(state = ACTIVE)
		csv_uploadbtn.configure(state = DISABLED)

	frame4 = Frame(roota, height = 500, width = 950, bg = '#fffacd')
	frame4.place(x = 250, y = 100)

	adminmodroot_imaglabel = Label(frame4 , image = adminmodroot_imag,  bd = 0).place(x = 0, y = 0)

	entry_csv = Entry(frame4, width=50, bg = '#d9dbde')
	entry_csv.place(x = 250, y =70,height = 20)

	csv_selectlbl = Label(frame4, bg = '#ffffff' ,font = ('Helvetica',12,'bold'), text="Select "+upd_option+" Data CSV")
	csv_selectlbl.place(x = 50,y = 70)

	csv_browsebtn = Button(frame4, text ="Browse...",  cursor = 'hand2',width=10, command = lambda: get_file_name(entry_csv))
	csv_browsebtn.place(x = 590,y = 70)

	csv_uploadbtn = Button(frame4, text ="Upload", cursor = 'hand2', command = lambda: upload_csvfile(entry_csv), width=10)
	csv_uploadbtn.place( x = 250, y = 120)
	csv_uploadbtn.configure(state = DISABLED)

	csv_cancelbtn = Button(frame4, text ="Reset",  cursor = 'hand2', command = lambda: select_reset(entry_csv), width=10)
	csv_cancelbtn.place( x = 330, y = 120)

	adminmnpgbtn = Button(frame4, text = 'Main page' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 15 , command  =  comeoutofpg  )
	adminmnpgbtn.place(x = 700,y = 70)


def reset_data():
	global frame4
	try:
		comeoutofpg()
	except :
		pass

	def reset_data_func(opt):
		msg_val = msgbox.askokcancel(title = 'Warning', message = 'Data will be deleted forever\nreset?')
		if msg_val:
			if opt == 1:
				cursor2.execute('delete from college')
			elif opt == 2:
				cursor2.execute('delete from course')
			elif opt == 3:
				cursor2.execute('delete from codes')
			connection2.commit()
			msgbox.showinfo(title = 'Alert!' , message = 'Successfully completed reset!')
		comeoutofpg()

	frame4 = Frame(roota, height = 500, width = 950, bg = '#fffacd')
	frame4.place(x = 250, y = 100)

	adminmodroot_imaglabel = Label(frame4 , image = adminmodroot_imag,  bd = 0).place(x = 0, y = 0)

	adminmnpgbtn = Button(frame4, text = 'Main page' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 15 , command  =  comeoutofpg  )
	adminmnpgbtn.place(x = 700,y = 70)

	warningtext = 'WARNING! Your data will be deleted completely!'
	warninglabel = Label(frame4, text = warningtext, bg = '#ffffff', fg = '#990000',font = ('cambria',25,'bold'))
	warninglabel.place(x = 50,y = 15)

	resetcollegebtn = Button(frame4, text = 'Delete college data' , bg = '#f0fff0' , fg = '#100000',font = ('Helvetica',12), command = lambda: reset_data_func(1) )
	resetcollegebtn.place(x = 150,y = 380)

	resetcoursebtn = Button(frame4, text = 'Delete course data' , bg = '#f0fff0' , fg = '#100000',font = ('Helvetica',12), command = lambda: reset_data_func(2) )
	resetcoursebtn.place(x = 350,y = 380)

	resetcourseidbtn = Button(frame4, text = 'Delete courseid data' , bg = '#f0fff0' , fg = '#100000',font = ('Helvetica',12), command = lambda: reset_data_func(3) )
	resetcourseidbtn.place(x = 550,y = 380)


def adminpage(name):
	global adminmodroot_imag
	rootaw()
	cnxa()

	frame6 = Frame(roota, height = 500, width = 250, bg = '#507063')
	frame6.place(x = 0, y = 100)

	frame6_imag = ImageTk.PhotoImage(Image.open('.\\images\\adminlf.png'))
	frame6_imaglabel = Label(frame6 , image = frame6_imag,  bd = 0).place(x = 0, y = 0)

	frame1a = Frame(roota, height = 100, width = 1200, bg = '#507063')
	frame1a.grid(row = 0, column = 0)

	header_img = ImageTk.PhotoImage(Image.open('.\\images\\colbg_head.png'))

	labelcbb = Label(frame1a,image = header_img, bg = '#E0D6D7')
	labelcbb.place(x = 0, y = 0)

	adminmodroot_imag = ImageTk.PhotoImage(Image.open('.\\images\\admupload.png'))
	adminmodroot_imaglabel = Label(roota , image = adminmodroot_imag,  bd = 0).place(x = 250, y = 100)

	welcometext = 'Welcome  ' + name
	welcomelabel = Label(roota, text = welcometext, bg = '#ffffff', fg = '#990000',font = ('cambria',25,'bold'))
	welcomelabel.place(x = 400,y = 115)

	uploadbulkbtn1 = Button(frame6, text = 'College data Upload' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 18 , command = lambda : bulk_upload('college') )
	uploadbulkbtn1.place(x = 40,y = 30)

	uploadbulkbtn1 = Button(frame6, text = 'Course data Upload' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 18 , command = lambda : bulk_upload('course') )
	uploadbulkbtn1.place(x = 40,y = 80)

	crecoldatabtn = Button(frame6, text = 'CourseId data Upload' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 18 , command = lambda : bulk_upload('courseid') )
	crecoldatabtn.place(x = 40,y = 130)

	resetdatabtn = Button(frame6, text = 'Reset data' , font = ('Helvetica',12), cursor = 'hand2',  bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 18 , command = reset_data )
	resetdatabtn.place(x = 40,y = 180)

	adminlogoutbutton = Button(frame6, text = 'Log out' , font = ('Helvetica',12), cursor = 'hand2', bg = '#f0fff0', activebackground = '#f0eff0' , fg = '#1b4b1e', width  = 20 , command  = adminlogoutbtnfunc)
	adminlogoutbutton.place(x = 30,y = 400)

	roota.mainloop()
if __name__ == '__main__':
	adminpage('SSK Admin direct access')
