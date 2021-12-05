from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk
from PIL import Image, ImageTk
import random
import myconn as myconn
import frontwindow as fw3
from tkinter import filedialog
from fpdf import FPDF


def cnxu():
	global connection3 , cursor3
	connection3 = myconn.myconn()
	cursor3 = connection3.cursor(buffered=True)
	cursor3.execute('use highedu')

def rootuw():
	global rootu
	rootu = Tk()
	rootu.title('ColGenie')
	rootu.geometry('1200x600')
	rootu.resizable(0,0)
	photoicon = PhotoImage(file = '.\\images\\genieblueicon.png')
	rootu.iconphoto(False, photoicon)

def logout():
	rootu.destroy()
	return fw3.guestpage()

def give_errorchat():
	chats = ['Sorry, I didn\'t get you','Pardon?','Can you please repeat?']
	giveuchat(random.choice(chats))

def umvarfunc(var):
	global umvar
	if not var :
		logout()
	elif var == '1' :
		if umvar == -1 :
			frame5.destroy()
			umvar += 1
			user0()
		elif umvar == 0 :
			umvar += 1
			get_user0_datas()
		elif umvar == 1:
			giveuchat('Give \'back\' to go and change your data...\nor')
			giveuchat(optiontext)
	elif var == '2' :
		if umvar == 0 :
			giveuchat('Hey there , just type exit (or quit) to go back to entry page')
		elif umvar == 1 :
			frame5.destroy()
			umvar -= 1
			user0()

def giveuchat(chat):
	global cwnumb, optiontext
	chatWindow.configure(state = NORMAL)
	chatWindow.insert(END, 'CGBot:\n'+chat+'\n')
	chatWindow.see('end')
	chatWindow.configure(state = DISABLED)
	cwnumb += len(('CGBot:\n'+chat+'\n').split('\n'))-1

	optiontext = 'Enter\n1-to get college names from your city\n2-to get college names from other cities\n3-to get college names based on specific courses\n4-to get college names based on other cities and specific courses\nEnter \'report\' to download as PDF'

def getuchat(chat):
	global cwnumb
	chaat = 'You: ' + chat
	chatWindow.configure(state = NORMAL)
	messageWindow.delete('0.0', END)
	chatWindow.insert(END, (' ').join(chaat.split('\n')) + '\n')
	chatWindow.tag_add('tag1', str(cwnumb)+'.0' , str(cwnumb)+'.'+str(len(chaat)))
	chatWindow.tag_config('tag1', foreground = '#7E1005', font=('Ink Free',16,'bold'))
	cwnumb = cwnumb + 1 
	chatWindow.see("end")
	chatWindow.configure(state = DISABLED)
	chat = chat.lower()
	if 'exit' in chat or 'quit' in chat or 'bye' in chat:
		umvarfunc('')

	elif umvar == -1 :

		if genudvar == 0 and ('next' in chat or 'back' in chat):
			giveuchat('Just type exit (or quit) to go back to entry page; or u could give your details and continue.')
		else:
			get_newuser_data_func(chat.strip())

	elif 'next' in chat :
		umvarfunc('1')

	elif 'back' in chat :
		umvarfunc('2')

	elif 'report' in chat :
		if reportflag:
			pdf_report()
			giveuchat(optiontext)
		else:
			giveuchat('No report available')

	elif umvar == 1 :
		if chat in ('1','2','3','4'):
			user1(chat)
		else:
			giveuchat('Enter 1 , 2 , 3 or 4 or back or quit')
	else:
		give_errorchat()


def store_newuser_data():
	global umvar
	cursor3.execute(f"insert into user(userid , name ,  phymark , chemark , mathmark , biomark ) values('{uid}','{genudata[0][:30]}','{genudata[1]}','{genudata[2]}','{genudata[3]}','{genudata[4]}')")
	connection3.commit()
	umvar += 1
	user0()


def get_newuser_data_func(chat):
	global genudvar , genudata

	if not genudvar :
		genudata.append(chat)
		genudvar += 1
		giveuchat('If you didn\'t attend the specific exam type "nil".')
		giveuchat(random.choice(chats2)+' '+chats1[genudvar-1]+' ?')
	elif genudvar in [1,2,3,4] :
		if 'nil' in chat :
			genudata.append('0')
			genudvar += 1
			if genudvar != 5 :
				giveuchat(random.choice(chats2)+' '+chats1[genudvar-1]+' ?')
			else :
				store_newuser_data()
		elif (chat.isdigit()) and (len(chat) < 3 or chat == '100') :
			genudata.append(chat)
			genudvar += 1
			if genudvar != 5 :
				giveuchat(random.choice(chats2)+' '+chats1[genudvar-1]+' ?')
			else :
				store_newuser_data()
		else :
			giveuchat('Make sure to fill only numbers between 0-100')


