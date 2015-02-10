import MySQLdb
import curses
screen = curses.initscr()
#curses.noecho() #Stops key presses from the user from showing on screen
#curses.curs_set(0) #removes cursor from screen
#curse.cbreak() react instantly, user doesn't have to press the enter key
screen.keypad(1) #mode the screen uses to pature key presses.
db = MySQLdb.connect("mysql.eecs.oregonstate.edu", "cs419-g6", "group6data", "cs419-g6")
cursor = db.cursor() 
screen.scrollok(1)
screen.addstr("Welcome to the Simplified Advising Scheduling System\n")
screen.addstr("To begin please provide your first and last name.\n") #Need their name in every option, so might as well only ask for it once.

name = screen.getstr() #get the string they typed
name2 = "'" + name + "'" #force name into a string so it works with the SQL queries
while True:
	screen.refresh()
	screen.addstr("\nPlease Select from the following menu:\n1)View Appointments\n2)Create Appointment\n3)Delete Appointment\n4)Exit\n")
	event = screen.getch()
	
	if event == ord("4"): break # 4 = They want to exit CLI client
	elif event == ord("1"): # 1 They want to read their advising schedule
		sql_read = "SELECT * FROM (SELECT date, time, a_name, s_name FROM advising_schedule, advisor, student WHERE advising_schedule.ad_id = advisor.a_id AND advising_schedule.stud_id = student.s_id) AS alias WHERE alias.a_name = " + name2 + "\n"
		#screen.addstr("SQL query is: " + sql_read) #Debugging purposes checking that SQL query appeared the way it should
		try:
			screen.addstr("\nSchedule for " + name + "\n")
			cursor.execute(sql_read)
			results = cursor.fetchall()
			for row in results:
				appdate = row[0]
				apptime = row[1]
				aname = row[2]
				sname = row[3]
				newdate = str(appdate) #must change from object to string
				newtime = str(apptime) #same as above
				screen.addstr("Appointment with student: " + sname + " On: " + newdate + " At: " + newtime +"\n")
		except:
			screen.addstr("No Advisor named: " + name + "\n")
	elif event == ord("2"): #create appointment
		screen.addstr("\nTo create an appointment please provide:\nThe Student's first and last name\n")
		student_name = screen.getstr()
		strStudent_name = "'" + student_name + "'"
		screen.addstr("\nThe date in the form YYYY-MM-DD\n")
		date = screen.getstr()
		strDate = "'" + date + "'"
		screen.addstr("\nThe time using 24hour clock in the format HH:MM:SS.\n")
		time = screen.getstr()
		strTime = "'" + time + "'"
		try:
			sql_ids = "SELECT a_id, s_id  FROM advisor, student where a_name = " + name2 + "AND s_name = " + strStudent_name + "\n"
			cursor.execute(sql_ids)
			ids_result = cursor.fetchall()
			for row in ids_result:
				aid = row[0]
				sid = row[1]
				str_aid = str(aid)
				str_sid = str(sid)
				sql_create = "INSERT INTO advising_schedule (`ad_id`, `stud_id`, `date`, `time`) VALUES (" + str_aid + ", " + str_sid + ", " + strDate + ", " + strTime + ");"
				cursor.execute(sql_create)
			screen.addstr("Appointment has been created\n")
		except:
			screen.addstr("Something went wrong.\n")
	elif event == ord("3"): #delete appointment
		screen.addstr("\nTo delete an appointment please provide:\nThe Student's first and last name.\nThe date of the appointment\n")
	
	#screen.erase()
curses.endwin()
