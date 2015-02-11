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
	screen.addstr("\nPlease Select from the following menu:\n1)View Appointments\n2)Cancel Appointment\n3)Exit\n")
	event = screen.getch()
	
	if event == ord("3"): break # 4 = They want to exit CLI client
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
	elif event == ord("2"): #Cancel appointment
		screen.addstr("\nTo cancel an appointment please provide:\nThe Student's first and last name.\n")
		st_name = screen.getstr()
		str_st_name = "'" + st_name + "'"
		screen.addstr("\nThe date of the appointment in the format YYYY-MM-DD\n")
		can_date = screen.getstr() 
		str_can_date = str(can_date)
		sql_emails = "SELECT a_email, s_email FROM advisor, student WHERE advisor.a_name = " + name2 + " AND student.s_name = " + str_st_name + "\n"
		try:
			cursor.execute(sql_emails)
			emails = cursor.fetchall()
			for row in emails:
				ad_email = row[0]
				stud_email = row[1]
			screen.addstr("Sending Cancellation Email to " + ad_email + " and " + stud_email + " for " + str_can_date + "\nAre you sure you want to continue? Y/N\n")
			confirm = screen.getch()
			if confirm == ord("y") or confirm == ord("Y"):
				screen.addstr("\nAppointment is Cancelled\n")
				#Use provided and gathered info to send emails telling student and adviser that appointment is cancelled and procmail takes care of removing it from Outlook and database.
			elif confirm == ord("n") or confirm == ("N"):
				screen.addstr("\nAppointment has not been Cancelled\n")
			else:
				screen.addstr("\nDidn't Understand your input. Appointment will not be Cancelled\n")
		except:
			screen.addstr("\nError Please Try Again\n")
curses.endwin()