def get_newuser_data():
	global frame5 , genudata , genudvar , chats1 , chats2
	frame5 = Frame(rootu, height = 500, width = 850)
	frame5.place(x = 350, y = 100)
	umod_imaglabel = Label(frame5 , image = umod_imag,  bd = 0).place(x = 0, y = 0)
	genudata = []
	genudvar = 0
	chats1 = ['physics','chemistry','maths','biology']
	chats2 = ['What\'s your marks in ','How much did you score in ']


def get_user0_datas():
	global frame5 , umvar
	datas = (phymark.get()+chemmark.get()+mathmark.get()+biomark.get())
	if datas.isdigit() :
		datas = [int(phymark.get()),int(chemmark.get()),int(mathmark.get()),int(biomark.get()),cityname.get(),castevalvar.get()]

		if datas[:4] == userrow[0][3:7] and datas[4] == userrow[0][10] and datas[5] == userrow[0][9] :
			user1()
		else:
			for mark in datas[:4] :
				if mark > 100 or mark < 0:
					msgbox.showinfo(title = 'Alert!' , message = 'Marks should be from 0 to 100')
					umvar -= 1
					break
			else :
				frame5.destroy()
				cutoff_mark = datas[0]/2 + datas[1]/2 + datas[2]
				if datas[4] == 'NIL':
					cursor3.execute(f'update user set  phymark = {datas[0]}, chemark = {datas[1]}, mathmark = {datas[2]}, biomark = {datas[3]}, cutoff = {cutoff_mark}, city = NULL , caste = "{datas[5]}" where userid = "{uid}" ')
				else:
					cursor3.execute(f'update user set  phymark = {datas[0]}, chemark = {datas[1]}, mathmark = {datas[2]}, biomark = {datas[3]}, cutoff = {cutoff_mark}, city = "{datas[4]}", caste = "{datas[5]}" where userid = "{uid}" ')
				connection3.commit()
				user1()

	else :
		msgbox.showinfo(title = 'Alert!' , message = 'Make sure to fill only numbers')
		umvar -= 1

def show_colleges_frame5_user1(colleges):
	global reportlist
	collegeWindow = Text(frame5, bd = 2, wrap = 'none' , bg='#f0f0f0', fg = '#000000',cursor = 'hand2' , width='100', height='28', font=('Courier',10), insertbackground = '#000000' ,insertborderwidth = 10 )
	collegeWindow.place(x = 6, y = 6)

	collWscrollbary = Scrollbar(frame5, orient="vertical", command=collegeWindow.yview)
	collWscrollbary.place(x = 818,y = 6, height = 456)

	collWscrollbarx = Scrollbar(frame5, orient="horizontal", command=collegeWindow.xview)
	collWscrollbarx.place(x = 6,y = 471, width = 807)
	collegeWindow.configure(yscrollcommand = collWscrollbary.set , xscrollcommand = collWscrollbarx.set)


	_1 = myconn.addspace('Code',5)
	_2 = myconn.addspace('Name',100)
	_3 = myconn.addspace('City',35)
	_4 = myconn.addspace('Course',64)
	_5 = myconn.addspace('Cutoff',8)
	collegeWindow.insert(END,_1+'| '+_2+'| '+_3+'| '+_4+'| '+_5+'\n')
	collegeWindow.insert(END,('-'*223)+'\n')

	reportlist = []
	reportlist.append('='*223)
	reportlist.append(_1+'| '+_2+'| '+_3+'| '+_4+'| '+_5)
	reportlist.append('='*223)

	colleges_new = []

	for i in colleges:
		_1 = myconn.addspace(str(i[0]),5)
		_2 = myconn.addspace(i[1],100)
		_3 = myconn.addspace(i[4]+','+i[5],35)
		_4 = myconn.addspace(i[7]+' : '+courses_dict[i[7]],64)

		_cutoff = i[castetuple.index(userrow[0][9])+8]

		if _cutoff == 0.0 :
			_cutoff = i[8]

		colleges_new.append([_cutoff,_1,_2,_3,_4])

	colleges_new_rp = sort_cols(colleges_new)

	for i in colleges_new_rp:
		_5 = myconn.addspace(i[0],8)
		collegeWindow.insert(END,i[1]+'| '+i[2]+'| '+i[3]+'| '+i[4]+'| '+_5+'\n')
		collegeWindow.insert(END,('-'*223)+'\n')
		reportlist.append(i[1]+'| '+i[2]+'| '+i[3]+'| '+i[4]+'| '+_5)
		reportlist.append('-'*223)

	collegeWindow.configure(state = DISABLED)

