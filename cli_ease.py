import MySQLdb
import curses
import smtplib
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

#Function to print menu and get user selection
#No parameters, returns char user selcted.
def printMenu():
	screen.addstr("\nPlease Select from the following menu:\n")
	screen.addstr("1)View Appointments\n2)Cancel Appointment\n3)Exit\n")
	selection = screen.getch()
	return selection;

#function to handle the reading of the database
#2 parameters, advisor's name as a string with literal quotes 
#and advisor's name as normal string. 
#Returns the number of rows / appointments
def readDatabase(str_advisor, advisor):
	sql_read = "SELECT date_time, ad_name, st_name FROM advising_schedule WHERE advising_schedule.ad_name = " + str_advisor + "\n"
	#screen.addstr("SQL query is: " + sql_read) #Debugging SQL query 
	screen.addstr("\nSchedule for " + advisor + "\n")
	cursor.execute(sql_read)
	results = cursor.fetchall()
	num = 0
	for row in results:
		num = num + 1
		appdate_time = row[0]
		aname = row[1]
		sname = row[2]
		newdate_time = str(appdate_time) #must change from object to string
		screen.addstr("Appointment with student: " + sname + " On: " + newdate_time + "\n")
	return num;

#Think once the files Andrew are working on will be able to call those instead
def emailTemp(stu_email, ad_email, student, adviser, date_time):
	screen.addstr("DO I get to email function???\n")
	sender = 'do.not.reply@engr.orst.edu'
	receivers = [stu_email, ad_email]
	message = """From: From EECS Advising <do.not.reply.@engr.orst.edu>
To: To """ + student + """ <""" + stu_email + """>
Subject: Advising Signup Cancellation

Advising Signup with """ + adviser + """ CANCELLED
Name: """ + student + """
Email: """ + stu_email + """
Date: """ + date_time+ """

Please contact support@engr.oregonstate.edu if you experience problems.
"""

	try:
		smtpObj = smtplib.SMTP('mail.engr.oregonstate.edu', 25)
		smtpObj.sendmail(sender, receivers, message)
		screen.addstr("An email has been sent to you and the student")
	except:
		screen.addstr("Error: Unable to send email.")
	return;
	
	
def cancelApp(str_advisor, advisor):
	t_rows = readDatabase(str_advisor, advisor)
	str_tRows = str(t_rows)
	screen.addstr("\nUsing 1 through " + str_tRows + " select the number that coincides with the appointment you want to cancel.\n")
	select = screen.getstr()
	print select
	sql_read = "SELECT date_time, ad_name, st_name FROM advising_schedule WHERE advising_schedule.ad_name = " + str_advisor + "\n"
	#screen.addstr("SQL query is: " + sql_read) #Debugging checking that SQL query appeared the way it should
	cursor.execute(sql_read)
	results = cursor.fetchall()
	num2 = 0
	for row in results:
		num2 = num2 + 1
		appdate_time = row[0]
		aname = row[1]
		sname = row[2]
		newdate_time = str(appdate_time) #must change from object to string
		if num2 == int(select):
			screen.addstr("STOP HERE " + str(num2) + "\n" )
			str_s_name = "'" + sname + "'"
			sql_emails = "SELECT ad_email, st_email FROM advising_schedule WHERE ad_name = " + str_advisor + " AND st_name = " + str_s_name + ";\n"
			screen.addstr("sql emails looks like this: \n" + sql_emails + "\n")
			cursor.execute(sql_emails)
			emails = cursor.fetchall()
			for row in emails:
				adv_email = row[0]
				stud_email = row[1]
			screen.addstr("Sending Cancellation Email to " + adv_email + " and " + stud_email + " for " + newdate_time + "\n")
			str_date = "'" + newdate_time + "'"
			sql_del = "DELETE FROM advising_schedule WHERE ad_name = " + str_advisor + " AND st_name = " + str_s_name + " AND date_time = " + str_date + "\n"
			screen.addstr("SQL DELETE = \n" + sql_del + "\n")
			screen.addstr("Are you sure you want to continue? Y/N\n")
			confirm = screen.getch()
			if confirm == ord("y") or confirm == ord("Y"):
				screen.addstr("\nAppointment is Cancelled\n")
				cursor.execute(sql_del)
				screen.addstr("Do I get here?\n")
				emailTemp(stud_email, adv_email, sname, advisor, newdate_time)
			elif confirm == ord("n") or confirm == ("N"):
				screen.addstr("\nAppointment has not been Cancelled\n")
			else:
				screen.addstr("\nIncorrect input. Appointment will not be Cancelled\n")
			break
	str_num = str(num2)
	screen.addstr("num of rows = " + str_num + "\n")


while True:
	screen.refresh()
	event = printMenu()
	
	if event == ord("3"):  #3 = They want to exit CLI client
		break
	elif event == ord("1"): #1 They want to read their advising schedule
		readDatabase(name2, name)
	elif event == ord("2"): #Cancel appointment
		cancelApp(name2, name)
curses.endwin()