def pdf_report():

	pdf = FPDF()
	pdf.add_page('L')
	pdf.set_xy(0,0)
	pdf.set_font('Arial','B',14)
	headerline = "List of recommended colleges and courses for user: "+uid
	pdf.write(10,headerline)
	pdf.set_font('courier','',6)
	for rowline in reportlist:
		pdf.ln(h='')
		pdf.cell(-10)
		for towrt in str(rowline):
			pdf.write(3,towrt)
	outfile = pdf.output(dest='S').encode('latin-1')
	f = filedialog.asksaveasfile(mode='wb', initialfile = uid+"_ColGenieReport.pdf")
	if f is None:
		msgbox.showinfo(title = 'Alert!' , message = 'No file selected')
	else:
		f.write(outfile)
		f.close()
		msgbox.showinfo(title = 'Alert!' , message = 'Report File created')


def sort_cols(col_list):
	for i in range(1,len(col_list)):
		key = col_list[i]
		j = i - 1
		while j >= 0 and key[0] > col_list[j][0]:
			col_list[j+1] = col_list[j]
			j -= 1
		else:
			col_list[j+1] = key
	return col_list

def showcol_manycities_user1(cities):
	global frame5, reportflag
	cities_new = ()

	if not len(cities):
		msgbox.showinfo(title = 'Alert!' , message = 'Choose an option\nThen press GO!')
	else:
		if len(cities) == 1:
			cities_new = (cities[0].split(','))[0]
			cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and city = \'{cities_new}\' and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')

		else:
			for city in cities:
				cities_new += ((city.split(','))[0],)
			cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and city in {cities_new} and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')

		frame5.destroy()
		frame5 = Frame(rootu, height = 500, width = 850, bg = '#e6e6fa')
		frame5.place(x = 350, y = 100)
		frame5c = Frame(frame5, height = 500, width = 850, bg = '#E0D6D7')
		frame5c.place(x = 0,y = 0)
		a = list(cursor3)
		if not len(a):
			reportflag = 0
			giveuchat('*** No colleges available for your cutoff, caste category, and selected cities. ***')
		else:
			reportflag = 1
			giveuchat('For your cutoff of '+str(userrow[0][7])+' and caste category '+str(userrow[0][9]+' eligible colleges and courses are listed :'))
			giveuchat(optiontext)

			cols = sort_cols(a)

			show_colleges_frame5_user1(cols)

def showcol_city_user1():
	global reportflag

	if userrow[0][10] is None:
		cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')
	else:
		city_course = (userrow[0][10].split(','))[0]
		cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and city = \'{city_course}\' and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')
	a = list(cursor3)
	if not len(a):
		reportflag = 0
		giveuchat('*** No colleges available for your cutoff, caste category, and city(ies). ***')
	else:
		reportflag = 1
		giveuchat('For your cutoff of '+str(userrow[0][7])+' and caste category '+str(userrow[0][9]+' eligible colleges and courses are listed :'))
		giveuchat(optiontext)

		cols = sort_cols(a)

		show_colleges_frame5_user1(cols)

def showcol_manycourses_user1(courses):
	global frame5, reportflag
	courses_new = ()

	if not len(courses):
		msgbox.showinfo(title = 'Alert!' , message = 'Choose an option\nThen press GO!')
	else:
		if len(courses) == 1:
			courses_new = courses[0][0]

			cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and c2.courseid = \'{courses_new}\' and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')

		else:
			for course in courses:
				courses_new += (course[0],)
			cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and c2.courseid in {courses_new} and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')


		frame5.destroy()
		frame5 = Frame(rootu, height = 500, width = 850, bg = '#e6e6fa')
		frame5.place(x = 350, y = 100)

		frame5c = Frame(frame5, height = 500, width = 850, bg = '#E0D6D7')
		frame5c.place(x = 0,y = 0)
		a = list(cursor3)
		if not len(a):
			reportflag = 0
			giveuchat('*** No colleges available for your cutoff, caste category, and selected courses. ***')
		else:
			reportflag = 1
			giveuchat('For your cutoff of '+str(userrow[0][7])+' and caste category '+str(userrow[0][9]+' and selected courses, eligible colleges and courses are listed :'))
			giveuchat(optiontext)

			cols = sort_cols(a)

			show_colleges_frame5_user1(cols)



def user1(flag_user1 = None):
	global frame5 , userrow , courses_dict , frame5c

	cursor3.execute(f'select * from user where userid = "{uid}" ')
	userrow = cursor3.fetchall()

	cursor3.execute('select * from codes')
	courses = list(cursor3)
	courses.sort()
	courses_dict = {}
	for i in courses:
		courses_dict[i[0]] = i[1]

	try:
		frame5.destroy()
	except:
		pass

	frame5 = Frame(rootu, height = 500, width = 850, bg = '#e6e6fa')
	frame5.place(x = 350, y = 100)
	frame5.grid_propagate(0)
	umod_imaglabel = Label(frame5 , image = umod_imag,  bd = 0).place(x = 0, y = 0)

	if flag_user1 is None :
		giveuchat(optiontext)

	elif flag_user1 == '1':
		frame5c = Frame(frame5, height = 500, width = 850, bg = '#E0D6D7')
		frame5c.place(x = 0,y = 0)
		showcol_city_user1()

	elif flag_user1 == '2':


		cities_user1_Vars = []
		cities_user1 = []

		giveuchat('Select your preferred cities and press GO.')

		def get_cities_user1():
			nonlocal cities_user1
			
			if CityVarminus1.get() == -1:
				cities_user1 = list(cities)
			else :
				cities_user1 = []
				for i in range(len(cities_user1_Vars)):
					if (globals()[cities_user1_Vars[i][0]]).get() :
						cities_user1.append(cities[i])

			showcol_manycities_user1(cities_user1)


		def _on_mousewheel(event):
			try:
				canvas_cities.yview_scroll(int(-1*(event.delta/120)), "units")
			except Exception :
				pass

		def configfunc(event):
			canvas_cities.config(scrollregion = canvas_cities.bbox('all'))

		canvas_cities = Canvas(frame5)
		frame5a = Frame(canvas_cities,bd = 5)
		myscrollbar = Scrollbar(frame5,orient = VERTICAL,command = canvas_cities.yview)
		canvas_cities.configure(yscrollcommand = myscrollbar.set)

		canvas_cities.grid(row = 0,column = 0)
		myscrollbar.grid(row = 0,column = 1,sticky = 'ns')
		canvas_cities.create_window((0,0),window = frame5a,anchor = 'nw')

		frame5a.bind('<Configure>',configfunc)

		canvas_cities.bind_all("<MouseWheel>", _on_mousewheel)

		cursor3.execute('select distinct city,state from college')
		cities = [str(c[0]+','+c[1]) for c in cursor3]
		cities.sort()
		CityVarminus1 = IntVar()
		CityAll = ttk.Checkbutton(frame5a,text = 'ALL' , variable = CityVarminus1,onvalue = -1 ,offvalue = 0)
		CityAll.grid(row = 0,sticky = 'w')

		for numb in range(len(cities)):
			globals()['CityVar'+str(numb)] = IntVar()
			globals()['City'+str(numb+1)] = ttk.Checkbutton(frame5a,text = cities[numb],\
				variable = globals()['CityVar'+str(numb)],onvalue = 1 ,offvalue = 0)
			(globals()['City'+str(numb+1)]).grid(row = numb + 1,sticky = 'w')

			cities_user1_Vars.append(['CityVar'+str(numb),'City'+str(numb+1)])

		donebtn_cities = ttk.Button(frame5,text = 'GO', width = 10,command = get_cities_user1)
		donebtn_cities.grid(row = 0,column = 2,sticky = 's')


	elif flag_user1 == '3':

		courses_user1_Vars = []
		courses_user1 = []

		giveuchat('Select your preferred courses and press GO.')

		def get_courses_user1():
			nonlocal courses_user1
			
			if CourseVarminus1.get() == -1:
				courses_user1 = list(courses)
			else :
				courses_user1 = []
				for i in range(len(courses_user1_Vars)):
					if (globals()[courses_user1_Vars[i][0]]).get() :
						courses_user1.append(list(courses[i]))
			showcol_manycourses_user1(courses_user1)


		def _on_mousewheel(event):
			try:
				canvas_courses.yview_scroll(int(-1*(event.delta/120)), "units")
			except Exception :
				pass

		def configfunc(event):
			canvas_courses.config(scrollregion = canvas_courses.bbox('all'))

		canvas_courses = Canvas(frame5)
		frame5a = Frame(canvas_courses,bd = 5)
		myscrollbar = Scrollbar(frame5,orient = VERTICAL,command = canvas_courses.yview)
		canvas_courses.configure(yscrollcommand = myscrollbar.set)

		canvas_courses.grid(row = 0,column = 0)
		myscrollbar.grid(row = 0,column = 1,sticky = 'ns')
		canvas_courses.create_window((0,0),window = frame5a,anchor = 'nw')

		frame5a.bind('<Configure>',configfunc)

		canvas_courses.bind_all("<MouseWheel>", _on_mousewheel)

		CourseVarminus1 = IntVar()
		CourseAll = ttk.Checkbutton(frame5a,text = 'ALL' , variable = CourseVarminus1,onvalue = -1 ,offvalue = 0)
		CourseAll.grid(row = 0,sticky = 'w')

		for numb in range(len(courses)):

			globals()['CourseVar'+str(numb)] = IntVar()

			globals()['Course'+str(numb+1)] = ttk.Checkbutton(frame5a,text = courses[numb],\
				variable = globals()['CourseVar'+str(numb)],onvalue = 1 ,offvalue = 0)
			(globals()['Course'+str(numb+1)]).grid(row = numb + 1,sticky = 'w')

			courses_user1_Vars.append(['CourseVar'+str(numb),'Course'+str(numb+1)])

		donebtn_courses = ttk.Button(frame5,text = 'GO',width = 10,command = get_courses_user1)
		donebtn_courses.grid(row = 0,column = 2,sticky = 's')

	elif flag_user1 == '4' :
		frame5.destroy()
		advanced_search()

	else :
		give_errorchat()

def showcol_advanced_user1(cities,courses):
	global frame5, reportflag

	cities_new = ()
	courses_new = ()

	if not len(cities) or not len(courses) :
		msgbox.showinfo(title = 'Alert!' , message = 'Choose options\nThen press GO!')
	else:
		for city in cities:
			cities_new += ((city.split(','))[0],)
		if len(cities_new) == 1:
			cities_new += (cities_new[0],)

		for course in courses:
			courses_new += (course[0],)
		if len(courses_new) == 1:
			courses_new += (courses_new[0],)

		cursor3.execute(f'select * from college c1 natural join course c2 where c1.collegeid = c2.collegeid and city in {cities_new} and c2.courseid in {courses_new} and (({userrow[0][9]} = 0.0 and OC <= {userrow[0][7]}) or ({userrow[0][9]} <= {userrow[0][7]}))')

		frame5.destroy()
		frame5 = Frame(rootu, height = 500, width = 850, bg = '#e6e6fa')
		frame5.place(x = 350, y = 100)

		frame5c = Frame(frame5, height = 500, width = 850, bg = '#E0D6D7')
		frame5c.place(x = 0,y = 0)

		a = list(cursor3)
		if not len(a):
			reportflag = 0
			giveuchat('*** No colleges available for your cutoff, caste category, and selected cities and courses. ***')
		else:
			reportflag = 1
			giveuchat('For your cutoff of '+str(userrow[0][7])+' and caste category '+str(userrow[0][9]+' and selected cities and courses, eligible colleges and courses are listed :'))
			giveuchat(optiontext)

			cols = sort_cols(a)

			show_colleges_frame5_user1(cols)

def advanced_search():
	global frame5 , courses_dict

	frame5 = Frame(rootu, height = 500, width = 850, bg = '#e6e6fa')
	frame5.place(x = 350, y = 100)
	frame5.grid_propagate(0)
	umod_imaglabel = Label(frame5 , image = umod_imag,  bd = 0).place(x=0,y = 0)

	giveuchat('Select your preferred courses and courses and press GO.')

	cursor3.execute('select * from codes')
	courses = list(cursor3)
	courses.sort()
	courses_dict = {}
	for i in courses:
		courses_dict[i[0]] = i[1]


	cities_user1_Vars = []
	cities_user1 = []

	courses_user1_Vars = []
	courses_user1 = []

	def get_city_course_user1():
		nonlocal cities_user1 , courses_user1
		
		if CityVarminus1.get() == -1:
			cities_user1 = list(cities)
		else :
			cities_user1 = []
			for i in range(len(cities_user1_Vars)):
				if (globals()[cities_user1_Vars[i][0]]).get() :
					cities_user1.append(cities[i])

		if CourseVarminus1.get() == -1:
				courses_user1 = list(courses)
		else :
			courses_user1 = []
			for i in range(len(courses_user1_Vars)):
				if (globals()[courses_user1_Vars[i][0]]).get() :
					courses_user1.append(list(courses[i]))

		showcol_advanced_user1(cities_user1,courses_user1)


	def configfunc_cities(event):
		canvas_cities.config(scrollregion = canvas_cities.bbox('all'))


	def configfunc_courses(event):
		canvas_courses.config(scrollregion = canvas_courses.bbox('all'))



	canvas_cities = Canvas(frame5,width = 360)
	canvas_courses = Canvas(frame5)
	frame5a = Frame(canvas_cities,bd = 5)
	frame5b = Frame(canvas_courses,bd = 5)
	myscrollbar_cities = Scrollbar(frame5,orient = VERTICAL,command = canvas_cities.yview)
	canvas_cities.configure(yscrollcommand = myscrollbar_cities.set)
	myscrollbar_courses = Scrollbar(frame5,orient = VERTICAL,command = canvas_courses.yview)
	canvas_courses.configure(yscrollcommand = myscrollbar_courses.set)

	canvas_cities.grid(row = 0,column = 0)
	myscrollbar_cities.grid(row = 0,column = 1,sticky = 'ns')
	canvas_cities.create_window((0,0),window = frame5a,anchor = 'nw')

	donebtn_cities = ttk.Button(frame5,text = 'GO',width = 10,command = get_city_course_user1)
	donebtn_cities.grid(row = 0,column = 2,sticky = 's')

	canvas_courses.grid(row = 0,column = 3)
	myscrollbar_courses.grid(row = 0,column = 4,sticky = 'ns')
	canvas_courses.create_window((0,0),window = frame5b,anchor = 'nw')


	frame5a.bind('<Configure>',configfunc_cities)
	frame5b.bind('<Configure>',configfunc_courses)

	cursor3.execute('select distinct city,state from college')
	cities = [str(c[0]+','+c[1]) for c in cursor3]
	cities.sort()

	CityVarminus1 = IntVar()
	CityAll = ttk.Checkbutton(frame5a,text = 'ALL' , variable = CityVarminus1,onvalue = -1 ,offvalue = 0)
	CityAll.grid(row = 0,sticky = 'w')

	CourseVarminus1 = IntVar()
	CourseAll = ttk.Checkbutton(frame5b,text = 'ALL' , variable = CourseVarminus1,onvalue = -1 ,offvalue = 0)
	CourseAll.grid(row = 0,sticky = 'w')

	for numb in range(len(cities)):
		globals()['CityVar'+str(numb)] = IntVar()
		globals()['City'+str(numb+1)] = ttk.Checkbutton(frame5a,text = cities[numb],\
			variable = globals()['CityVar'+str(numb)],onvalue = 1 ,offvalue = 0)
		(globals()['City'+str(numb+1)]).grid(row = numb + 1,sticky = 'w')
		cities_user1_Vars.append(['CityVar'+str(numb),'City'+str(numb+1)])

	for numb in range(len(courses)):
		globals()['CourseVar'+str(numb)] = IntVar()
		globals()['Course'+str(numb+1)] = ttk.Checkbutton(frame5b,text = courses[numb],\
			variable = globals()['CourseVar'+str(numb)],onvalue = 1 ,offvalue = 0)
		(globals()['Course'+str(numb+1)]).grid(row = numb + 1,sticky = 'w')
		courses_user1_Vars.append(['CourseVar'+str(numb),'Course'+str(numb+1)])




def showcitylist_user0():

	def selectcity():
		try:
			citybox.configure(state = NORMAL)
			cityvalue = citylist.get(citylist.curselection())
			citybox.delete(0,END)
			citybox.insert(0,cityvalue)
			citybox.configure(state = DISABLED)
		except:
			msgbox.showinfo(title = 'Alert!' , message = 'Please select a city to confirm')

	def cancelselection():
		citybox.configure(state = NORMAL)
		citybox.delete(0,END)
		if userrow[0][10] is not None :
			citybox.insert(0,userrow[0][10])
		else :
			citybox.insert(0,'NIL')
		citybox.configure(state = DISABLED)

	frame5a = Frame(frame5)
	frame5a.place(x = 500, y = 90)

	citylist = Listbox(frame5a, height = 10, width = 15, cursor = 'hand2' , font = ('Helvetica',12), highlightcolor = '#000033' , bg = '#cfdfe6' , fg = '#000033',selectbackground = '#000033' , selectforeground = '#f0f0f0')
	citylist.grid(row = 0, column = 0)
	cursor3.execute('select distinct city,state from college')
	cities = [str(c[0]+','+c[1]) for c in cursor3]
	cities.sort()
	citylist.insert(0 , 'NIL')
	for numb in range(1,len(cities)+1):
		citylist.insert(numb , cities[numb-1])

	xscrolb=Scrollbar(frame5a, orient = HORIZONTAL, command = citylist.xview)
	yscrolb=Scrollbar(frame5a, orient = VERTICAL, command = citylist.yview)

	citylist.configure(xscroll = xscrolb.set, yscroll = yscrolb.set)

	xscrolb.grid(row = 1, column = 0, sticky = 'ew')
	yscrolb.grid(row = 0, column = 1, sticky = 'ns')

	confirmbtn = Button(frame5a,text = 'Confirm', cursor = 'hand2',command = selectcity)
	confirmbtn.grid(row = 2,column = 0,sticky = 'sw')

	cancelbtn = Button(frame5a,text = 'Cancel', cursor = 'hand2',command = cancelselection)
	cancelbtn.grid(row = 2,column = 0,sticky = 'se')

		


def user0():
	global frame5 , phymark , chemmark , mathmark , biomark , cityname , userrow , citybox , castevalvar , castetuple

	frame5 = Frame(rootu, height = 500, width = 850, bg = '#ffffe0')
	frame5.place(x = 350, y = 100)

	umod_imaglabel = Label(frame5 , image = umod_imag,  bd = 0).place(x = 0, y = 0)

	cursor3.execute(f'select * from user where userid = "{uid}" ')
	userrow = cursor3.fetchall()

	giveuchat('Your details are displayed here(choosing a city will help in recommending the colleges near you), you can make changes to your data if required then type NEXT to move on. To come back here type back. (And don\'t forget to choose your caste; default is OC.)(Giving your city as NIL will lead to recommending colleges from every city.To exit give exit or quit.')

	phymark = StringVar()
	phymarklabel = Label(frame5, text = 'Physics  :-      ', bd = 1 , relief = 'solid', bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 20, y = 60)
	phyboxul = Label(frame5 , text = '        ' ,bd = 0, bg = '#000000', font = ('Helvetica',12) , cursor = 'hand2').place(x = 120, y = 64)
	phymarkbox = Entry(frame5 ,bd = 0, width=4, fg = '#000033' ,bg = '#cfdfe6', font = ('Helvetica',12) , cursor = 'hand2',textvariable = phymark)
	phymarkbox.place(x = 120, y = 60)
	phymarkbox.insert(0,userrow[0][3])

	chemmark = StringVar()
	chemmarklabel = Label(frame5, text = 'Chemistry:-    ', bd = 1 , relief = 'solid',  bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 20, y = 100)
	chemmboxul = Label(frame5 , text = '        ' ,bd = 0, bg = '#000000', font = ('Helvetica',12) , cursor = 'hand2').place(x = 120, y = 104)
	chemmarkbox = Entry(frame5 ,bd = 0, width=4, fg = '#000033' ,bg = '#cfdfe6', font = ('Helvetica',12) , cursor = 'hand2',textvariable = chemmark)
	chemmarkbox.place(x = 120, y = 100)
	chemmarkbox.insert(0,userrow[0][4])

	mathmark = StringVar()
	mathmarklabel = Label(frame5, text = 'Maths    :-       ', bd = 1 , relief = 'solid',  bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 20, y = 140)
	mathboxul = Label(frame5 , text = '        ' ,bd = 0, bg = '#000000', font = ('Helvetica',12) , cursor = 'hand2').place(x = 120, y = 144)
	mathmarkbox = Entry(frame5 ,bd = 0, width=4, fg = '#000033' ,bg = '#cfdfe6', font = ('Helvetica',12) , cursor = 'hand2',textvariable = mathmark)
	mathmarkbox.place(x = 120, y = 140)
	mathmarkbox.insert(0,userrow[0][5])

	biomark = StringVar()
	biomarklabel = Label(frame5, text = 'Biology  :-      ', bd = 1 , relief = 'solid',  bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 20, y = 180)
	bioboxul = Label(frame5 , text = '        ' ,bd = 0, bg = '#000000', font = ('Helvetica',12) , cursor = 'hand2').place(x = 120, y = 184)
	biomarkbox = Entry(frame5 ,bd = 0, width=4, fg = '#000033' ,bg = '#cfdfe6', font = ('Helvetica',12) , cursor = 'hand2',textvariable = biomark)
	biomarkbox.place(x = 120, y = 180)
	biomarkbox.insert(0,userrow[0][6])

	cityname = StringVar()
	citylabel = Label(frame5, text = 'City     :-', bd = 1 , relief = 'solid',  bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 420, y = 60)
	cityboxul = Label(frame5 , text = '\t\t' ,bd = 0, bg = '#000000', font = ('Helvetica',12) , cursor = 'hand2').place(x = 500, y = 64)
	citybox = Entry(frame5 ,bd = 0,highlightcolor = 'blue', bg = '#ffffe0',width = 16, font = ('Helvetica',12) , textvariable = cityname)
	citybox.place(x = 500, y = 58)

	if userrow[0][10] is None :
		citybox.insert(0,'NIL')
	else :
		citybox.insert(0,userrow[0][10])

	citybox.configure(state = DISABLED)

	showcitylist_user0()


	Labelcaste = Label(frame5, text = '        CASTE        ', bd = 1 , relief = 'solid',  bg = '#f0f0f0', font = ('Helvetica',12)).place(x = 250, y = 60)
	frame5caste = Frame(frame5,width = 118 , height = 170 , bd = 1 , relief = 'sunken' )
	frame5caste.place(x = 252, y = 100)
	frame5caste.pack_propagate(0)
	castevalvar = StringVar()
	castetuple = ('OC','BC','BCM','MBC','SC','SCA','ST')
	caste_indb = userrow[0][9]
	caste_indb_index = castetuple.index(caste_indb)

	OCbutton = ttk.Radiobutton(frame5caste, text = castetuple[0], variable = castevalvar, value = castetuple[0])
	OCbutton.place(x = 35,y = 0)
	BCbutton = ttk.Radiobutton(frame5caste, text = castetuple[1], variable = castevalvar, value = castetuple[1])
	BCbutton.place(x = 35,y = 25)
	BCMbutton = ttk.Radiobutton(frame5caste, text = castetuple[2], variable = castevalvar, value = castetuple[2])
	BCMbutton.place(x = 35,y = 50)
	MBCbutton = ttk.Radiobutton(frame5caste, text = castetuple[3], variable = castevalvar, value = castetuple[3])
	MBCbutton.place(x = 35,y = 75)
	SCbutton = ttk.Radiobutton(frame5caste, text = castetuple[4], variable = castevalvar, value = castetuple[4])
	SCbutton.place(x = 35,y = 100)
	SCAbutton = ttk.Radiobutton(frame5caste, text = castetuple[5], variable = castevalvar, value = castetuple[5])
	SCAbutton.place(x = 35,y = 125)
	STbutton = ttk.Radiobutton(frame5caste, text = castetuple[6], variable = castevalvar, value = castetuple[6])
	STbutton.place(x = 35,y = 150)

	caste_buttons = (OCbutton,BCbutton,BCMbutton,MBCbutton,SCbutton,SCAbutton,STbutton)


	for btn in caste_buttons :
		if caste_buttons.index(btn) != caste_indb_index :
			pass
		else:
			btn.invoke()

	try:
		while True:
			rootu.update()
	except:
		pass



def userpage(id,name,new = 1):
	global  uchat , umod_imag , chatWindow , messageWindow , cwnumb , uid , umvar, reportflag

	reportflag = 0
	cwnumb = 1
	uid = id

	rootuw()
	cnxu()

	uchat = StringVar()

	umod_imagload = Image.open('.\\images\\usermdbg.png')
	umod_imag = ImageTk.PhotoImage(umod_imagload)

	frame1b = Frame(rootu, height = 100, width = 1200, bg = '#E0D6D7')
	frame1b.place(x = 0, y = 0)

	header_img = ImageTk.PhotoImage(Image.open('.\\images\\colbg_head.png'))

	labelcbb = Label(frame1b,image = header_img, fg = '#bff0ff', bg = '#E0D6D7')
	labelcbb.place(x = 0, y = 0)

	framechat = Frame(rootu, height = 500, width = 350, bg = '#E0D6D7')
	framechat.place(x = 0, y = 100)

	chatWindow = Text(framechat, bd = 3, wrap = 'word', bg = '#F5F0EF', cursor = '' , width='50', height='8', font=('calibri',14), insertbackground = '#a1ffef' , foreground='#000a33')
	chatWindow.place(x = 6,y = 6, height = 385, width = 320)
	chatWindow.configure(state = DISABLED)
	giveuchat('Hello ' + name + ' :)')

	messageWindow = Text(framechat, bd = 3 , wrap = 'word', bg = 'black', font=('calibri',16), insertbackground = '#a1ffef' , insertwidth = 3, foreground='#00ffff' )
	messageWindow.place(x = 6, y = 400, height = 50, width = 337)
	messageWindow.focus_set()

	scrollbar = Scrollbar(framechat, orient = "vertical", command = chatWindow.yview)
	scrollbar.place(x = 326,y = 6, height = 385)
	chatWindow.configure(yscrollcommand = scrollbar.set)

	sendbutton_img = ImageTk.PhotoImage(Image.open('.\\images\\sendbtn.png'))
	sendbutton = Button(framechat, cursor = 'hand2' ,  bg = '#E0D6D7' ,bd = 0 ,  image = sendbutton_img, activebackground = '#129443', command = lambda :  getuchat(messageWindow.get('1.0','end-1c')) )
	sendbutton.place(x = 6, y = 455, height = 40 , width = 337)

	if new :
		umvar = -1
		get_newuser_data()

	else :
		umvar = 0
		user0()

	rootu.mainloop()


if __name__ == '__main__':
	userpage('theuser1','ssk',0)
